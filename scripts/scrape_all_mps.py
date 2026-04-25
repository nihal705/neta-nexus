"""
Complete scraper for ALL 543 Lok Sabha MPs
Source: PRS India (prsindia.org/mptrack)
Run: python scripts/scrape_all_mps.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENCODED = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://root:{ENCODED}@localhost:3306/neta_nexus_clean"
engine = create_engine(DATABASE_URL)

def scrape_all_mps():
    """Scrape ALL 543 MPs from PRS India"""
    
    all_mps = []
    
    # PRS India MP list page (all 543 MPs)
    base_url = "https://prsindia.org/mptrack"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print("Fetching MP list...")
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all MP links (this will get ALL 543)
    mp_links = []
    for link in soup.find_all('a', href=True):
        if '/mptrack/' in link['href'] and 'mpid=' in link['href']:
            mp_links.append(link['href'])
    
    mp_links = list(set(mp_links))  # Remove duplicates
    print(f"Found {len(mp_links)} MP links")
    
    for idx, mp_url in enumerate(mp_links):
        print(f"Scraping MP {idx+1}/{len(mp_links)}...")
        
        try:
            full_url = f"https://prsindia.org{mp_url}" if mp_url.startswith('/') else mp_url
            mp_response = requests.get(full_url, headers=headers, timeout=30)
            mp_soup = BeautifulSoup(mp_response.content, 'html.parser')
            
            # Extract MP data
            mp_data = {}
            
            # Name
            name_tag = mp_soup.find('h1')
            mp_data['name'] = name_tag.text.strip() if name_tag else ''
            
            # Party, Constituency, State
            info_table = mp_soup.find('table', class_='info-table')
            if info_table:
                rows = info_table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        key = cells[0].text.strip().lower()
                        value = cells[1].text.strip()
                        if 'party' in key:
                            mp_data['party'] = value
                        elif 'constituency' in key:
                            mp_data['constituency'] = value
                        elif 'state' in key:
                            mp_data['state'] = value
            
            # Parliamentary performance
            performance = mp_soup.find('div', class_='performance-stats')
            if performance:
                stats = performance.find_all('div', class_='stat')
                for stat in stats:
                    label = stat.find('span', class_='label')
                    value = stat.find('span', class_='value')
                    if label and value:
                        if 'attendance' in label.text.lower():
                            mp_data['attendance'] = value.text.strip().replace('%', '')
                        elif 'questions' in label.text.lower():
                            mp_data['questions'] = value.text.strip()
            
            all_mps.append(mp_data)
            time.sleep(1)  # Be respectful
            
        except Exception as e:
            print(f"Error scraping MP: {e}")
            continue
    
    # Save to database
    with engine.connect() as conn:
        for mp in all_mps:
            # Insert into database
            conn.execute(
                text("""
                    INSERT INTO candidates (name, party, is_current) 
                    VALUES (:name, :party, 1)
                    ON DUPLICATE KEY UPDATE party = :party
                """),
                {"name": mp.get('name'), "party": mp.get('party')}
            )
        conn.commit()
    
    print(f"\n✅ Completed! Scraped {len(all_mps)} MPs")
    return all_mps

if __name__ == "__main__":
    scrape_all_mps()