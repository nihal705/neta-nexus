
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
    # Show actual Karnataka candidates
    result = conn.execute(text("""
        SELECT c.name, c.party, s.name as state_name
        FROM candidates c
        JOIN states s ON c.state_id = s.id
        WHERE c.state_id = 6
        LIMIT 20
    """))
    
    print('Actual Karnataka candidates:')
    for row in result:
        print(f'  {row[0]} - {row[1]} ({row[2]})')
    
    # Count
    result = conn.execute(text('SELECT COUNT(*) FROM candidates WHERE state_id = 6'))
    print(f'\nTotal Karnataka candidates: {result.fetchone()[0]}')
