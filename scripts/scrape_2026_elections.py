"""
Scrape 2026 State Election Data from MyNeta
States: Tamil Nadu, Kerala, West Bengal, Puducherry, Assam
Run: python scripts/scrape_2026_elections.py
"""

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin

# Define the 2026 elections
ELECTIONS = {
    'Tamil Nadu': {
        'url': 'https://myneta.info/TamilNadu2026/index.php?action=show_constituencies',
        'state_code': 'TN',
        'year': 2026
    },
    'Kerala': {
        'url': 'https://myneta.info/Kerala2026/index.php?action=show_constituencies',
        'state_code': 'KL',
        'year': 2026
    },
    'West Bengal': {
        'url': 'https://myneta.info/WestBengal2026/index.php?action=show_constituencies',
        'state_code': 'WB',
        'year': 2026
    },
    'Puducherry': {
        'url': 'https://myneta.info/Puducherry2026/index.php?action=show_constituencies',
        'state_code': 'PY',
        'year': 2026
    },
    'Assam': {
        'url': 'https://myneta.info/Assam2026/index.php?action=show_constituencies',
        'state_code': 'AS',
        'year': 2026
    }
}

def scrape_state_candidates(state_name, config):
    """Scrape all candidates for a state from MyNeta"""
    
    print(f"\n{'='*60}")
    print(f"Scraping {state_name} 2026 Elections")
    print(f"{'='*60}")
    
    all_candidates = []
    url = config['url']
    state_code = config['state_code']
    year = config['year']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all constituency links
        constituency_links = []
        for link in soup.find_all('a', href=True):
            if 'action=show_candidates' in link['href'] or 'constituency_id' in link['href']:
                full_url = urljoin(url, link['href'])
                if full_url not in [c['url'] for c in constituency_links]:
                    constituency_links.append({
                        'name': link.text.strip(),
                        'url': full_url
                    })
        
        print(f"Found {len(constituency_links)} constituencies")
        
        # Scrape each constituency
        for const in constituency_links[:10]:  # Limit to 10 for testing; remove [:10] for full scrape
            print(f"  Scraping: {const['name']}")
            
            try:
                const_response = requests.get(const['url'], headers=headers, timeout=30)
                const_soup = BeautifulSoup(const_response.content, 'html.parser')
                
                # Find the candidates table
                table = const_soup.find('table', id='table1')
                if not table:
                    continue
                
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        candidate = {
                            'state': state_name,
                            'state_code': state_code,
                            'year': year,
                            'constituency': const['name'],
                            'sno': cols[0].text.strip() if len(cols) > 0 else '',
                            'name': cols[1].text.strip() if len(cols) > 1 else '',
                            'party': cols[2].text.strip() if len(cols) > 2 else '',
                            'criminal_cases': cols[3].text.strip() if len(cols) > 3 else '0',
                            'education': cols[4].text.strip() if len(cols) > 4 else '',
                            'age': cols[5].text.strip() if len(cols) > 5 else '',
                            'total_assets': cols[6].text.strip() if len(cols) > 6 else '',
                            'liabilities': cols[7].text.strip() if len(cols) > 7 else ''
                        }
                        
                        if candidate['name']:
                            all_candidates.append(candidate)
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                print(f"    Error: {e}")
                continue
        
        print(f"  Total candidates scraped: {len(all_candidates)}")
        
    except Exception as e:
        print(f"Error scraping {state_name}: {e}")
    
    return all_candidates

def main():
    """Main function to scrape all states"""
    
    print("="*60)
    print("SCRAPING 2026 STATE ELECTIONS FROM MYNETA")
    print("="*60)
    
    all_candidates = []
    
    for state_name, config in ELECTIONS.items():
        candidates = scrape_state_candidates(state_name, config)
        all_candidates.extend(candidates)
        time.sleep(2)  # Delay between states
    
    # Save to CSV
    if all_candidates:
        df = pd.DataFrame(all_candidates)
        output_file = 'data/2026_elections_all_states.csv'
        df.to_csv(output_file, index=False)
        print(f"\n{'='*60}")
        print(f"✅ SAVED {len(all_candidates)} candidates to {output_file}")
        print(f"{'='*60}")
        print(f"\n📊 Breakdown by state:")
        print(df['state'].value_counts().to_string())
    else:
        print("\n❌ No candidates scraped. Please check the URLs.")

if __name__ == "__main__":
    main()