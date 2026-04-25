import re
import hashlib
from datetime import datetime
from typing import Optional

def clean_currency(value: str) -> Optional[float]:
    """Clean currency string to float"""
    if not value:
        return None
    # Remove currency symbols and commas
    cleaned = re.sub(r'[₹,\s]+', '', str(value))
    try:
        return float(cleaned)
    except:
        return None

def format_currency(value: float) -> str:
    """Format float to Indian currency format"""
    if not value:
        return "N/A"
    return f"₹{value:,.2f}"

def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def generate_cache_key(*args) -> str:
    """Generate cache key from arguments"""
    key_string = ":".join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def validate_voter_id(voter_id: str) -> bool:
    """Validate voter ID format"""
    # Voter ID format: 3 letters + 7 digits
    pattern = r'^[A-Z]{3}\d{7}$'
    return bool(re.match(pattern, voter_id.upper()))

def extract_constituency_from_voter_id(voter_id: str) -> Optional[str]:
    """Extract constituency code from voter ID (mock)"""
    # In production, this would call ECI API
    # For now, return mock based on ID pattern
    if not validate_voter_id(voter_id):
        return None
    # Mock mapping - in production use API
    mapping = {
        "ABC": "VARANASI",
        "DEF": "LUCKNOW",
        "GHI": "GORAKHPUR"
    }
    prefix = voter_id[:3].upper()
    return mapping.get(prefix, "UNKNOWN")