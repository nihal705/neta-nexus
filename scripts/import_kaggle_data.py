"""
Import Kaggle election data to MySQL
Run: python scripts/import_kaggle_data.py
"""

import pandas as pd
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Database connection
DATABASE_URL = 'mysql+pymysql://root:Nihal%40786313@localhost:3306/neta_nexus'
engine = create_engine(DATABASE_URL)

# Read the CSV
csv_path = project_root / 'data' / 'election_2024.csv'

if not csv_path.exists():
    print(f"❌ File not found: {csv_path}")
    print("Please save the CSV to data/election_2024.csv")
    sys.exit(1)

print(f"📖 Reading: {csv_path}")
df = pd.read_csv(csv_path, encoding='latin-1')

print(f"✅ Loaded {len(df)} rows")
print(f"📊 Columns: {list(df.columns)}")

# Clean column names (remove spaces, special characters)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

print(f"\n📋 Cleaned columns: {list(df.columns)}")

# Map common column names to our schema
column_mapping = {
    'candidate': 'name',
    'candidate_name': 'name',
    'constituency_name': 'constituency',
    'constituency': 'constituency',
    'party_name': 'party',
    'party_symbol': 'party_symbol',
    'votes': 'votes',
    'vote_share': 'vote_percentage',
    'vote_percentage': 'vote_percentage',
    'winner': 'winner',
    'margin': 'margin',
    'state_name': 'state',
    'state': 'state',
}

# Check what columns we have
available_columns = {}
for kaggle_col, our_col in column_mapping.items():
    if kaggle_col in df.columns:
        available_columns[kaggle_col] = our_col
        print(f"  ✓ Found: {kaggle_col} -> {our_col}")

if not available_columns:
    print("\n❌ No matching columns found. Your CSV has:")
    for col in df.columns:
        print(f"  - {col}")
    print("\nPlease update the column_mapping in this script")
    sys.exit(1)

# Create a new dataframe with mapped columns
new_df = pd.DataFrame()

for kaggle_col, our_col in available_columns.items():
    new_df[our_col] = df[kaggle_col]

# Add year if not present
if 'year' not in new_df.columns and 'election_year' not in df.columns:
    new_df['year'] = 2024

print(f"\n✅ Prepared {len(new_df)} records for import")
print(f"📋 Output columns: {list(new_df.columns)}")

# Import to database
print("\n📤 Importing to MySQL...")
new_df.to_sql('election_2024_data', engine, if_exists='replace', index=False)

print(f"✅ Imported {len(new_df)} rows to 'election_2024_data' table")

# Verify
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM election_2024_data"))
    count = result.fetchone()[0]
    print(f"\n✓ Verification: {count} rows in database")

    # Show sample
    result = conn.execute(text("SELECT * FROM election_2024_data LIMIT 3"))
    print("\n📊 Sample data:")
    for row in result:
        print(f"  {row}")

print("\n🎉 IMPORT COMPLETE!")

