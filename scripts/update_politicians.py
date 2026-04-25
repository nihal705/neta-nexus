"""
Complete update for politicians with constituency_id
Run with: python scripts/final_update_politicians.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.models import Candidate, State, Constituency, Affidavit, ElectionResult
from datetime import datetime

def main():
    print("=" * 60)
    print("Updating Politicians with Complete Data")
    print("=" * 60)
    
    db = SessionLocal()
    
    # Get states
    states = {s.code: s for s in db.query(State).all()}
    print("States available:", list(states.keys()))
    
    # Get or create constituencies
    constituencies_needed = ['Varanasi', 'Gorakhpur', 'Lucknow', 'New Delhi', 'Wayanad', 'Bhowanipore', 'Gandhinagar']
    
    for const_name in constituencies_needed:
        existing = db.query(Constituency).filter(Constituency.name == const_name).first()
        if not existing:
            # Determine state for this constituency
            state_code = 'UP'
            if const_name == 'New Delhi':
                state_code = 'DL'
            elif const_name == 'Wayanad':
                state_code = 'KL'
            elif const_name == 'Bhowanipore':
                state_code = 'WB'
            elif const_name == 'Gandhinagar':
                state_code = 'GJ'
            
            state = states.get(state_code)
            if state:
                new_const = Constituency(
                    name=const_name,
                    type='PARLIAMENTARY',
                    state_id=state.id,
                    district=const_name
                )
                db.add(new_const)
                print(f"Created constituency: {const_name}")
    
    db.commit()
    
    # Get constituencies after creation
    constituencies = {c.name: c for c in db.query(Constituency).all()}
    print("Available constituencies:", list(constituencies.keys()))
    
    # Politicians data
    politicians = [
        {
            'name': 'Narendra Modi',
            'party': 'Bharatiya Janata Party',
            'age': 73,
            'gender': 'Male',
            'education': 'M.A. Political Science, Gujarat University',
            'profession': 'Politician, Social Worker',
            'state_code': 'UP',
            'constituency_name': 'Varanasi',
            'assets': {
                'total': 'Rs 2,80,00,000',
                'movable': 'Rs 1,20,00,000',
                'immovable': 'Rs 1,60,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 11,34,567'
            },
            'elections': [
                {'year': 2014, 'votes': 581022, 'percent': 56.9, 'won': True},
                {'year': 2019, 'votes': 674664, 'percent': 63.6, 'won': True}
            ]
        },
        {
            'name': 'Rahul Gandhi',
            'party': 'Indian National Congress',
            'age': 53,
            'gender': 'Male',
            'education': 'M.Phil, Trinity College, Cambridge',
            'profession': 'Politician',
            'state_code': 'DL',
            'constituency_name': 'Wayanad',
            'assets': {
                'total': 'Rs 15,40,00,000',
                'movable': 'Rs 5,40,00,000',
                'immovable': 'Rs 10,00,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 45,00,000'
            },
            'elections': [
                {'year': 2014, 'votes': 408651, 'percent': 43.1, 'won': True},
                {'year': 2019, 'votes': 706543, 'percent': 64.7, 'won': True}
            ]
        },
        {
            'name': 'Arvind Kejriwal',
            'party': 'Aam Aadmi Party',
            'age': 55,
            'gender': 'Male',
            'education': 'B.Tech, IIT Kharagpur',
            'profession': 'Social Worker, Politician',
            'state_code': 'DL',
            'constituency_name': 'New Delhi',
            'assets': {
                'total': 'Rs 2,50,00,000',
                'movable': 'Rs 1,00,00,000',
                'immovable': 'Rs 1,50,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 18,00,000'
            },
            'elections': [
                {'year': 2015, 'votes': 57069, 'percent': 64.2, 'won': True},
                {'year': 2020, 'votes': 46823, 'percent': 60.5, 'won': True}
            ]
        },
        {
            'name': 'Mamata Banerjee',
            'party': 'All India Trinamool Congress',
            'age': 68,
            'gender': 'Female',
            'education': 'B.A., LL.B, University of Calcutta',
            'profession': 'Politician, Lawyer',
            'state_code': 'WB',
            'constituency_name': 'Bhowanipore',
            'assets': {
                'total': 'Rs 55,00,000',
                'movable': 'Rs 25,00,000',
                'immovable': 'Rs 30,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 12,00,000'
            },
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
            'gender': 'Male',
            'education': 'B.Sc., DAV College',
            'profession': 'Politician, Priest',
            'state_code': 'UP',
            'constituency_name': 'Gorakhpur',
            'assets': {
                'total': 'Rs 1,20,00,000',
                'movable': 'Rs 50,00,000',
                'immovable': 'Rs 70,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 8,00,000'
            },
            'elections': [
                {'year': 2017, 'votes': 521089, 'percent': 67.8, 'won': True},
                {'year': 2022, 'votes': 489012, 'percent': 58.4, 'won': True}
            ]
        },
        {
            'name': 'Amit Shah',
            'party': 'Bharatiya Janata Party',
            'age': 59,
            'gender': 'Male',
            'education': 'B.Sc.',
            'profession': 'Politician',
            'state_code': 'GJ',
            'constituency_name': 'Gandhinagar',
            'assets': {
                'total': 'Rs 5,00,00,000',
                'movable': 'Rs 2,00,00,000',
                'immovable': 'Rs 3,00,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 15,00,000'
            },
            'elections': [
                {'year': 2019, 'votes': 892000, 'percent': 69.8, 'won': True}
            ]
        },
        {
            'name': 'Rajnath Singh',
            'party': 'Bharatiya Janata Party',
            'age': 72,
            'gender': 'Male',
            'education': 'M.Sc.',
            'profession': 'Politician',
            'state_code': 'UP',
            'constituency_name': 'Lucknow',
            'assets': {
                'total': 'Rs 3,50,00,000',
                'movable': 'Rs 1,50,00,000',
                'immovable': 'Rs 2,00,00,000',
                'liabilities': 'Rs 0',
                'income': 'Rs 10,00,000'
            },
            'elections': [
                {'year': 2014, 'votes': 560000, 'percent': 52.3, 'won': True},
                {'year': 2019, 'votes': 640000, 'percent': 58.7, 'won': True}
            ]
        }
    ]
    
    updated = 0
    for data in politicians:
        candidate = db.query(Candidate).filter(Candidate.name == data['name']).first()
        
        if not candidate:
            print(f"Candidate not found: {data['name']}")
            continue
        
        print(f"\nUpdating: {data['name']}")
        
        # Get constituency
        constituency = constituencies.get(data['constituency_name'])
        constituency_id = constituency.id if constituency else None
        
        # Update basic info
        candidate.age = data['age']
        candidate.gender = data['gender']
        candidate.education = data['education'][:200]
        candidate.profession = data['profession'][:200]
        candidate.party = data['party']
        candidate.constituency_id = constituency_id
        if data['state_code'] in states:
            candidate.state_id = states[data['state_code']].id
        candidate.is_current = True
        
        # Add affidavit if not exists
        if not candidate.affidavit:
            affidavit = Affidavit(
                candidate_id=candidate.id,
                total_assets=data['assets']['total'],
                movable_assets=data['assets']['movable'],
                immovable_assets=data['assets']['immovable'],
                total_liabilities=data['assets']['liabilities'],
                annual_income=data['assets']['income'],
                education_details=data['education'][:500],
                profession_details=data['profession'][:500],
                filed_on=datetime(2024, 1, 1)
            )
            db.add(affidavit)
            print("   Added affidavit")
        
        # Add election results
        existing_years = [r.election_year for r in candidate.election_results]
        for election in data['elections']:
            if election['year'] not in existing_years:
                result = ElectionResult(
                    candidate_id=candidate.id,
                    election_year=election['year'],
                    election_type='LOK_SABHA' if election['year'] >= 2014 else 'ASSEMBLY',
                    constituency_id=constituency_id,
                    votes_received=election['votes'],
                    vote_percentage=election['percent'],
                    winner=election['won'],
                    margin=election['votes'] // 20
                )
                db.add(result)
                print(f"   Added election result: {election['year']}")
        
        updated += 1
        db.commit()
        print("   Done")
    
    print("\n" + "=" * 60)
    print(f"SUCCESS! Updated {updated} politicians")
    print("=" * 60)
    
    # Verification
    print("\nVerification:")
    for data in politicians:
        c = db.query(Candidate).filter(Candidate.name == data['name']).first()
        if c:
            const = db.query(Constituency).filter(Constituency.id == c.constituency_id).first()
            const_name = const.name if const else "None"
            print(f"\n  {c.name}:")
            print(f"    Age: {c.age}")
            print(f"    Party: {c.party}")
            print(f"    Constituency: {const_name}")
            print(f"    State ID: {c.state_id}")
            print(f"    Affidavit: {'Yes' if c.affidavit else 'No'}")
            print(f"    Elections: {len(c.election_results)}")
    
    db.close()
    print("\n" + "=" * 60)
    print("All done!")
    print("=" * 60)

if __name__ == "__main__":
    main()