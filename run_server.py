#!/usr/bin/env python3
"""
StyleSense - AI Fashion Recommendation Backend Server
Serves API on http://localhost:8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import os

app = FastAPI(title="StyleSense - AI Fashion Recommendation System")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fashion Data
fashion_data = [
    {"name": "Black Hoodie", "category": "casual winter", "price": 1500},
    {"name": "Formal Blazer", "category": "formal office", "price": 3500},
    {"name": "Summer Dress", "category": "summer casual", "price": 2000},
    {"name": "Denim Jacket", "category": "casual winter", "price": 2500},
    {"name": "Traditional Kurta", "category": "ethnic festival", "price": 1800},
    {"name": "Sports Tracksuit", "category": "sports gym", "price": 2200},
    {"name": "Cotton T-Shirt", "category": "casual daily", "price": 800},
    {"name": "Leather Jacket", "category": "casual winter", "price": 4500},
    {"name": "Yoga Pants", "category": "sports gym", "price": 1200},
    {"name": "Party Gown", "category": "formal party", "price": 5000},
]

# User Input Model
class UserInput(BaseModel):
    occasion: str
    weather: str
    budget: int
    style: str

# Recommendation Logic
def recommend_dress(occasion, weather, budget, style):
    recommendations = []
    for item in fashion_data:
        if (
            occasion.lower() in item["category"]
            or weather.lower() in item["category"]
            or style.lower() in item["category"]
        ) and item["price"] <= budget:
            recommendations.append(item)
    
    # If no matches, return random items within budget
    if not recommendations:
        recommendations = [item for item in fashion_data if item["price"] <= budget]
        if recommendations:
            random.shuffle(recommendations)
            recommendations = recommendations[:5]
    
    return recommendations

# API Endpoint for recommendations
@app.post("/recommend")
def get_recommendation(user: UserInput):
    """
    Get fashion recommendations based on user preferences.
    
    Parameters:
    - occasion: Type of occasion (party, office, casual, etc.)
    - weather: Weather condition (summer, winter, rainy, etc.)
    - budget: Maximum budget in rupees
    - style: Style preference (formal, casual, ethnic, etc.)
    """
    result = recommend_dress(
        user.occasion,
        user.weather,
        user.budget,
        user.style
    )
    
    if not result:
        return {"message": "No dresses found within your budget"}
    
    return {"recommended_dresses": result}

# Serve the frontend
@app.get("/", response_class=HTMLResponse)
def get_frontend():
    """Serve the frontend HTML"""
    frontend_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(frontend_path, "r", encoding="utf-8") as f:
        return f.read()

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "StyleSense API is running"}

if __name__ == "__main__":
    import uvicorn
    print("Starting StyleSense API Server...")
    print("Open your browser to: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
