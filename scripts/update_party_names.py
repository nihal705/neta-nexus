"""
Update party names for Karnataka candidates
Run: python scripts/update_party_names.py
"""

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path

# Load .env
env_path = Path('.env')
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENCODED = quote_plus(DB_PASSWORD)
DATABASE_URL = f'mysql+pymysql://root:{ENCODED}@localhost:3306/neta_nexus'
engine = create_engine(DATABASE_URL)

print("="*60)
print("UPDATING PARTY NAMES FOR KARNATAKA CANDIDATES")
print("="*60)

with engine.connect() as conn:
    # Count candidates with Unknown party
    result = conn.execute(text("SELECT COUNT(*) FROM candidates WHERE state_id = 6 AND (party = 'Unknown' OR party IS NULL)"))
    unknown_count = result.fetchone()[0]
    print(f"Candidates with Unknown party in Karnataka: {unknown_count}")
    
    # Update based on name patterns (you can expand this)
    # For now, let's just show the list
    result = conn.execute(text("""
        SELECT id, name, party FROM candidates 
        WHERE state_id = 6 
        LIMIT 20
    """))
    
    print("\nSample Karnataka candidates:")
    for row in result:
        print(f"  ID: {row[0]}, Name: {row[1]}, Party: {row[2]}")
    
    # Optional: Update party for specific known politicians
    # Uncomment these as needed:
    """
    conn.execute(text("UPDATE candidates SET party = 'BJP' WHERE state_id = 6 AND name LIKE '%Modi%'"))
    conn.execute(text("UPDATE candidates SET party = 'INC' WHERE state_id = 6 AND name LIKE '%Gandhi%'"))
    conn.execute(text("UPDATE candidates SET party = 'JD(S)' WHERE state_id = 6 AND name LIKE '%Kumaraswamy%'"))
    conn.execute(text("UPDATE candidates SET party = 'Congress' WHERE state_id = 6 AND name LIKE '%Siddaramaiah%'"))
    conn.commit()
    print("\n✅ Updated party names for known candidates")
    """
    
print("\n🎉 Done!")