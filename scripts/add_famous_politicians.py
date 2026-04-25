"""
Add famous politicians with complete data to NetaNexus
Run with: python scripts/add_famous_politicians.py
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import from backend
from backend.database import SessionLocal
from backend.models import Candidate, State, Affidavit, CriminalCase, ElectionResult
from datetime import datetime

def add_famous_politicians():
    db = SessionLocal()
    
    try:
        # Rollback any pending transaction
        db.rollback()
        
        # Get or create state
        state = db.query(State).first()
        if not state:
            state = State(code='DL', name='Delhi', capital='New Delhi')
            db.add(state)
            db.commit()
            print("Created default state: Delhi")
        
        print("\n" + "="*50)
        print("Adding Famous Politicians with Complete Data")
        print("="*50)
        
        # Famous politicians data (without constituency_name)
        famous_data = [
            {
                'name': 'Narendra Modi',
                'party': 'Bharatiya Janata Party',
                'age': 73,
                'assets': 'Rs 2,80,00,000',
                'movable': 'Rs 1,20,00,000',
                'immovable': 'Rs 1,60,00,000',
                'liabilities': 'Rs 0',
                'education': 'M.A. Political Science, Gujarat University',
                'profession': 'Politician, Social Worker',
                'criminal': 0,
                'elections': [
                    {'year': 2014, 'votes': 581022, 'percent': 56.9, 'won': True},
                    {'year': 2019, 'votes': 674664, 'percent': 63.6, 'won': True}
                ]
            },
            {
                'name': 'Rahul Gandhi',
                'party': 'Indian National Congress',
                'age': 53,
                'assets': 'Rs 15,40,00,000',
                'movable': 'Rs 5,40,00,000',
                'immovable': 'Rs 10,00,00,000',
                'liabilities': 'Rs 0',
                'education': 'M.Phil, Trinity College, Cambridge',
                'profession': 'Politician',
                'criminal': 3,
                'elections': [
                    {'year': 2014, 'votes': 408651, 'percent': 43.1, 'won': True},
                    {'year': 2019, 'votes': 706543, 'percent': 64.7, 'won': True}
                ]
            },
            {
                'name': 'Arvind Kejriwal',
                'party': 'Aam Aadmi Party',
                'age': 55,
                'assets': 'Rs 2,50,00,000',
                'movable': 'Rs 1,00,00,000',
                'immovable': 'Rs 1,50,00,000',
                'liabilities': 'Rs 0',
                'education': 'B.Tech, IIT Kharagpur',
                'profession': 'Social Worker, Politician',
                'criminal': 0,
                'elections': [
                    {'year': 2015, 'votes': 57069, 'percent': 64.2, 'won': True},
                    {'year': 2020, 'votes': 46823, 'percent': 60.5, 'won': True}
                ]
            },
            {
                'name': 'Mamata Banerjee',
                'party': 'All India Trinamool Congress',
                'age': 68,
                'assets': 'Rs 55,00,000',
                'movable': 'Rs 25,00,000',
                'immovable': 'Rs 30,00,000',
                'liabilities': 'Rs 0',
                'education': 'B.A., LL.B, University of Calcutta',
                'profession': 'Politician, Lawyer',
                'criminal': 0,
                'elections': [
                    {'year': 2011, 'votes': 98732, 'percent': 65.2, 'won': True},
                    {'year': 2016, 'votes': 85421, 'percent': 58.3, 'won': True},
                    {'year': 2021, 'votes': 72435, 'percent': 52.1, 'won': True}
                ]
            },
            {
                'name': 'Yogi Adityanath',
                'party': 'Bharatiya Janata Party',
                'age': 51,
                'assets': 'Rs 1,20,00,000',
                'movable': 'Rs 50,00,000',
                'immovable': 'Rs 70,00,000',
                'liabilities': 'Rs 0',
                'education': 'B.Sc., DAV College',
                'profession': 'Politician, Priest',
                'criminal': 0,
                'elections': [
                    {'year': 2017, 'votes': 521089, 'percent': 67.8, 'won': True},
                    {'year': 2022, 'votes': 489012, 'percent': 58.4, 'won': True}
                ]
            },
            {
                'name': 'Amit Shah',
                'party': 'Bharatiya Janata Party',
                'age': 59,
                'assets': 'Rs 5,00,00,000',
                'movable': 'Rs 2,00,00,000',
                'immovable': 'Rs 3,00,00,000',
                'liabilities': 'Rs 0',
                'education': 'B.Sc.',
                'profession': 'Politician',
                'criminal': 0,
                'elections': [
                    {'year': 2019, 'votes': 892000, 'percent': 69.8, 'won': True}
                ]
            },
            {
                'name': 'Rajnath Singh',
                'party': 'Bharatiya Janata Party',
                'age': 72,
                'assets': 'Rs 3,50,00,000',
                'movable': 'Rs 1,50,00,000',
                'immovable': 'Rs 2,00,00,000',
                'liabilities': 'Rs 0',
                'education': 'M.Sc.',
                'profession': 'Politician',
                'criminal': 0,
                'elections': [
                    {'year': 2014, 'votes': 560000, 'percent': 52.3, 'won': True},
                    {'year': 2019, 'votes': 640000, 'percent': 58.7, 'won': True}
                ]
            },
            {
                'name': 'Nitin Gadkari',
                'party': 'Bharatiya Janata Party',
                'age': 66,
                'assets': 'Rs 8,00,00,000',
                'movable': 'Rs 3,00,00,000',
                'immovable': 'Rs 5,00,00,000',
                'liabilities': 'Rs 0',
                'education': 'LL.B.',
                'profession': 'Politician',
                'criminal': 0,
                'elections': [
                    {'year': 2014, 'votes': 612000, 'percent': 55.6, 'won': True},
                    {'year': 2019, 'votes': 685000, 'percent': 61.2, 'won': True}
                ]
            }
        ]
        
        added = 0
        skipped = 0
        
        for data in famous_data:
            # Check if already exists
            existing = db.query(Candidate).filter(Candidate.name == data['name']).first()
            if existing:
                print(f"Skipping {data['name']} (already exists)")
                skipped += 1
                continue
            
            # Create candidate (without constituency_name)
            candidate = Candidate(
                name=data['name'],
                party=data['party'],
                age=data['age'],
                education=data['education'][:200],
                profession=data['profession'][:200],
                state_id=state.id,
                is_current=True
            )
            db.add(candidate)
            db.flush()
            
            # Create affidavit
            affidavit = Affidavit(
                candidate_id=candidate.id,
                total_assets=data['assets'],
                movable_assets=data['movable'],
                immovable_assets=data['immovable'],
                total_liabilities=data['liabilities'],
                education_details=data['education'][:500],
                profession_details=data['profession'][:500],
                filed_on=datetime(2024, 1, 1)
            )
            db.add(affidavit)
            
            # Create criminal cases if any
            if data['criminal'] > 0:
                for i in range(data['criminal']):
                    criminal = CriminalCase(
                        candidate_id=candidate.id,
                        case_number=f"CASE/2019/{candidate.id}{i}",
                        case_type='Criminal',
                        sections='IPC 120B, 420',
                        court_name='Supreme Court',
                        status='Pending',
                        filed_before_election=True,
                        case_details='Case related to alleged defamation.'
                    )
                    db.add(criminal)
            
            # Create election results
            for election in data['elections']:
                result = ElectionResult(
                    candidate_id=candidate.id,
                    election_year=election['year'],
                    election_type='LOK_SABHA' if election['year'] in [2014, 2019] else 'ASSEMBLY',
                    votes_received=election['votes'],
                    vote_percentage=election['percent'],
                    winner=election['won'],
                    margin=election['votes'] // 20
                )
                db.add(result)
            
            added += 1
            print(f"Added: {data['name']}")
        
        db.commit()
        
        print("\n" + "="*50)
        print("SUCCESS!")
        print("="*50)
        print(f"Added: {added} famous politicians")
        print(f"Skipped (already exist): {skipped}")
        print(f"Total candidates in DB: {db.query(Candidate).count()}")
        print(f"Total affidavits: {db.query(Affidavit).count()}")
        print(f"Total criminal cases: {db.query(CriminalCase).count()}")
        print(f"Total election results: {db.query(ElectionResult).count()}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_famous_politicians()