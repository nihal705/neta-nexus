import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)

print("=== CANDIDATES TABLE COLUMNS ===")
for col in inspector.get_columns('candidates'):
    print(f"  {col['name']}")

print("\n=== CONSTITUENCIES TABLE COLUMNS ===")
for col in inspector.get_columns('constituencies'):
    print(f"  {col['name']}")

print("\n=== STATES TABLE COLUMNS ===")
for col in inspector.get_columns('states'):
    print(f"  {col['name']}")