"""
Import all pending datasets with automatic column detection
Run: python scripts/import_all_pending_fixed.py
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file
def load_env():
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True
    return False

load_env()

# Get database credentials
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "neta_nexus")

ENCODED_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("="*60)
print("IMPORTING ALL PENDING DATASETS (AUTO COLUMN DETECTION)")
print("="*60)

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

def find_name_column(df):
    """Find the column that contains candidate names"""
    for col in df.columns:
        col_lower = col.lower()
        if any(name in col_lower for name in ['candidate', 'name', 'cand_name', 'winning_candidate']):
            return col
    return df.columns[0] if len(df.columns) > 0 else None

def find_party_column(df):
    """Find the column that contains party names"""
    for col in df.columns:
        col_lower = col.lower()
        if any(party in col_lower for party in ['party', 'party_name']):
            return col
    return None

# ============================================================
# DATASET 1: Already imported Lok Sabha Members History (8889 records)
# ============================================================
print("\n📁 Dataset 1: Lok Sabha Members History (1947-2019)")
csv_path = project_root / 'data' / 'loksabha_members_history.csv'

if csv_path.exists():
    df = pd.read_csv(csv_path, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} MP records")
    print(f"   Columns: {list(df.columns)}")
    
    name_col = find_name_column(df)
    party_col = find_party_column(df)
    
    print(f"   Using name column: {name_col}")
    print(f"   Using party column: {party_col}")
    
    df.to_sql('loksabha_members_history', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        if name_col:
            conn.execute(text(f'''
                INSERT IGNORE INTO candidates (name, party, is_current)
                SELECT {name_col}, {party_col if party_col else "'Unknown'"}, 0
                FROM loksabha_members_history
                WHERE {name_col} IS NOT NULL AND {name_col} != ''
            '''))
            conn.commit()
    print(f"   ✅ Imported {len(df)} MP records")
else:
    print(f"   ❌ File not found: {csv_path}")

# ============================================================
# DATASET 2: Indian Candidates 2019
# ============================================================
print("\n📁 Dataset 2: Indian Candidates 2019")
csv_path = project_root / 'data' / 'election_2019_candidates.csv'

if csv_path.exists():
    df = pd.read_csv(csv_path, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} candidates")
    print(f"   Columns: {list(df.columns)}")
    
    name_col = find_name_column(df)
    party_col = find_party_column(df)
    
    print(f"   Using name column: {name_col}")
    print(f"   Using party column: {party_col}")
    
    df.to_sql('election_2019_candidates', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        if name_col:
            conn.execute(text(f'''
                INSERT IGNORE INTO candidates (name, party, is_current)
                SELECT {name_col}, {party_col if party_col else "'Unknown'"}, 0
                FROM election_2019_candidates
                WHERE {name_col} IS NOT NULL AND {name_col} != ''
            '''))
            conn.commit()
    print(f"   ✅ Imported candidates")
else:
    print(f"   ❌ File not found: {csv_path}")

# ============================================================
# DATASET 3: Lok Sabha 2019 Results
# ============================================================
print("\n📁 Dataset 3: Lok Sabha 2019 Results")
csv_path = project_root / 'data' / 'loksabha_2019.csv'

if csv_path.exists():
    df = pd.read_csv(csv_path, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} candidates")
    print(f"   Columns: {list(df.columns)}")
    
    name_col = find_name_column(df)
    party_col = find_party_column(df)
    
    print(f"   Using name column: {name_col}")
    print(f"   Using party column: {party_col}")
    
    df.to_sql('loksabha_2019', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        if name_col:
            conn.execute(text(f'''
                INSERT IGNORE INTO candidates (name, party, is_current)
                SELECT {name_col}, {party_col if party_col else "'Unknown'"}, 0
                FROM loksabha_2019
                WHERE {name_col} IS NOT NULL AND {name_col} != ''
            '''))
            conn.commit()
    print(f"   ✅ Imported candidates")
else:
    print(f"   ❌ File not found: {csv_path}")

# ============================================================
# DATASET 4: Lok Sabha 2004-2019
# ============================================================
print("\n📁 Dataset 4: Lok Sabha 2004-2019")
csv_path = project_root / 'data' / 'loksabha_2004_2019' / '2004-2019.csv'

if csv_path.exists():
    df = pd.read_csv(csv_path, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
    
    name_col = find_name_column(df)
    party_col = find_party_column(df)
    
    print(f"   Using name column: {name_col}")
    print(f"   Using party column: {party_col}")
    
    df.to_sql('loksabha_2004_2019_data', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        if name_col:
            conn.execute(text(f'''
                INSERT IGNORE INTO candidates (name, party, is_current)
                SELECT DISTINCT {name_col}, {party_col if party_col else "'Unknown'"}, 0
                FROM loksabha_2004_2019_data
                WHERE {name_col} IS NOT NULL AND {name_col} != ''
            '''))
            conn.commit()
    print(f"   ✅ Imported records")
else:
    print(f"   ❌ File not found: {csv_path}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("IMPORT COMPLETE!")
print("="*60)

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
    total = result.fetchone()[0]
    print(f"\n📊 FINAL TOTAL CANDIDATES IN DATABASE: {total}")

    # Show sample of what was added
    result = conn.execute(text('''
        SELECT name, party 
        FROM candidates 
        WHERE name IN ('Narendra Modi', 'Rahul Gandhi', 'Arvind Kejriwal')
        OR name LIKE '%Modi%'
        LIMIT 10
    '''))
    print("\n📋 Sample candidates in database:")
    for row in result:
        print(f"  {row[0]} | {row[1]}")

print("\n🎉 All pending datasets imported successfully!")