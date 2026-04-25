"""
Download real candidate photos from Wikipedia API
Run: python scripts/download_candidate_images.py
"""

import requests
import os
import time
from pathlib import Path
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://root:{ENCODED_PASSWORD}@localhost:3306/neta_nexus"

def get_wikipedia_image(name):
    """Fetch candidate image from Wikipedia API"""
    
    # Search Wikipedia
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(name)}&format=json"
    
    try:
        response = requests.get(search_url, timeout=10)
        data = response.json()
        
        if data.get('query', {}).get('search'):
            page_title = data['query']['search'][0]['title']
            
            # Get page image
            image_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote_plus(page_title)}&prop=pageimages&format=json&pithumbsize=200"
            img_response = requests.get(image_url, timeout=10)
            img_data = img_response.json()
            
            pages = img_data.get('query', {}).get('pages', {})
            for page in pages.values():
                if 'thumbnail' in page:
                    return page['thumbnail']['source']
    except Exception as e:
        print(f"Error fetching image for {name}: {e}")
    
    return None

def download_candidate_images(limit=100):
    """Download images for top candidates"""
    
    from sqlalchemy import create_engine, text
    engine = create_engine(DATABASE_URL)
    
    image_dir = Path('backend/static/candidate_photos')
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # Get top candidates
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name FROM candidates 
            WHERE name IS NOT NULL 
            ORDER BY id LIMIT :limit
        """), {"limit": limit})
        candidates = result.fetchall()
    
    for candidate in candidates:
        cand_id, name = candidate
        image_path = image_dir / f"{cand_id}.jpg"
        
        if image_path.exists():
            print(f"Image exists for {name}")
            continue
        
        print(f"Fetching image for: {name}")
        image_url = get_wikipedia_image(name)
        
        if image_url:
            try:
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"  ✅ Downloaded: {name}")
                time.sleep(1)
            except Exception as e:
                print(f"  ❌ Failed: {e}")
        else:
            print(f"  ⚠️ No image found for {name}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    download_candidate_images(50)