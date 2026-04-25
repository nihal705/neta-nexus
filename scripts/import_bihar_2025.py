"""
Import Bihar Assembly Elections 2025
Run: python scripts/import_bihar_2025.py
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
import glob

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env
def load_env():
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip()
    return True

load_env()

# Database connection
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "neta_nexus")

ENCODED_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("="*60)
print("IMPORTING BIHAR ASSEMBLY ELECTIONS 2025")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Find the CSV file
data_dir = project_root / 'data'
csv_files = glob.glob(str(data_dir / '**/*.csv'), recursive=True)

# Find Bihar file
target_file = None
for f in csv_files:
    if 'bihar' in f.lower():
        target_file = f
        break

if target_file:
    print(f"\n📖 Reading: {target_file}")
    df = pd.read_csv(target_file, encoding='latin-1')
    print(f"✅ Loaded {len(df)} records")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Import to database
    df.to_sql('bihar_2025', engine, if_exists='replace', index=False)
    print(f"✅ Imported to 'bihar_2025' table")
    
    # Find candidate name column
    name_col = None
    for col in df.columns:
        if any(name in col for name in ['candidate', 'name', 'winner', 'cand_name']):
            name_col = col
            break
    
    # Find party column
    party_col = None
    for col in df.columns:
        if 'party' in col:
            party_col = col
            break
    
    # Find constituency column
    const_col = None
    for col in df.columns:
        if 'constituency' in col:
            const_col = col
            break
    
    # Get Bihar state ID
    with engine.connect() as conn:
        # Check if Bihar state exists
        result = conn.execute(text("SELECT id FROM states WHERE code = 'BI'"))
        bihar_state = result.fetchone()
        
        if not bihar_state:
            conn.execute(text("INSERT INTO states (code, name, capital) VALUES ('BI', 'Bihar', 'Patna')"))
            conn.commit()
            result = conn.execute(text("SELECT id FROM states WHERE code = 'BI'"))
            bihar_state = result.fetchone()
        
        bihar_state_id = bihar_state[0] if bihar_state else None
    
    if name_col:
        with engine.connect() as conn:
            if const_col:
                # Add constituencies
                conn.execute(text(f'''
                    INSERT IGNORE INTO constituencies (name, type, state_id)
                    SELECT DISTINCT {const_col}, 'ASSEMBLY', {bihar_state_id}
                    FROM bihar_2025
                    WHERE {const_col} IS NOT NULL
                '''))
                print("✅ Constituencies added")
                
                # Add candidates with constituency_id
                conn.execute(text(f'''
                    INSERT IGNORE INTO candidates (name, party, constituency_id, state_id, is_current)
                    SELECT 
                        b.{name_col},
                        b.{party_col if party_col else "'Unknown'"},
                        c.id,
                        {bihar_state_id},
                        1
                    FROM bihar_2025 b
                    JOIN constituencies c ON c.name = b.{const_col}
                    WHERE b.{name_col} IS NOT NULL
                '''))
            else:
                # Just add candidates with state
                conn.execute(text(f'''
                    INSERT IGNORE INTO candidates (name, party, state_id, is_current)
                    SELECT DISTINCT {name_col}, {party_col if party_col else "'Unknown'"}, {bihar_state_id}, 1
                    FROM bihar_2025
                    WHERE {name_col} IS NOT NULL
                '''))
            
            conn.commit()
            print("✅ Candidates added to main table")
    
    # Show final count
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
        print(f"\n📊 Total candidates in database: {result.fetchone()[0]}")
else:
    print("\n❌ No Bihar file found. Please check the extracted folder structure.")
    print("Files found:")
    for f in csv_files:
        print(f"  - {f}")