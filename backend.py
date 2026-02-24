# StyleSense - Simple Generative AI Fashion Recommendation System
# Backend - Single File (Easy Version)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI(title="StyleSense - AI Fashion Recommendation System")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Enhanced Fashion Data
# -----------------------------
fashion_data = [
    {"name": "Black Hoodie", "category": "casual winter", "price": 1500, "brand": "UrbanStyle", "stock": 25, "description": "Comfortable cotton blend hoodie perfect for winter"},
    {"name": "Formal Blazer", "category": "formal office", "price": 3500, "brand": "Executive", "stock": 15, "description": "Premium blazer for professional settings"},
    {"name": "Summer Dress", "category": "summer casual", "price": 2000, "brand": "Breeze", "stock": 30, "description": "Light and airy summer dress"},
    {"name": "Denim Jacket", "category": "casual winter", "price": 2500, "brand": "DenimCo", "stock": 20, "description": "Classic denim jacket with modern fit"},
    {"name": "Traditional Kurta", "category": "ethnic festival", "price": 1800, "brand": "Heritage", "stock": 18, "description": "Traditional kurta with contemporary design"},
    {"name": "Sports Tracksuit", "category": "sports gym", "price": 2200, "brand": "FitPro", "stock": 22, "description": "Performance tracksuit for active lifestyle"},
    {"name": "Cotton T-Shirt", "category": "casual daily", "price": 800, "brand": "BasicWear", "stock": 50, "description": "Essential cotton t-shirt for everyday wear"},
    {"name": "Leather Jacket", "category": "casual winter", "price": 4500, "brand": "RockStyle", "stock": 10, "description": "Premium leather jacket with attitude"},
    {"name": "Yoga Pants", "category": "sports gym", "price": 1200, "brand": "FlexFit", "stock": 35, "description": "Stretchy and comfortable yoga pants"},
    {"name": "Party Gown", "category": "formal party", "price": 5000, "brand": "Glamour", "stock": 8, "description": "Elegant gown for special occasions"},
    {"name": "Casual Jeans", "category": "casual daily", "price": 1800, "brand": "DenimCo", "stock": 40, "description": "Comfortable slim-fit jeans"},
    {"name": "Winter Coat", "category": "formal winter", "price": 6000, "brand": "WarmStyle", "stock": 12, "description": "Luxurious winter coat with premium insulation"}
]

# -----------------------------
# User Input Model
# -----------------------------
class UserInput(BaseModel):
    occasion: str
    weather: str
    budget: int
    style: str

# -----------------------------
# AI Recommendation Logic (Simple Matching Algorithm)
# -----------------------------
def recommend_dress(occasion, weather, budget, style):
    recommendations = []

    for item in fashion_data:
        if (
            occasion.lower() in item["category"]
            or weather.lower() in item["category"]
            or style.lower() in item["category"]
        ):
            if item["price"] <= budget:
                recommendations.append(item)

    return recommendations

# -----------------------------
# Trend Generator (AI Simulation)
# -----------------------------
def generate_trend():
    trends = [
        "Oversized fashion is trending in 2026.",
        "Minimal style is becoming popular.",
        "Earth tone colors dominate this season.",
        "Layered outfits are in high demand.",
        "Streetwear style is trending now."
    ]
    return random.choice(trends)

# -----------------------------
# Confidence Score Generator
# -----------------------------
def ai_confidence():
    return str(random.randint(85, 99)) + "%"

# -----------------------------
# API - Recommend Endpoint
# -----------------------------
@app.post("/recommend")
def get_recommendation(user: UserInput):

    result = recommend_dress(
        user.occasion,
        user.weather,
        user.budget,
        user.style
    )

    if not result:
        return {"message": "No dresses found within your budget"}

    return {
        "recommended_dresses": result,
        "trend_insight": generate_trend(),
        "ai_confidence": ai_confidence()
    }

# -----------------------------
# API - Search Dress
# -----------------------------
@app.get("/search")
def search_dress(name: str):
    result = [
        item for item in fashion_data
        if name.lower() in item["name"].lower()
    ]

    if not result:
        return {"message": "Dress not found"}

    return {"search_result": result}

# -----------------------------
# API - Get Categories
# -----------------------------
@app.get("/categories")
def get_categories():
    categories = list(set([item["category"] for item in fashion_data]))
    return {"categories": categories}

# -----------------------------
# API - Filter by Price Range
# -----------------------------
@app.get("/filter")
def filter_items(min_price: int = 0, max_price: int = 10000, category: str = None):
    filtered = [
        item for item in fashion_data
        if min_price <= item["price"] <= max_price
    ]
    
    if category:
        filtered = [item for item in filtered if category.lower() in item["category"].lower()]
    
    return {"items": filtered, "count": len(filtered)}

# -----------------------------
# API - Get Item Details
# -----------------------------
@app.get("/item/{item_name}")
def get_item_details(item_name: str):
    for item in fashion_data:
        if item["name"].lower() == item_name.lower():
            return item
    return {"message": "Item not found"}

# -----------------------------
# Get All Fashion Items
# -----------------------------
@app.get("/items")
def get_all_items():
    return {"items": fashion_data}

# -----------------------------
# Serve Frontend
# -----------------------------
@app.get("/frontend")
def serve_frontend():
    return FileResponse("index.html")

# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to StyleSense AI Fashion Recommendation System"}