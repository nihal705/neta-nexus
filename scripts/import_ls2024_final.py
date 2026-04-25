"""
Import Complete Lok Sabha 2024 ECI Data - Final Working Version
Run: python scripts/import_ls2024_final.py
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
    
    # Get unique candidates
    candidates_df = df[['candidate', 'party']].drop_duplicates()
    candidates_df = candidates_df[candidates_df['candidate'].notna()]
    candidates_df = candidates_df[candidates_df['candidate'] != '']
    
    print(f"Found {len(candidates_df)} unique candidates")
    
    # Insert candidates using a loop with proper escaping
    with engine.connect() as conn:
        inserted = 0
        for idx, row in candidates_df.iterrows():
            name = row['candidate']
            # Escape single quotes in name
            name = name.replace("'", "''")
            
            party = row['party'] if pd.notna(row['party']) else 'Unknown'
            party = party.replace("'", "''")
            
            try:
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, is_current) VALUES (:name, :party, 1)"),
                    {"name": name, "party": party}
                )
                inserted += 1
                if inserted % 500 == 0:
                    conn.commit()
                    print(f"   Inserted {inserted} candidates...")
            except Exception as e:
                print(f"   Error inserting {name}: {e}")
        
        conn.commit()
        print(f"✅ Inserted {inserted} new candidates")
    
    # Show final count
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM candidates'))
        print(f"\n📊 TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
else:
    print(f"\n❌ File not found: {csv_file}")

print("\n🎉 Import complete!")