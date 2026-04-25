# Save this as scripts/check_candidates.py
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.models import Candidate

def main():
    db = SessionLocal()
    
    # Count total candidates
    total = db.query(Candidate).count()
    print(f'Total candidates in database: {total}')
    
    if total == 0:
        print('No candidates found! You need to import data first.')
    else:
        # Show all candidates with 'Modi' in name
        modi_candidates = db.query(Candidate).filter(Candidate.name.like('%Modi%')).all()
        print(f'\nCandidates with "Modi" in name: {len(modi_candidates)}')
        for c in modi_candidates:
            print(f'  - {c.name} (ID: {c.id})')
        
        # Show first 10 candidates
        print('\nFirst 10 candidates in database:')
        candidates = db.query(Candidate).limit(10).all()
        for c in candidates:
            print(f'  - {c.name} (Party: {c.party})')
    
    db.close()

if __name__ == "__main__":
    main()