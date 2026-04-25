#!/usr/bin/env python3
"""
Download ADR (Association for Democratic Reforms) data
Source: https://github.com/datameet/india-election-data
"""

import requests
import pandas as pd
import os
from pathlib import Path

# Create data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# URLs for datasets
DATASETS = {
    "adr_2014": "https://raw.githubusercontent.com/datameet/india-election-data/master/affidavits/adr-2014.csv",
    "adr_2009": "https://raw.githubusercontent.com/datameet/india-election-data/master/affidavits/adr-2009.csv",
    "ipc_crimes_2014": "https://raw.githubusercontent.com/datameet/india-election-data/master/affidavits/ipc-crimes-2014.csv",
    "adr_2019": "https://raw.githubusercontent.com/datameet/india-election-data/master/affidavits/adr-2019.csv",
}

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    filepath = DATA_DIR / filename
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    file_size = filepath.stat().st_size
    print(f"✅ Saved to {filepath} ({file_size:,} bytes)")
    return filepath

def preview_data(filepath):
    """Show preview of downloaded data"""
    df = pd.read_csv(filepath)
    print(f"   - Rows: {len(df):,}")
    print(f"   - Columns: {', '.join(df.columns[:5])}...")
    return df

def main():
    print("=" * 50)
    print("📥 Downloading ADR Election Data")
    print("=" * 50)
    
    for name, url in DATASETS.items():
        try:
            filepath = download_file(url, f"{name}.csv")
            preview_data(filepath)
            print()
        except Exception as e:
            print(f"❌ Error downloading {name}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Download complete!")
    print(f"📁 Data saved to: {DATA_DIR}")
    print("=" * 50)
    
    print("\n📌 Next steps:")
    print("1. Run: python scripts/import_candidates.py")
    print("2. Or run: npm run data:import")

if __name__ == "__main__":
    main()