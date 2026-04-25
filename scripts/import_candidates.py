#!/usr/bin/env python3
"""
Import candidate data from CSV files to PostgreSQL
"""

import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/neta_nexus")
DATA_DIR = Path(__file__).parent.parent / "data"

def clean_numeric(value):
    """Clean numeric values from strings"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        cleaned = str(value).replace('₹', '').replace(',', '').strip()
        return float(cleaned) if cleaned else None
    except:
        return None

def import_adr_2014():
    """Import ADR 2014 data"""
    print("\n📊 Importing ADR 2014 data...")
    
    filepath = DATA_DIR / "adr_2014.csv"
    if not filepath.exists():
        print(f"⚠️ File not found: {filepath}")
        return 0
    
    df = pd.read_csv(filepath)
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Map to our schema
    df['name'] = df.get('candidate_name', df.get('name', ''))
    df['party'] = df.get('party_name', df.get('party', ''))
    df['constituency'] = df.get('constituency_name', df.get('constituency', ''))
    df['state'] = df.get('state_name', df.get('state', ''))
    df['age'] = df.get('age', None)
    df['education'] = df.get('education', '')
    df['gender'] = df.get('gender', '')
    
    # Remove rows with no name
    df = df[df['name'].notna() & (df['name'] != '')]
    
    print(f"   Found {len(df)} valid candidates")
    
    # Connect to database
    engine = create_engine(DATABASE_URL)
    
    # Insert in batches
    batch_size = 1000
    total_imported = 0
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        batch.to_sql('candidates_temp', engine, if_exists='replace', index=False)
        total_imported += len(batch)
        print(f"   Imported batch {i//batch_size + 1} ({total_imported} total)")
    
    print(f"✅ Imported {total_imported} candidates from ADR 2014")
    return total_imported

def create_mock_data():
    """Create mock data for demonstration"""
    print("\n📊 Creating mock data...")
    
    engine = create_engine(DATABASE_URL)
    
    # States
    states_data = [
        {"code": "UP", "name": "Uttar Pradesh", "capital": "Lucknow"},
        {"code": "MH", "name": "Maharashtra", "capital": "Mumbai"},
        {"code": "DL", "name": "Delhi", "capital": "New Delhi"},
        {"code": "WB", "name": "West Bengal", "capital": "Kolkata"},
        {"code": "TN", "name": "Tamil Nadu", "capital": "Chennai"},
        {"code": "KA", "name": "Karnataka", "capital": "Bangalore"},
        {"code": "GJ", "name": "Gujarat", "capital": "Gandhinagar"},
        {"code": "BI", "name": "Bihar", "capital": "Patna"},
    ]
    
    pd.DataFrame(states_data).to_sql('states', engine, if_exists='append', index=False)
    print(f"   ✅ Added {len(states_data)} states")
    
    # Constituencies
    constituencies_data = []
    for i in range(1, 544):
        constituencies_data.append({
            "name": f"Constituency {i}",
            "type": "PARLIAMENTARY",
            "state_id": (i % 8) + 1,
            "district": f"District {(i % 50) + 1}"
        })
    
    pd.DataFrame(constituencies_data).to_sql('constituencies', engine, if_exists='append', index=False)
    print(f"   ✅ Added {len(constituencies_data)} constituencies")
    
    return len(constituencies_data)

def main():
    print("=" * 50)
    print("📥 Importing Candidate Data to PostgreSQL")
    print("=" * 50)
    
    # Check database connection
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("✅ Database connected")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and DATABASE_URL is correct")
        return
    
    # Import data
    total_candidates = import_adr_2014()
    
    if total_candidates == 0:
        print("\n⚠️ No ADR data found. Creating mock data instead...")
        create_mock_data()
    
    print("\n" + "=" * 50)
    print("🎉 Import complete!")
    print("=" * 50)
    
    print("\n📌 Next steps:")
    print("1. Start the application: npm run dev")
    print("2. Visit: http://localhost:3000")

if __name__ == "__main__":
    main()