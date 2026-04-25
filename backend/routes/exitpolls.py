from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from backend.database import get_db
from backend.models import ExitPoll
from backend.schemas import ExitPollResponse

router = APIRouter()

@router.get("/media")
async def get_media_exit_polls(
    election_id: int = Query(2024, description="Election year"),
    db: Session = Depends(get_db)
):
    """Get exit polls from various media sources"""
    
    # In production, fetch from database
    # For MVP, return comprehensive mock data with all major pollsters
    exit_polls = [
        {
            "source_name": "Axis My India",
            "prediction_data": {
                "BJP": "295-315",
                "INC": "125-145",
                "Others": "55-75",
                "margin_error": "±5%",
                "sample_size": 125000,
                "methodology": "Face-to-face interviews",
                "states_covered": 28
            },
            "published_at": "2024-05-20T19:30:00",
            "color": "#00A896"
        },
        {
            "source_name": "C-Voter",
            "prediction_data": {
                "BJP": "287-305",
                "INC": "132-150",
                "Others": "45-55",
                "margin_error": "±4%",
                "sample_size": 98000,
                "methodology": "Telephonic + IVR",
                "states_covered": 28
            },
            "published_at": "2024-05-20T20:00:00",
            "color": "#2B6CB0"
        },
        {
            "source_name": "Today's Chanakya",
            "prediction_data": {
                "BJP": "305-325",
                "INC": "105-125",
                "Others": "60-70",
                "margin_error": "±3%",
                "sample_size": 150000,
                "methodology": "Door-to-door surveys",
                "states_covered": 28
            },
            "published_at": "2024-05-20T21:00:00",
            "color": "#F59E0B"
        },
        {
            "source_name": "Republic TV",
            "prediction_data": {
                "BJP": "290-310",
                "INC": "130-148",
                "Others": "48-58",
                "margin_error": "±4%",
                "sample_size": 75000,
                "methodology": "Online + CATI",
                "states_covered": 28
            },
            "published_at": "2024-05-20T20:30:00",
            "color": "#DC2626"
        },
        {
            "source_name": "Times Now-ETG",
            "prediction_data": {
                "BJP": "285-300",
                "INC": "135-155",
                "Others": "50-60",
                "margin_error": "±5%",
                "sample_size": 110000,
                "methodology": "Mixed mode",
                "states_covered": 28
            },
            "published_at": "2024-05-20T19:45:00",
            "color": "#7C3AED"
        },
        {
            "source_name": "India Today-CVoter",
            "prediction_data": {
                "BJP": "289-307",
                "INC": "128-146",
                "Others": "52-62",
                "margin_error": "±4%",
                "sample_size": 105000,
                "methodology": "Telephonic",
                "states_covered": 28
            },
            "published_at": "2024-05-20T20:15:00",
            "color": "#EC4899"
        }
    ]
    
    return exit_polls

@router.get("/comparative")
async def get_comparative_analysis(
    election_id: int = Query(2024, description="Election year")
):
    """Get comparative analysis of all exit polls"""
    
    # Mock data for comparative chart
    return {
        "chart_data": {
            "agencies": [
                "Axis My India",
                "C-Voter",
                "Today's Chanakya",
                "Republic TV",
                "Times Now",
                "India Today"
            ],
            "bjp_min": [295, 287, 305, 290, 285, 289],
            "bjp_max": [315, 305, 325, 310, 300, 307],
            "bjp_average": [305, 296, 315, 300, 292, 298],
            "inc_min": [125, 132, 105, 130, 135, 128],
            "inc_max": [145, 150, 125, 148, 155, 146],
            "inc_average": [135, 141, 115, 139, 145, 137]
        },
        "consensus": {
            "bjp_range": "290-310",
            "inc_range": "130-145",
            "description": "Most polls predict BJP crossing 280 seats, INC improving from 2019",
            "margin_of_error": "±4%",
            "reliability": "High",
            "total_seats": 543
        },
        "trends": {
            "swing_states": [
                {"state": "Uttar Pradesh", "trend": "BJP+", "swing": "+5%"},
                {"state": "West Bengal", "trend": "TMC+", "swing": "+3%"},
                {"state": "Maharashtra", "trend": "Close", "swing": "±2%"}
            ]
        }
    }

@router.get("/constituency/{constituency_id}")
async def get_constituency_exit_poll(
    constituency_id: int,
    election_id: int = Query(2024)
):
    """Get exit poll prediction for a specific constituency"""
    
    # Mock constituency-level prediction
    return {
        "constituency_id": constituency_id,
        "predictions": [
            {
                "source": "Axis My India",
                "winner": "BJP",
                "margin_percentage": 8.5,
                "confidence": "High"
            },
            {
                "source": "C-Voter",
                "winner": "BJP",
                "margin_percentage": 6.2,
                "confidence": "Medium"
            }
        ],
        "consensus": {
            "winner": "BJP",
            "confidence": "High"
        }
    }