"""
Download real candidate photos from Wikipedia
Run: python scripts/download_candidate_images_clean.py
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from pathlib import Path
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

def get_wikipedia_image(name):
    """Fetch image URL from Wikipedia"""
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(name)}&format=json"
    
    try:
        response = requests.get(search_url, timeout=10)
        data = response.json()
        
        if data.get('query', {}).get('search'):
            page_title = data['query']['search'][0]['title']
            image_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&format=json&pithumbsize=300"
            img_response = requests.get(image_url, timeout=10)
            img_data = img_response.json()
            
            pages = img_data.get('query', {}).get('pages', {})
            for page in pages.values():
                if 'thumbnail' in page:
                    return page['thumbnail']['source']
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def download_images():
    """Download images for all candidates"""
    image_dir = Path('backend/static/candidate_images')
    image_dir.mkdir(parents=True, exist_ok=True)
    
    with engine.connect() as conn:
        candidates = conn.execute(text("SELECT id, name FROM candidates WHERE image_url IS NULL OR image_url = ''"))
        
        for candidate in candidates:
            cand_id, name = candidate
            print(f"Fetching image for: {name}")
            
            image_url = get_wikipedia_image(name)
            if image_url:
                try:
                    response = requests.get(image_url, timeout=30)
                    if response.status_code == 200:
                        filepath = image_dir / f"{cand_id}.jpg"
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        # Update database
                        conn.execute(
                            text("UPDATE candidates SET image_url = :url WHERE id = :id"),
                            {"url": f"/static/candidate_images/{cand_id}.jpg", "id": cand_id}
                        )
                        conn.commit()
                        print(f"  ✅ Downloaded: {name}")
                    else:
                        print(f"  ❌ Failed: {name}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
            else:
                print(f"  ⚠️ No image found: {name}")
            
            time.sleep(0.5)

if __name__ == "__main__":
    download_images()