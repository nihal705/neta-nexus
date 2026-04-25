from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import json

from backend.database import get_db
from backend.models import Candidate

router = APIRouter()

# Symbol mapping for major parties (emoji fallback)
PARTY_SYMBOLS = {
    "Bharatiya Janata Party": {"symbol": "🪷", "color": "#FF9933", "name": "BJP"},
    "Indian National Congress": {"symbol": "👋", "color": "#00BFFF", "name": "INC"},
    "Aam Aadmi Party": {"symbol": "🧹", "color": "#00BFFF", "name": "AAP"},
    "All India Trinamool Congress": {"symbol": "🌾", "color": "#008000", "name": "TMC"},
    "Samajwadi Party": {"symbol": "🚲", "color": "#FF0000", "name": "SP"},
    "Bahujan Samaj Party": {"symbol": "🐘", "color": "#0000FF", "name": "BSP"},
    "Communist Party of India (Marxist)": {"symbol": "🌾🔴", "color": "#FF0000", "name": "CPI(M)"},
    "Nationalist Congress Party": {"symbol": "⌚", "color": "#0000FF", "name": "NCP"},
    "Telugu Desam Party": {"symbol": "🚲", "color": "#FFFF00", "name": "TDP"},
    "Dravida Munnetra Kazhagam": {"symbol": "🌞", "color": "#FF0000", "name": "DMK"},
    "Yuvajana Sramika Rythu Congress Party": {"symbol": "✋", "color": "#0000FF", "name": "YSRCP"},
    "Janata Dal (United)": {"symbol": "🔊", "color": "#008000", "name": "JD(U)"},
    "Shiv Sena": {"symbol": "🐯", "color": "#FF6600", "name": "SS"},
    "Rashtriya Janata Dal": {"symbol": "💡", "color": "#008000", "name": "RJD"},
    "Communist Party of India": {"symbol": "🌾", "color": "#FF0000", "name": "CPI"},
    "Janata Dal (Secular)": {"symbol": "👨‍🌾", "color": "#008000", "name": "JD(S)"},
    "Rashtriya Loktantrik Party": {"symbol": "📯", "color": "#FF9933", "name": "RLP"},
    "Apna Dal": {"symbol": "👩", "color": "#FF9933", "name": "AD"},
    "Suheldev Bharatiya Samaj Party": {"symbol": "🐘", "color": "#FF9933", "name": "SBSP"},
    "NISHAD Party": {"symbol": "🐟", "color": "#00BFFF", "name": "NISHAD"},
    "Jansatta Dal": {"symbol": "📢", "color": "#008000", "name": "Jansatta"},
}

@router.get("/symbols")
async def get_party_symbols():
    """Get all party symbols"""
    return PARTY_SYMBOLS

@router.get("/symbol/{party_name}")
async def get_party_symbol(party_name: str):
    """Get symbol for a specific party"""
    if not party_name:
        return {"symbol": "🏛️", "color": "#666666", "short_name": "Unknown"}
    
    # Normalize party name
    for key, value in PARTY_SYMBOLS.items():
        if key.lower() in party_name.lower() or party_name.lower() in key.lower():
            return {
                "party": party_name,
                "matched_party": key,
                "symbol": value["symbol"],
                "color": value["color"],
                "short_name": value["name"]
            }
    
    # Default fallback
    return {
        "party": party_name,
        "symbol": "🏛️",
        "color": "#666666",
        "short_name": party_name[:15] if party_name else "Unknown"
    }

@router.get("/candidate/{candidate_id}/image")
async def get_candidate_image(candidate_id: int, db: Session = Depends(get_db)):
    """Get or generate candidate image"""
    
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check if image exists locally
    image_path = f"backend/static/candidate_photos/{candidate_id}.webp"
    
    if os.path.exists(image_path):
        return {
            "has_image": True, 
            "url": f"/static/candidate_photos/{candidate_id}.webp",
            "initials": "",
            "color": "#00A896"
        }
    
    # Generate avatar from initials
    name_parts = candidate.name.split() if candidate.name else ["?"]
    initials = "".join([part[0] for part in name_parts[:2]]).upper() if candidate.name else "?"
    
    # Get party color
    party_info = await get_party_symbol(candidate.party)
    color = party_info.get("color", "#00A896")
    
    return {
        "has_image": False,
        "initials": initials,
        "color": color,
        "name": candidate.name,
        "party": candidate.party
    }


@router.get("/candidate/bulk-images")
async def get_bulk_candidate_images(
    candidate_ids: str,
    db: Session = Depends(get_db)
):
    """Get images for multiple candidates at once"""
    
    ids = [int(x.strip()) for x in candidate_ids.split(",")]
    candidates = db.query(Candidate).filter(Candidate.id.in_(ids)).all()
    
    results = {}
    for candidate in candidates:
        # Generate initials
        name_parts = candidate.name.split() if candidate.name else ["?"]
        initials = "".join([part[0] for part in name_parts[:2]]).upper() if candidate.name else "?"
        
        # Get party color
        party_info = await get_party_symbol(candidate.party)
        color = party_info.get("color", "#00A896")
        
        results[candidate.id] = {
            "initials": initials,
            "color": color,
            "name": candidate.name,
            "party": candidate.party
        }
    
    return results