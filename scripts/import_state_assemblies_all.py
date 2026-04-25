"""
Import ALL State Legislative Assemblies Data (2013-2017)
Extracts every candidate record, not just unique names
Run: python scripts/import_state_assemblies_all.py
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
print("IMPORTING ALL STATE LEGISLATIVE ASSEMBLIES DATA (2013-2017)")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Find the dataset folder
data_dir = project_root / 'data'
folder_path = data_dir / 'state_assemblies_2013_2017'

if not folder_path.exists():
    print(f"\n❌ Folder not found: {folder_path}")
    sys.exit(1)

print(f"\n📁 Using folder: {folder_path}")

# Find the Candidate CSV file
candidate_file = None
for file in folder_path.glob('*.csv'):
    if 'Candidate' in file.name:
        candidate_file = file
        break

if candidate_file:
    print(f"\n📖 Reading: {candidate_file.name}")
    df = pd.read_csv(candidate_file, encoding='latin-1')
    print(f"   ✅ Loaded {len(df)} records")
    print(f"   📋 Columns: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.upper()
    
    # Find candidate name column
    name_col = 'CAND_NAME'
    if name_col not in df.columns:
        for col in df.columns:
            if 'CAND' in col and 'NAME' in col:
                name_col = col
                break
    
    # Find party column
    party_col = 'PARTYABBRE'
    if party_col not in df.columns:
        for col in df.columns:
            if 'PARTY' in col:
                party_col = col
                break
    
    # Find constituency column
    const_col = 'AC_NAME'
    if const_col not in df.columns:
        for col in df.columns:
            if 'AC' in col or 'CONST' in col:
                const_col = col
                break
    
    # Find state column
    state_col = 'ST_NAME'
    if state_col not in df.columns:
        for col in df.columns:
            if 'STATE' in col or 'ST_' in col:
                state_col = col
                break
    
    print(f"\n   Using columns:")
    print(f"      Candidate: {name_col}")
    print(f"      Party: {party_col}")
    print(f"      Constituency: {const_col}")
    print(f"      State: {state_col}")
    
    # Get ALL candidates (not just unique)
    all_candidates = df[[name_col, party_col, const_col, state_col]].copy()
    all_candidates = all_candidates[all_candidates[name_col].notna()]
    all_candidates = all_candidates[all_candidates[name_col] != '']
    
    print(f"\n   Found {len(all_candidates)} candidate records")
    
    # Insert ALL candidates into database
    with engine.connect() as conn:
        inserted = 0
        skipped = 0
        
        for idx, row in all_candidates.iterrows():
            name = str(row[name_col]).replace("'", "''")[:200]
            party = str(row[party_col])[:100] if pd.notna(row[party_col]) else 'Unknown'
            party = party.replace("'", "''")
            
            try:
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, :party, 0)"),
                    {"name": name, "party": party}
                )
                inserted += 1
                
                if inserted % 2000 == 0:
                    conn.commit()
                    print(f"      Inserted {inserted} candidates...")
                    
            except Exception as e:
                skipped += 1
        
        conn.commit()
        print(f"\n   ✅ Inserted {inserted} new candidates")
        print(f"   ⚠️ Skipped {skipped} duplicates")
        
    # Also save full table for reference
    df.to_sql('state_assemblies_candidates_full', engine, if_exists='replace', index=False)
    print(f"\n   ✅ Saved full dataset to 'state_assemblies_candidates_full' table")
    
else:
    print(f"\n❌ Candidate CSV file not found in {folder_path}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("IMPORT COMPLETE!")
print("="*60)

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
    print(f"\n📊 FINAL TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")

print("\n🎉 Import complete!")