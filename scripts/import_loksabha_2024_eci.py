"""
Import Complete Lok Sabha 2024 ECI Data
Run: python scripts/import_loksabha_2024_eci.py
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd

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
csv_file = project_root / 'data' / 'loksabha_2024_complete' / 'eci_data_2024.csv'

if csv_file.exists():
    print(f"\n📖 Reading: {csv_file}")
    df = pd.read_csv(csv_file, encoding='latin-1')
    print(f"✅ Loaded {len(df)} records")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Save to database
    df.to_sql('loksabha_2024_eci', engine, if_exists='replace', index=False)
    print("✅ Saved to loksabha_2024_eci table")
    
    # Find candidate name column
    name_col = None
    for col in df.columns:
        if 'candidate' in col or 'name' in col:
            name_col = col
            break
    
    # Find party column
    party_col = None
    for col in df.columns:
        if 'party' in col:
            party_col = col
            break
    
    print(f"\nUsing name column: {name_col}")
    print(f"Using party column: {party_col}")
    
    if name_col:
        with engine.connect() as conn:
            # Get unique candidates
            candidates_df = df[[name_col, party_col] if party_col else [name_col]].drop_duplicates()
            candidates_df = candidates_df[candidates_df[name_col].notna()]
            candidates_df = candidates_df[candidates_df[name_col] != '']
            
            print(f"\nFound {len(candidates_df)} unique candidates")
            
            # Insert in batches
            batch_size = 1000
            for i in range(0, len(candidates_df), batch_size):
                batch = candidates_df.iloc[i:i+batch_size]
                batch.to_sql('temp_candidates', engine, if_exists='replace', index=False)
                
                if party_col:
                    conn.execute(text("""
                        INSERT IGNORE INTO candidates (name, party, is_current)
                        SELECT name, party, 1 FROM temp_candidates
                    """))
                else:
                    conn.execute(text("""
                        INSERT IGNORE INTO candidates (name, is_current)
                        SELECT name, 1 FROM temp_candidates
                    """))
                conn.commit()
                print(f"   Inserted batch {i//batch_size + 1}")
            
            print("✅ Candidates added to main table")
    
    # Show final count
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
        print(f"\n📊 TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
else:
    print(f"\n❌ File not found: {csv_file}")
    print("Please check the file path")

print("\n🎉 Import complete!")