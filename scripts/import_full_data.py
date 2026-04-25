#!/usr/bin/env python3
"""
Complete data import script for NetaNexus
Imports candidates and their affidavit details
"""

import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import engine, SessionLocal
from backend.models import Candidate, State, Constituency, Affidavit

def import_full_candidate_data():
    """Import all candidate data with affidavit details"""
    
    print("=" * 60)
    print("NetaNexus - Complete Data Import")
    print("=" * 60)
    
    db = SessionLocal()
    
    # Get or create default state
    state = db.query(State).first()
    if not state:
        state = State(code="DL", name="Delhi", capital="New Delhi")
        db.add(state)
        db.commit()
        print("✅ Created default state")
    
    # Path to data files
    data_dir = project_root / "data" / "india-election-data" / "affidavits"
    
    # Import main candidate files
    files = [
        ("myneta.2014.csv", 2014, "LOK_SABHA"),
        ("myneta.2009.csv", 2009, "LOK_SABHA"),
        ("myneta.2004.csv", 2004, "LOK_SABHA"),
    ]
    
    total_candidates = 0
    
    for filename, year, election_type in files:
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"⚠️ File not found: {filename}")
            continue
        
        print(f"\n📁 Importing {filename}...")
        df = pd.read_csv(filepath)
        print(f"   Records: {len(df)}")
        
        # Map columns
        name_col = 'Candidate' if 'Candidate' in df.columns else 'candidate_name'
        party_col = 'Party' if 'Party' in df.columns else 'party_name'
        const_col = 'Constituency' if 'Constituency' in df.columns else 'constituency_name'
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                name = str(row.get(name_col, ''))[:200]
                if name and name != 'nan' and len(name) > 2:
                    
                    # Check if candidate exists
                    existing = db.query(Candidate).filter(
                        Candidate.name == name,
                        Candidate.election_year == year
                    ).first()
                    
                    if not existing:
                        candidate = Candidate(
                            name=name,
                            party=str(row.get(party_col, 'Unknown'))[:100],
                            constituency_name=str(row.get(const_col, ''))[:100],
                            state_id=state.id,
                            election_year=year,
                            election_type=election_type,
                            is_current=(year == 2024)
                        )
                        db.add(candidate)
                        imported += 1
                        
                        if imported % 100 == 0:
                            db.commit()
                            print(f"   Imported {imported} candidates...")
                
            except Exception as e:
                continue
        
        db.commit()
        total_candidates += imported
        print(f"   ✅ Imported {imported} candidates from {filename}")
    
    # Import affidavit details
    print("\n📁 Importing affidavit details...")
    affidavit_file = data_dir / "myneta.details.2014.csv"
    
    if affidavit_file.exists():
        df_details = pd.read_csv(affidavit_file)
        print(f"   Records: {len(df_details)}")
        
        # Pivot the data
        pivoted = df_details.pivot_table(
            index='ID', 
            columns='Key', 
            values='Value', 
            aggfunc='first'
        ).reset_index()
        
        affidavits_added = 0
        for idx, row in pivoted.iterrows():
            candidate_name = row.get('candidate_name', '')
            if candidate_name and candidate_name != 'nan':
                # Find matching candidate
                candidate = db.query(Candidate).filter(
                    Candidate.name.ilike(f'%{candidate_name[:50]}%')
                ).first()
                
                if candidate and not candidate.affidavit:
                    affidavit = Affidavit(
                        candidate_id=candidate.id,
                        total_assets=str(row.get('total_assets', ''))[:50],
                        movable_assets=str(row.get('movable_assets', ''))[:50],
                        immovable_assets=str(row.get('immovable_assets', ''))[:50],
                        total_liabilities=str(row.get('total_liabilities', ''))[:50],
                        annual_income=str(row.get('annual_income', ''))[:50],
                        education_details=str(row.get('education', ''))[:500],
                        profession_details=str(row.get('profession', ''))[:500],
                        filed_on=2024
                    )
                    db.add(affidavit)
                    affidavits_added += 1
                    
                    if affidavits_added % 50 == 0:
                        db.commit()
                        print(f"   Added {affidavits_added} affidavits...")
        
        db.commit()
        print(f"   ✅ Added {affidavits_added} affidavits")
    
    # Final summary
    final_count = db.query(Candidate).count()
    affidavit_count = db.query(Affidavit).count()
    
    print("\n" + "=" * 60)
    print("✅ IMPORT COMPLETE!")
    print(f"📊 Total Candidates: {final_count}")
    print(f"📋 Total Affidavits: {affidavit_count}")
    print("=" * 60)
    
    db.close()

if __name__ == "__main__":
    import_full_candidate_data()