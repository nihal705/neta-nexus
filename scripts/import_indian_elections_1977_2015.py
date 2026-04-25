"""
Import Indian Election Dataset (1977-2015)
Run: python scripts/import_indian_elections_1977_2015.py
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
print("IMPORTING INDIAN ELECTION DATASET (1977-2015)")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Find all CSV files in the dataset folder
data_dir = project_root / 'data'
csv_files = glob.glob(str(data_dir / '**/*.csv'), recursive=True)

print(f"\n📁 Found {len(csv_files)} CSV files")

# Try to find the main election results file
main_file = None
for f in csv_files:
    if 'election' in f.lower() or 'results' in f.lower() or 'candidate' in f.lower():
        if '1977' in f or '2015' in f or 'all' in f:
            main_file = f
            break

if main_file:
    print(f"\n📖 Reading main file: {main_file}")
    df = pd.read_csv(main_file, encoding='latin-1')
    print(f"✅ Loaded {len(df)} records")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Import to database
    df.to_sql('elections_1977_2015', engine, if_exists='replace', index=False)
    print(f"✅ Imported to 'elections_1977_2015' table")
    
    # Find candidate name column
    name_col = None
    for col in df.columns:
        if any(name in col for name in ['candidate', 'name', 'cand_name', 'winner']):
            name_col = col
            break
    
    # Find party column
    party_col = None
    for col in df.columns:
        if 'party' in col:
            party_col = col
            break
    
    if name_col:
        with engine.connect() as conn:
            conn.execute(text(f'''
                INSERT IGNORE INTO candidates (name, party, is_current)
                SELECT DISTINCT {name_col}, {party_col if party_col else "'Unknown'"}, 0
                FROM elections_1977_2015
                WHERE {name_col} IS NOT NULL AND {name_col} != ''
            '''))
            conn.commit()
            print(f"✅ Added candidates to main table")
    
    # Show final count
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
        print(f"\n📊 Total candidates in database: {result.fetchone()[0]}")
else:
    print("\n❌ No main file found. Please check the extracted folder structure.")
    print("Files found:")
    for f in csv_files:
        print(f"  - {f}")