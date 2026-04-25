"""
Parse MyNeta HTML files - Version 2
Handles different table structures
Run: python scripts/parse_html_v2.py
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import pandas as pd
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env
def load_env():
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")
    return True

load_env()

# Database connection
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://root:{ENCODED_PASSWORD}@localhost:3306/neta_nexus"

print("="*60)
print("PARSING MYNETA HTML FILES - VERSION 2")
print("="*60)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

html_folder = project_root / 'data' / '2026_elections_html'

if not html_folder.exists():
    print(f"\n❌ Folder not found: {html_folder}")
    sys.exit(1)

# State mapping
state_mapping = {
    'assam': {'name': 'Assam', 'code': 'AS'},
    'kerala': {'name': 'Kerala', 'code': 'KL'},
    'puducherry': {'name': 'Puducherry', 'code': 'PY'},
}

all_candidates = []

for html_file in html_folder.glob('*.html'):
    file_name = html_file.stem.lower()
    
    # Determine state
    state_info = None
    for key, info in state_mapping.items():
        if key in file_name:
            state_info = info
            break
    
    if not state_info:
        continue
    
    print(f"\n📖 Parsing: {html_file.name}")
    print(f"   State: {state_info['name']}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Look for ANY table that might contain candidate data
    all_tables = soup.find_all('table')
    candidates_found = 0
    
    for table_idx, table in enumerate(all_tables):
        rows = table.find_all('tr')
        if len(rows) < 2:
            continue
        
        # Check if this table has candidate-like data
        first_row = rows[0]
        headers = first_row.find_all('th')
        
        # If no th, check first row td for patterns
        if not headers:
            first_data = rows[0].find_all('td')
            if first_data and len(first_data) >= 3:
                # Might be data rows without header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        # Try to extract candidate
                        candidate_name = cols[0].get_text(strip=True)
                        if candidate_name and len(candidate_name) > 2 and not candidate_name.isdigit():
                            candidate = {
                                'state': state_info['name'],
                                'state_code': state_info['code'],
                                'year': 2026,
                                'name': candidate_name,
                                'party': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                                'constituency': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                                'criminal_cases': cols[3].get_text(strip=True) if len(cols) > 3 else '0',
                                'education': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                                'age': cols[5].get_text(strip=True) if len(cols) > 5 else '',
                                'total_assets': cols[6].get_text(strip=True) if len(cols) > 6 else '',
                                'liabilities': cols[7].get_text(strip=True) if len(cols) > 7 else ''
                            }
                            all_candidates.append(candidate)
                            candidates_found += 1
            continue
        
        # Check header keywords
        header_text = ' '.join([h.get_text(strip=True).lower() for h in headers])
        
        # If this looks like a candidate table
        if any(keyword in header_text for keyword in ['candidate', 'name', 'party', 'constituency']):
            # Skip header row
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    candidate = {
                        'state': state_info['name'],
                        'state_code': state_info['code'],
                        'year': 2026,
                        'name': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                        'constituency': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                        'party': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'criminal_cases': cols[4].get_text(strip=True) if len(cols) > 4 else '0',
                        'education': cols[5].get_text(strip=True) if len(cols) > 5 else '',
                        'age': cols[6].get_text(strip=True) if len(cols) > 6 else '',
                        'total_assets': cols[7].get_text(strip=True) if len(cols) > 7 else '',
                        'liabilities': cols[8].get_text(strip=True) if len(cols) > 8 else ''
                    }
                    
                    if candidate['name'] and candidate['name'] != 'SNo':
                        all_candidates.append(candidate)
                        candidates_found += 1
    
    print(f"   Found {candidates_found} candidates")

# Save results
if all_candidates:
    df = pd.DataFrame(all_candidates)
    output_file = project_root / 'data' / '2026_elections_parsed.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n{'='*60}")
    print(f"✅ SAVED {len(all_candidates)} candidates to {output_file}")
    print(f"{'='*60}")
    
    # Show sample
    print(f"\n📋 Sample candidates:")
    print(df[['name', 'party', 'constituency']].head(10).to_string())
    
    # Import to MySQL
    print(f"\n📤 Importing to MySQL...")
    
    with engine.connect() as conn:
        inserted = 0
        for idx, row in df.iterrows():
            name = row['name'].replace("'", "''")[:200]
            party = row['party'].replace("'", "''")[:100] if pd.notna(row['party']) else 'Unknown'
            
            # Get or create state
            state_result = conn.execute(text("SELECT id FROM states WHERE code = :code"), {"code": row['state_code']})
            state_id = state_result.fetchone()
            
            if not state_id:
                conn.execute(text("INSERT INTO states (code, name) VALUES (:code, :name)"), 
                           {"code": row['state_code'], "name": row['state']})
                conn.commit()
                state_result = conn.execute(text("SELECT id FROM states WHERE code = :code"), {"code": row['state_code']})
                state_id = state_result.fetchone()
            
            try:
                conn.execute(
                    text("INSERT IGNORE INTO candidates (name, party, state_id, is_current) VALUES (:name, :party, :state_id, 1)"),
                    {"name": name, "party": party, "state_id": state_id[0]}
                )
                inserted += 1
                if inserted % 100 == 0:
                    conn.commit()
                    print(f"      Inserted {inserted} candidates...")
            except Exception as e:
                pass
        
        conn.commit()
        print(f"   ✅ Inserted {inserted} candidates")
    
    # Final count
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM candidates"))
        print(f"\n📊 TOTAL CANDIDATES IN DATABASE: {result.fetchone()[0]}")
else:
    print("\n❌ No candidates found")
    print("\n💡 Tip: Run the diagnostic script first to see the actual HTML structure")

print("\n🎉 Done!")