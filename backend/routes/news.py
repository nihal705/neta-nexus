from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from backend.database import get_db
from backend.models import News

router = APIRouter()

# Google News RSS feed (free, no API key needed)
NEWS_SOURCES = {
    'india_today': 'https://www.indiatoday.in/rss/india',
    'ndtv': 'https://feeds.feedburner.com/NDTVIndia',
    'the_hindu': 'https://www.thehindu.com/news/national/?service=rss',
    'times_of_india': 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
}

@router.get("/candidate/{candidate_id}")
async def get_candidate_news(candidate_id: int, db: Session = Depends(get_db)):
    """Fetch news articles related to a candidate"""
    
    from backend.models import Candidate
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        return {"news": []}
    
    # Search Google News for candidate name
    search_url = f"https://news.google.com/rss/search?q={candidate.name}+election+candidate&hl=en-IN"
    
    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'xml')
        
        articles = []
        for item in soup.find_all('item')[:10]:
            articles.append({
                'title': item.title.text if item.title else '',
                'link': item.link.text if item.link else '',
                'pub_date': item.pubDate.text if item.pubDate else '',
                'source': 'Google News'
            })
        
        return {"news": articles, "candidate": candidate.name}
    except Exception as e:
        return {"news": [], "error": str(e)}

@router.get("/trending")
async def get_trending_news():
    """Get trending political news"""
    
    try:
        response = requests.get(NEWS_SOURCES['india_today'], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'xml')
        
        articles = []
        for item in soup.find_all('item')[:15]:
            articles.append({
                'title': item.title.text if item.title else '',
                'link': item.link.text if item.link else '',
                'description': item.description.text[:200] if item.description else '',
                'pub_date': item.pubDate.text if item.pubDate else '',
                'source': 'India Today'
            })
        
        return {"articles": articles}
    except Exception as e:
        return {"articles": [], "error": str(e)}