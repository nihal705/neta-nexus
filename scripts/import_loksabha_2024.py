"""
Import Lok Sabha 2024 Full Data
Run: python scripts/import_loksabha_2024.py
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

print(f"🔗 Connecting to database...")

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

# Read CSV
csv_path = project_root / 'data' / 'loksabha_2024_full.csv'

if not csv_path.exists():
    print(f"❌ File not found: {csv_path}")
    print("Please download from Kaggle and save to data/loksabha_2024_full.csv")
    sys.exit(1)

print(f"📖 Reading {csv_path}")
df = pd.read_csv(csv_path, encoding='latin-1')
print(f"✅ Loaded {len(df)} candidates")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(f"📋 Columns: {list(df.columns)}")

# Import to database
df.to_sql('loksabha_2024_full', engine, if_exists='replace', index=False)
print(f"✅ Imported to 'loksabha_2024_full' table")

# Merge into main candidates table
with engine.connect() as conn:
    # Add constituencies (using correct column name 'constituency')
    conn.execute(text('''
        INSERT IGNORE INTO constituencies (name, type)
        SELECT DISTINCT constituency, 'PARLIAMENTARY'
        FROM loksabha_2024_full
        WHERE constituency IS NOT NULL
    '''))
    conn.commit()
    print("✅ Constituencies added")
    
    # Add candidates with constituency_id
    conn.execute(text('''
        INSERT IGNORE INTO candidates (name, party, constituency_id, is_current)
        SELECT 
            l.candidate,
            l.party,
            c.id,
            1
        FROM loksabha_2024_full l
        JOIN constituencies c ON c.name = l.constituency
        WHERE l.candidate IS NOT NULL
    '''))
    conn.commit()
    print("✅ Candidates merged into main table")
    
    # Show final count
    result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
    print(f"\n📊 Total candidates in database: {result.fetchone()[0]}")
    
    # Show sample from Varanasi
    result = conn.execute(text('''
        SELECT c.name, c.party, const.name
        FROM candidates c
        JOIN constituencies const ON c.constituency_id = const.id
        WHERE const.name = 'Varanasi'
        LIMIT 5
    '''))
    print("\n📋 Candidates from Varanasi constituency:")
    for row in result:
        print(f"  {row[0]} | {row[1]} | {row[2]}")

print("\n🎉 Import complete!")