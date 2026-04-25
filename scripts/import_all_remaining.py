"""
Import all remaining Kaggle datasets
Run: python scripts/import_all_remaining.py
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
print("IMPORTING ALL REMAINING KAGGLE DATASETS")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)


# ============================================================
# DATASET 1: Lok Sabha 2014
# ============================================================
print("\n📁 Dataset 1: Lok Sabha 2014")
csv_file = project_root / 'data' / 'loksabha_2014.csv'

if csv_file.exists():
    df = pd.read_csv(csv_file, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} records")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Find candidate column
    name_col = None
    for col in df.columns:
        if 'candidate' in col or 'name' in col:
            name_col = col
            break
    
    if name_col:
        candidates = df[[name_col]].drop_duplicates()
        candidates = candidates[candidates[name_col].notna()]
        candidates = candidates[candidates[name_col] != '']
        
        with engine.connect() as conn:
            inserted = 0
            for _, row in candidates.iterrows():
                name = row[name_col].replace("'", "''")
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, 'Unknown', 0)"),
                    {"name": name}
                )
                inserted += 1
                if inserted % 500 == 0:
                    conn.commit()
                    print(f"      Inserted {inserted} candidates...")
            conn.commit()
        print(f"   ✅ Added {inserted} candidates from LS 2014")
else:
    print(f"   ❌ File not found: {csv_file}")


# ============================================================
# DATASET 2: Lok Sabha 2009
# ============================================================
print("\n📁 Dataset 2: Lok Sabha 2009")
csv_file = project_root / 'data' / 'loksabha_2009.csv'

if csv_file.exists():
    df = pd.read_csv(csv_file, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} records")
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    name_col = None
    for col in df.columns:
        if 'candidate' in col or 'name' in col:
            name_col = col
            break
    
    if name_col:
        candidates = df[[name_col]].drop_duplicates()
        candidates = candidates[candidates[name_col].notna()]
        candidates = candidates[candidates[name_col] != '']
        
        with engine.connect() as conn:
            inserted = 0
            for _, row in candidates.iterrows():
                name = row[name_col].replace("'", "''")
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, 'Unknown', 0)"),
                    {"name": name}
                )
                inserted += 1
                if inserted % 500 == 0:
                    conn.commit()
            conn.commit()
        print(f"   ✅ Added {inserted} candidates from LS 2009")
else:
    print(f"   ❌ File not found: {csv_file}")


# ============================================================
# DATASET 3: State Legislative Assemblies (2013-2017)
# ============================================================
print("\n📁 Dataset 3: State Legislative Assemblies")
csv_file = project_root / 'data' / 'state_assemblies_2013_2017.csv'

if csv_file.exists():
    df = pd.read_csv(csv_file, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} records")
    print(f"   📋 Columns: {list(df.columns)}")
    
    df.to_sql('state_assemblies_raw', engine, if_exists='replace', index=False)
    
    # Find candidate column
    name_col = None
    for col in df.columns:
        if 'candidate' in col.lower():
            name_col = col
            break
    
    if name_col:
        candidates = df[[name_col]].drop_duplicates()
        candidates = candidates[candidates[name_col].notna()]
        candidates = candidates[candidates[name_col] != '']
        
        with engine.connect() as conn:
            inserted = 0
            for _, row in candidates.iterrows():
                name = row[name_col].replace("'", "''")
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, 'Unknown', 0)"),
                    {"name": name}
                )
                inserted += 1
                if inserted % 1000 == 0:
                    conn.commit()
                    print(f"      Inserted {inserted} candidates...")
            conn.commit()
        print(f"   ✅ Added {inserted} candidates from State Assemblies")
else:
    print(f"   ❌ File not found: {csv_file}")


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("IMPORT COMPLETE!")
print("="*60)

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
    print(f"\n📊 FINAL TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
    
    # Show breakdown
    result = conn.execute(text('SELECT COUNT(*) FROM candidates WHERE is_current = 1'))
    print(f"   Current representatives: {result.fetchone()[0]}")
    
    result = conn.execute(text('SELECT COUNT(DISTINCT party) FROM candidates WHERE party IS NOT NULL'))
    print(f"   Unique political parties: {result.fetchone()[0]}")

print("\n🎉 Import complete!")