
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path

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

with engine.connect() as conn:
    # Check Karnataka state ID
    result = conn.execute(text("SELECT id, name, code FROM states WHERE name = 'Karnataka' OR code = 'KA'"))
    karnataka = result.fetchone()
    print(f'Karnataka state: {karnataka}')
    
    if karnataka:
        # Check candidates with Karnataka state_id
        result = conn.execute(text("SELECT COUNT(*) FROM candidates WHERE state_id = :state_id"), {"state_id": karnataka[0]})
        print(f'Candidates with state_id = {karnataka[0]}: {result.fetchone()[0]}')
        
        # Show sample Karnataka candidates
        result = conn.execute(text("SELECT name, party FROM candidates WHERE state_id = :state_id LIMIT 10"), {"state_id": karnataka[0]})
        print('\nSample Karnataka candidates:')
        for row in result:
            print(f'  {row[0]} - {row[1]}')
    else:
        print('Karnataka state not found in states table!')
