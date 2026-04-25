from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from datetime import datetime
import random

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting: {e}")

manager = ConnectionManager()

@router.websocket("/live-results")
async def websocket_live_results(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Initial data
    results = {
        "bjp": 245,
        "inc": 142,
        "others": 156,
        "timestamp": datetime.now().isoformat(),
        "total_seats": 543
    }
    
    try:
        while True:
            # Simulate random updates (in production, fetch from ECI)
            results["bjp"] += random.randint(-2, 3)
            results["inc"] += random.randint(-1, 2)
            results["others"] = 543 - results["bjp"] - results["inc"]
            results["timestamp"] = datetime.now().isoformat()
            
            await manager.broadcast(results)
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)