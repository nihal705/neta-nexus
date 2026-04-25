#!/usr/bin/env python3
"""
Setup database and create all tables
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import engine, Base
from backend.models import (
    State, Constituency, Candidate, Affidavit, 
    CriminalCase, ElectionResult, ParliamentaryScore, ExitPoll
)

def setup_database():
    """Create all database tables"""
    print("=" * 50)
    print("Setting up database...")
    print("=" * 50)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Tables created: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()