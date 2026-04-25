
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
    # Check where 'Lal Krishna Advani' is stored
    result = conn.execute(text("SELECT id, name, party, state_id FROM candidates WHERE name LIKE '%Advani%'"))
    for row in result:
        print(f'Candidate: {row[1]}')
        print(f'  State ID: {row[3]}')
        
        # Get state name
        state_result = conn.execute(text("SELECT name, code FROM states WHERE id = :sid"), {"sid": row[3]})
        state = state_result.fetchone()
        if state:
            print(f'  State: {state[0]} ({state[1]})')
        print()