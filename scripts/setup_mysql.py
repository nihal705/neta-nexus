#!/usr/bin/env python3
"""
Setup MySQL database - Using separated credentials
"""

import sys
import os
from pathlib import Path
from urllib.parse import quote_plus

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env manually
def load_env_file():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value
        return True
    return False

print("Loading environment...")
load_env_file()

# Get database credentials
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "neta_nexus")

# URL encode password
encoded_password = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"Username: {DB_USERNAME}")

# Set the URL in environment for SQLAlchemy
os.environ["DATABASE_URL"] = DATABASE_URL

# Now import and setup
try:
    from sqlalchemy import create_engine, inspect, text
    from sqlalchemy.orm import Session
    
    engine = create_engine(DATABASE_URL)
    print("✅ Database engine created")
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Connection successful!")
    
    from backend.database import Base
    from backend.models import State, Constituency, Candidate, Affidavit, CriminalCase, ElectionResult, ParliamentaryScore, ExitPoll
    
    print("\n📦 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")
    
    # Insert sample states
    session = Session(engine)
    
    states = [
        {"code": "UP", "name": "Uttar Pradesh", "capital": "Lucknow"},
        {"code": "MH", "name": "Maharashtra", "capital": "Mumbai"},
        {"code": "DL", "name": "Delhi", "capital": "New Delhi"},
        {"code": "WB", "name": "West Bengal", "capital": "Kolkata"},
        {"code": "TN", "name": "Tamil Nadu", "capital": "Chennai"},
        {"code": "KA", "name": "Karnataka", "capital": "Bangalore"},
        {"code": "GJ", "name": "Gujarat", "capital": "Gandhinagar"},
        {"code": "BI", "name": "Bihar", "capital": "Patna"},
    ]
    
    for state_data in states:
        existing = session.query(State).filter(State.code == state_data["code"]).first()
        if not existing:
            session.add(State(**state_data))
    
    session.commit()
    print(f"✅ Added {len(states)} states")
    session.close()
    
    # List tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📋 Tables: {', '.join(tables)}")
    
    print("\n🎉 DATABASE SETUP COMPLETE!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()