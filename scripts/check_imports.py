"""Diagnostic script to check imports"""

print("=" * 50)
print("Checking Python Environment")
print("=" * 50)

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

print("\n" + "=" * 50)
print("Checking Installed Packages")
print("=" * 50)

packages = ["sqlalchemy", "pymysql", "fastapi", "uvicorn", "dotenv"]
for package in packages:
    try:
        exec(f"import {package}")
        print(f"✅ {package}")
    except ImportError as e:
        print(f"❌ {package}: {e}")

print("\n" + "=" * 50)
print("Checking Database Connection")
print("=" * 50)

try:
    from sqlalchemy import create_engine, text
    import os
    from pathlib import Path
    
    # Load .env
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    db_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                    print(f"Found DATABASE_URL in .env")
                    break
    else:
        db_url = "mysql+pymysql://root@localhost:3306/neta_nexus"
        print(f"Using default DATABASE_URL")
    
    # Test connection (mask password)
    display_url = db_url.split(':')[0] + ':***@' + db_url.split('@')[1] if '@' in db_url else db_url[:30] + '...'
    print(f"Testing connection to: {display_url}")
    
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.fetchone()
        print(f"✅ Connected! MySQL Version: {version[0]}")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")

print("\n" + "=" * 50)
print("Recommendations")
print("=" * 50)

if "sqlalchemy" in str(e) or "pymysql" in str(e):
    print("Run these commands:")
    print("  pip install sqlalchemy pymysql cryptography")
    print("  pip install --upgrade sqlalchemy")