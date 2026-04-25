"""
Import Complete Lok Sabha Election 2024 Data
Run: python scripts/import_loksabha_2024_complete.py
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
print("IMPORTING COMPLETE LOK SABHA 2024 DATA")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Find the CSV file
data_dir = project_root / 'data'
csv_files = glob.glob(str(data_dir / '**/*.csv'), recursive=True)

# Find file with 2024 in name
target_file = None
for f in csv_files:
    if '2024' in f and 'loksabha' in f.lower():
        target_file = f
        break

if not target_file:
    for f in csv_files:
        if '2024' in f:
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
    df.to_sql('loksabha_2024_complete', engine, if_exists='replace', index=False)
    print(f"✅ Imported to 'loksabha_2024_complete' table")
    
    # Find candidate name column
    name_col = None
    for col in df.columns:
        if any(name in col for name in ['candidate', 'name', 'cand']):
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
    
    if name_col:
        with engine.connect() as conn:
            # Add constituencies
            if const_col:
                conn.execute(text(f'''
                    INSERT IGNORE INTO constituencies (name, type)
                    SELECT DISTINCT {const_col}, 'PARLIAMENTARY'
                    FROM loksabha_2024_complete
                    WHERE {const_col} IS NOT NULL
                '''))
                print("✅ Constituencies added")
                
                # Add candidates with constituency_id
                conn.execute(text(f'''
                    INSERT IGNORE INTO candidates (name, party, constituency_id, is_current)
                    SELECT 
                        l.{name_col},
                        l.{party_col if party_col else "'Unknown'"},
                        c.id,
                        1
                    FROM loksabha_2024_complete l
                    JOIN constituencies c ON c.name = l.{const_col}
                    WHERE l.{name_col} IS NOT NULL
                '''))
            else:
                # Just add candidates without constituency
                conn.execute(text(f'''
                    INSERT IGNORE INTO candidates (name, party, is_current)
                    SELECT DISTINCT {name_col}, {party_col if party_col else "'Unknown'"}, 1
                    FROM loksabha_2024_complete
                    WHERE {name_col} IS NOT NULL
                '''))
            
            conn.commit()
            print("✅ Candidates added to main table")
    
    # Show final count
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
        print(f"\n📊 Total candidates in database: {result.fetchone()[0]}")
else:
    print("\n❌ No 2024 data file found. Files available:")
    for f in csv_files:
        print(f"  - {f}")