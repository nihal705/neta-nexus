from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Candidate, Affidavit, CriminalCase, ElectionResult
from backend.schemas import CompareRequest, CompareResponse, CandidateDetailResponse

router = APIRouter()

@router.post("/")
async def compare_candidates(request: CompareRequest, db: Session = Depends(get_db)):
    """Compare multiple candidates side by side"""
    
    if len(request.candidate_ids) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 candidates to compare")
    
    if len(request.candidate_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 candidates can be compared")
    
    candidates = []
    for cand_id in request.candidate_ids:
        candidate = db.query(Candidate).filter(Candidate.id == cand_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail=f"Candidate {cand_id} not found")
        candidates.append(candidate)
    
    # Build detailed comparison response
    comparison_data = []
    
    for candidate in candidates:
        # Get affidavit
        affidavit = candidate.affidavit
        total_assets = affidavit.total_assets if affidavit else "N/A"
        
        # Count criminal cases
        criminal_count = len(candidate.criminal_cases)
        
        # Count election wins
        wins = sum(1 for r in candidate.election_results if r.winner)
        
        comparison_data.append({
            "id": candidate.id,
            "name": candidate.name,
            "party": candidate.party,
            "age": candidate.age or "N/A",
            "education": candidate.education or "N/A",
            "profession": candidate.profession or "N/A",
            "total_assets": total_assets,
            "criminal_cases": criminal_count,
            "election_wins": wins,
            "photo_url": candidate.photo_url
        })
    
    return {
        "candidates": comparison_data,
        "comparison_fields": [
            "name", "party", "age", "education", "profession",
            "total_assets", "criminal_cases", "election_wins"
        ]
    }

@router.get("/summary/{candidate_id}")
async def get_candidate_summary(candidate_id: int, db: Session = Depends(get_db)):
    """Get quick summary for comparison card"""
    
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    wins = sum(1 for r in candidate.election_results if r.winner)
    criminal_count = len(candidate.criminal_cases)
    
    return {
        "id": candidate.id,
        "name": candidate.name,
        "party": candidate.party,
        "photo_url": candidate.photo_url,
        "age": candidate.age,
        "education": candidate.education,
        "election_wins": wins,
        "criminal_cases": criminal_count,
        "is_current": candidate.is_current
    }