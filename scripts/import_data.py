"""
Simple script to import candidate data from CSV files
Run this from project root: python scripts/import_data.py
"""

import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import database modules
from backend.database import engine, SessionLocal
from backend.models import Candidate, State, Constituency

def import_candidates():
    """Import candidate data from CSV files"""
    
    print("=" * 50)
    print("Importing Candidate Data")
    print("=" * 50)
    
    # Path to CSV files
    csv_path = project_root / "data" / "india-election-data" / "affidavits"
    
    # Files to import (ordered by year)
    files = [
        ("myneta.2014.csv", 2014),
        ("myneta.2009.csv", 2009),
        ("myneta.2004.csv", 2004),
    ]
    
    db = SessionLocal()
    
    # First, ensure we have at least one state
    state = db.query(State).first()
    if not state:
        state = State(code="DL", name="Delhi", capital="New Delhi")
        db.add(state)
        db.commit()
        print("✅ Created default state: Delhi")
    
    total_imported = 0
    
    for filename, year in files:
        filepath = csv_path / filename
        if not filepath.exists():
            print(f"⚠️ File not found: {filename}")
            continue
        
        print(f"\n📁 Importing {filename} ({year})...")
        
        try:
            df = pd.read_csv(filepath)
            print(f"   Rows found: {len(df)}")
            
            # Look for candidate name column
            name_col = None
            for col in df.columns:
                if 'candidate' in col.lower() or 'name' in col.lower():
                    name_col = col
                    break
            
            if name_col:
                print(f"   Using column: {name_col}")
                
                # Import first 100 candidates (to avoid overwhelming the database)
                imported = 0
                for idx, row in df.head(100).iterrows():
                    try:
                        candidate_name = str(row[name_col])[:200]
                        if candidate_name and candidate_name != 'nan':
                            # Check if candidate already exists
                            existing = db.query(Candidate).filter(
                                Candidate.name == candidate_name,
                                Candidate.party == str(row.get('party', ''))[:100]
                            ).first()
                            
                            if not existing:
                                candidate = Candidate(
                                    name=candidate_name,
                                    party=str(row.get('party', 'Unknown'))[:100],
                                    state_id=state.id,
                                    is_current=(year == 2014)
                                )
                                db.add(candidate)
                                imported += 1
                    
                    except Exception as e:
                        continue
                    
                    # Commit every 50 records
                    if imported % 50 == 0:
                        db.commit()
                        print(f"   Imported {imported} candidates so far...")
                
                db.commit()
                total_imported += imported
                print(f"   ✅ Imported {imported} candidates from {filename}")
            else:
                print(f"   ⚠️ No candidate name column found in {filename}")
                print(f"   Columns available: {list(df.columns)[:10]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Show summary
    candidate_count = db.query(Candidate).count()
    print(f"\n" + "=" * 50)
    print(f"✅ Import Complete!")
    print(f"📊 Total candidates in database: {candidate_count}")
    print("=" * 50)
    
    db.close()

if __name__ == "__main__":
    import_candidates()