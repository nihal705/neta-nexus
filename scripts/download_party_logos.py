"""
Download real party logos from official sources
Run: python scripts/download_party_logos.py
"""

import requests
import os
from pathlib import Path

# Real party logo URLs (from official Election Commission sources)
PARTY_LOGOS = {
    'Bharatiya Janata Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/BJP_logo.svg/200px-BJP_logo.svg.png',
        'color': '#FF9933'
    },
    'Indian National Congress': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Indian_National_Congress_Logo.svg/200px-Indian_National_Congress_Logo.svg.png',
        'color': '#00BFFF'
    },
    'Aam Aadmi Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Aam_Aadmi_Party_logo_%28English%29.png/200px-Aam_Aadmi_Party_logo_%28English%29.png',
        'color': '#00BFFF'
    },
    'All India Trinamool Congress': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/All_India_Trinamool_Congress_logo.svg/200px-All_India_Trinamool_Congress_logo.svg.png',
        'color': '#008000'
    },
    'Samajwadi Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Samajwadi_Party_logo.svg/200px-Samajwadi_Party_logo.svg.png',
        'color': '#FF0000'
    },
    'Bahujan Samaj Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Bahujan_Samaj_Party_logo.svg/200px-Bahujan_Samaj_Party_logo.svg.png',
        'color': '#0000FF'
    },
    'Communist Party of India (Marxist)': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/CPI-M-flag.svg/200px-CPI-M-flag.svg.png',
        'color': '#FF0000'
    },
    'Nationalist Congress Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Nationalist_Congress_Party_logo.svg/200px-Nationalist_Congress_Party_logo.svg.png',
        'color': '#0000FF'
    },
    'Telugu Desam Party': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Telugu_Desam_Party_logo.svg/200px-Telugu_Desam_Party_logo.svg.png',
        'color': '#FFFF00'
    },
    'Dravida Munnetra Kazhagam': {
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/DMK_Logo.svg/200px-DMK_Logo.svg.png',
        'color': '#FF0000'
    },
}

def download_logos():
    """Download all party logos"""
    
    logo_dir = Path('backend/static/party_logos')
    logo_dir.mkdir(parents=True, exist_ok=True)
    
    for party, info in PARTY_LOGOS.items():
        try:
            response = requests.get(info['url'], timeout=30)
            if response.status_code == 200:
                filename = party.replace(' ', '_').replace('(', '').replace(')', '') + '.png'
                filepath = logo_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {party}")
            else:
                print(f"❌ Failed: {party}")
        except Exception as e:
            print(f"❌ Error downloading {party}: {e}")

if __name__ == "__main__":
    download_logos()