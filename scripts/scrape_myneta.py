import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_myneta(state="up", year=2019):
    """Scrape candidate data from myneta.info"""
    
    url = f"http://myneta.info/{state}{year}/index.php?action=show_candidates"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        candidates = []
        rows = soup.find_all('tr')[1:11]  # Get first 10 candidates
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                candidate = {
                    'name': cols[0].text.strip(),
                    'party': cols[1].text.strip(),
                    'constituency': cols[2].text.strip()
                }
                candidates.append(candidate)
                print(f"Found: {candidate}")
        
        # Save to CSV
        df = pd.DataFrame(candidates)
        df.to_csv('data/scraped_candidates.csv', index=False)
        print(f"\n✅ Saved {len(candidates)} candidates!")
        return df
        
    except Exception as e:
        print(f"Error: {e}")
        print("Try changing state and year")
        return None

if __name__ == "__main__":
    scrape_myneta()