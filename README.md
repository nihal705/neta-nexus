# NetaNexus - Political Data Platform (Prototype)

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow.svg)]()
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

## 📋 Overview

**NetaNexus** is a prototype web application for exploring Indian political candidate data. This is a **work in progress** demonstrating the architecture and core functionality of a comprehensive political database platform.

> ⚠️ **DISCLAIMER**: This is an incomplete prototype. Many features are under development, and data is limited.

## 🎯 Current Status

| Feature | Status |
|---------|--------|
| Database Schema | ✅ Complete |
| Basic Search | ✅ Working |
| Candidate Profiles | ✅ Basic |
| State Filtering | ⚠️ Partial |
| Candidate Images | ❌ Not Implemented |
| Complete Data | ❌ In Progress |
| User Authentication | ❌ Not Implemented |
| Live Results | ❌ Not Implemented |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/neta-nexus.git
cd neta-nexus

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
python scripts/setup_database.py

# Start backend
cd ../backend
python -m uvicorn main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

📊 Current Data
Total Candidates: ~69,000

States Covered: 11

Data Sources: ADR, MyNeta, ECI

🛠️ Tech Stack
Layer	Technology
Frontend	React 18, Vite, Tailwind CSS
Backend	FastAPI, Python 3.11
Database	MySQL 8.0
Deployment	Docker Ready

📁 Project Structure
```text
neta-nexus/
├── backend/                 # FastAPI backend
│   ├── routes/             # API endpoints
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   └── main.py             # Entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── hooks/          # Custom hooks
│   └── public/             # Static assets
├── scripts/                # Utility scripts
└── data/                   # Data files (gitignored)
```

🔧 Known Issues
Duplicate candidates in search results

Incomplete state mapping for some candidates

Missing candidate images

Mock data for parliamentary scores

No user authentication

🚧 Roadmap
Complete data import for all states

Fix duplicate candidate issue

Add real candidate images

Implement user authentication

Add live election results

Complete constituency maps

Add news aggregation

📝 License
Proprietary License - All rights reserved. This is a private repository. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.

👨‍💻 Author
NetaNexus Team

⚠️ Disclaimer
This is a prototype and work in progress. The data presented may be incomplete or inaccurate. This project is for demonstration purposes only. All data is sourced from public APIs (ADR, MyNeta, ECI).