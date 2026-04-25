"""
Import State Legislative Assemblies Data (2013-2017)
Run: python scripts/import_state_assemblies_fixed.py
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
import zipfile

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
print("IMPORTING STATE LEGISLATIVE ASSEMBLIES DATA (2013-2017)")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Find the dataset - look for zip file or extracted folder
data_dir = project_root / 'data'

# Check for zip files
zip_files = list(data_dir.glob('*assembly*.zip')) + list(data_dir.glob('*state*.zip'))
if zip_files:
    print(f"\n📦 Found zip file: {zip_files[0].name}")
    print("   Extracting...")
    with zipfile.ZipFile(zip_files[0], 'r') as zip_ref:
        zip_ref.extractall(data_dir / 'state_assemblies_extracted')
    folder_path = data_dir / 'state_assemblies_extracted'
    print("   ✅ Extracted")
else:
    # Look for extracted folder
    possible_folders = ['state_assemblies_2013_2017', 'state-legislative-assembly-elections-data', 
                        'assembly_elections', 'state_assemblies_extracted']
    folder_path = None
    for folder in possible_folders:
        if (data_dir / folder).exists():
            folder_path = data_dir / folder
            break

if not folder_path:
    print("\n❌ Could not find the dataset. Please:")
    print("1. Extract the ZIP file you downloaded from Kaggle")
    print("\nAvailable files in data/:")
    for item in data_dir.iterdir():
        print(f"  - {item.name}")
    sys.exit(1)

print(f"\n📁 Using folder: {folder_path}")

# Find all CSV files in the folder
csv_files = list(folder_path.glob('*.csv'))
print(f"\n📋 Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f"  - {f.name}")

# ============================================================
# Process each CSV file
# ============================================================
total_candidates_added = 0

for csv_file in csv_files:
    print(f"\n📖 Reading: {csv_file.name}")
    
    try:
        df = pd.read_csv(csv_file, encoding='latin-1')
        print(f"   ✅ Loaded {len(df)} records")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Clean column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Save raw data to database
        table_name = f"state_data_{csv_file.stem.lower()}"
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"   ✅ Saved to '{table_name}' table")
        
        # Try to find candidate name column
        name_col = None
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['candidate', 'cand_name', 'name']):
                name_col = col
                break
        
        if name_col:
            # Extract unique candidates
            candidates_df = df[[name_col]].drop_duplicates()
            candidates_df = candidates_df[candidates_df[name_col].notna()]
            candidates_df = candidates_df[candidates_df[name_col] != '']
            
            print(f"   Found {len(candidates_df)} unique candidates")
            
            # Insert into main candidates table
            with engine.connect() as conn:
                inserted = 0
                for idx, row in candidates_df.iterrows():
                    name = str(row[name_col]).replace("'", "''")[:200]
                    
                    try:
                        conn.execute(
                            text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, 'Unknown', 0)"),
                            {"name": name}
                        )
                        inserted += 1
                        if inserted % 500 == 0:
                            conn.commit()
                            print(f"      Inserted {inserted} candidates...")
                    except Exception as e:
                        pass
                
                conn.commit()
                total_candidates_added += inserted
                print(f"   ✅ Inserted {inserted} candidates from {csv_file.name}")
        else:
            print(f"   ⚠️ No candidate name column found in {csv_file.name}")
            print(f"   Available columns: {list(df.columns)}")
            
    except Exception as e:
        print(f"   ❌ Error processing {csv_file.name}: {e}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("IMPORT COMPLETE!")
print("="*60)

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
    print(f"\n📊 FINAL TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
    print(f"   New candidates added from this import: {total_candidates_added}")

print("\n🎉 Import complete!")