"""
Import Tamil Nadu Assembly Elections 2021
Run: python scripts/import_tamilnadu_final.py
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
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")
    return True

load_env()

# Database connection
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://root:{ENCODED_PASSWORD}@localhost:3306/neta_nexus"

print("="*60)
print("IMPORTING TAMIL NADU ASSEMBLY ELECTIONS 2021")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Path to files
data_dir = project_root / 'data' / 'Tamilnadu_2021_assembly'

# File paths
details_file = data_dir / 'Tamil_Nadu_State_Elections_2021_Details.csv'
constituency_file = data_dir / 'Tamil_Nadu_State_Elections_2021_Constituency_Metadata.csv'
alliance_file = data_dir / 'Tamil_Nadu_State_Elections_2021_Alliance.csv'

# Get Tamil Nadu state ID
with engine.connect() as conn:
    result = conn.execute(text("SELECT id FROM states WHERE code = 'TN'"))
    tn_state = result.fetchone()
    
    if not tn_state:
        conn.execute(text("INSERT INTO states (code, name, capital) VALUES ('TN', 'Tamil Nadu', 'Chennai')"))
        conn.commit()
        result = conn.execute(text("SELECT id FROM states WHERE code = 'TN'"))
        tn_state = result.fetchone()
    
    tn_state_id = tn_state[0]
    print(f"\n🏛️ Tamil Nadu State ID: {tn_state_id}")

total_added = 0

# ============================================================
# FILE 1: Details.csv (Main candidate data)
# ============================================================
print(f"\n📖 Reading: {details_file.name}")
print('-'*40)

try:
    df = pd.read_csv(details_file, encoding='utf-8')
    print(f"   ✅ Loaded {len(df)} records")
    print(f"   📋 Columns: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Find candidate name column
    name_col = None
    for col in df.columns:
        if 'candidate' in col.lower() or 'name' in col.lower():
            name_col = col
            break
    
    # Find party column
    party_col = None
    for col in df.columns:
        if 'party' in col.lower():
            party_col = col
            break
    
    # Find constituency column
    const_col = None
    for col in df.columns:
        if 'constituency' in col.lower():
            const_col = col
            break
    
    print(f"   Using name column: {name_col}")
    print(f"   Using party column: {party_col}")
    
    if name_col:
        # Get unique candidates
        unique_candidates = df[name_col].dropna().unique()
        unique_candidates = [str(c).strip() for c in unique_candidates if str(c).strip()]
        
        print(f"   Found {len(unique_candidates)} unique candidates")
        
        # Insert into database
        with engine.connect() as conn:
            inserted = 0
            for name in unique_candidates:
                name_clean = name.replace("'", "''")[:200]
                
                # Get party if available
                party = 'Unknown'
                if party_col:
                    party_row = df[df[name_col] == name]
                    if len(party_row) > 0:
                        party = str(party_row.iloc[0][party_col])[:100] if pd.notna(party_row.iloc[0][party_col]) else 'Unknown'
                        party = party.replace("'", "''")
                
                try:
                    conn.execute(
                        text("INSERT IGNORE INTO candidates (name, party, state_id, is_current) VALUES (:name, :party, :state_id, 1)"),
                        {"name": name_clean, "party": party, "state_id": tn_state_id}
                    )
                    inserted += 1
                    if inserted % 500 == 0:
                        conn.commit()
                        print(f"      Inserted {inserted} candidates...")
                except Exception as e:
                    pass
            
            conn.commit()
            total_added += inserted
            print(f"   ✅ Inserted {inserted} candidates")
            
            # Save raw data to database
            df.to_sql('tn_2021_details', engine, if_exists='replace', index=False)
            print(f"   ✅ Saved raw data to 'tn_2021_details' table")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================
# FILE 2: Constituency Metadata
# ============================================================
print(f"\n📖 Reading: {constituency_file.name}")
print('-'*40)

try:
    df_const = pd.read_csv(constituency_file, encoding='utf-8')
    print(f"   ✅ Loaded {len(df_const)} records")
    print(f"   📋 Columns: {list(df_const.columns)}")
    
    # Save to database
    df_const.to_sql('tn_2021_constituencies', engine, if_exists='replace', index=False)
    print(f"   ✅ Saved to 'tn_2021_constituencies' table")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================
# FILE 3: Alliance Data
# ============================================================
print(f"\n📖 Reading: {alliance_file.name}")
print('-'*40)

try:
    df_alliance = pd.read_csv(alliance_file, encoding='utf-8')
    print(f"   ✅ Loaded {len(df_alliance)} records")
    print(f"   📋 Columns: {list(df_alliance.columns)}")
    
    # Save to database
    df_alliance.to_sql('tn_2021_alliances', engine, if_exists='replace', index=False)
    print(f"   ✅ Saved to 'tn_2021_alliances' table")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("IMPORT COMPLETE!")
print("="*60)

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM candidates"))
    print(f"\n📊 TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
    print(f"   New candidates added from Tamil Nadu: {total_added}")

print("\n🎉 Import complete!")