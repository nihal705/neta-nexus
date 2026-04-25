from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# Candidate Schemas
class CandidateBase(BaseModel):
    name: str
    party: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    education: Optional[str] = None
    profession: Optional[str] = None
    photo_url: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    constituency_id: Optional[int] = None
    state_id: Optional[int] = None
    is_current: bool = False
    
    class Config:
        from_attributes = True

# Affidavit Schemas
class AffidavitResponse(BaseModel):
    total_assets: Optional[str] = None
    movable_assets: Optional[str] = None
    immovable_assets: Optional[str] = None
    total_liabilities: Optional[str] = None
    annual_income: Optional[str] = None
    education_details: Optional[str] = None
    filed_on: Optional[date] = None

# Criminal Case Schemas
class CriminalCaseResponse(BaseModel):
    case_number: str
    case_type: str
    sections: str
    status: str
    filed_before_election: bool
    case_details: Optional[str] = None

# Election Result Schemas
class ElectionResultResponse(BaseModel):
    election_year: int
    election_type: str
    votes_received: int
    vote_percentage: float
    winner: bool
    margin: int

# Parliamentary Score Schema
class ParliamentaryScoreResponse(BaseModel):
    attendance_percentage: float
    questions_asked: int
    debates_participated: int
    private_member_bills: int
    composite_score: float

# Complete Candidate Detail
class CandidateDetailResponse(CandidateResponse):
    affidavit: Optional[AffidavitResponse] = None
    criminal_cases: List[CriminalCaseResponse] = []
    election_results: List[ElectionResultResponse] = []
    parliamentary_score: Optional[ParliamentaryScoreResponse] = None

# Search Response
class SearchResponse(BaseModel):
    total: int
    candidates: List[CandidateResponse]
    page: int
    per_page: int
    total_pages: int

# Exit Poll Schema
class ExitPollResponse(BaseModel):
    source_name: str
    prediction_data: Dict[str, Any]
    published_at: datetime
    color: Optional[str] = None

# Compare Schemas
class CompareRequest(BaseModel):
    candidate_ids: List[int] = Field(..., min_length=2, max_length=5)
    
    @validator('candidate_ids')
    def validate_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Candidate IDs must be unique')
        return v

class CompareResponse(BaseModel):
    candidates: List[CandidateDetailResponse]
    comparison_fields: List[str] = [
        "name", "party", "age", "education", "profession",
        "total_assets", "criminal_cases", "election_wins"
    ]

# Live Results Schema
class LiveResultsResponse(BaseModel):
    election_id: int
    trends: Dict[str, int]
    last_updated: Optional[str]
    is_counting_day: bool
    total_seats: int
    constituencies_declared: int