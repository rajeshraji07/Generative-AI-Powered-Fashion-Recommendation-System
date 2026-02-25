# StyleSense - Simple Generative AI Fashion Recommendation System
# Backend + Frontend in Single File Version

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random

app = FastAPI(title="StyleSense - AI Fashion Recommendation System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Fashion Data
# -----------------------------
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

# -----------------------------
# User Input Model
# -----------------------------
class UserInput(BaseModel):
    occasion: str
    weather: str
    budget: int
    style: str

# -----------------------------
# Recommendation Logic
# -----------------------------
def recommend_dress(occasion, weather, budget, style):
    recommendations = []

    for item in fashion_data:
        if (
            occasion.lower() in item["category"]
            or weather.lower() in item["category"]
            or style.lower() in item["category"]
        ) and item["price"] <= budget:
            recommendations.append(item)

    return recommendations

# -----------------------------
# API Endpoint
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

    return {"recommended_dresses": result}

# -----------------------------
# Frontend + Backend Together
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>StyleSense AI</title>
    </head>
    <body style="font-family: Arial; text-align:center;">

        <h2>StyleSense AI Fashion Recommendation</h2>

        <input id="occasion" placeholder="Occasion"><br><br>
        <input id="weather" placeholder="Weather"><br><br>
        <input id="budget" type="number" placeholder="Budget"><br><br>
        <input id="style" placeholder="Style"><br><br>

        <button onclick="getRecommendation()">Get Recommendation</button>

        <h3>Result:</h3>
        <div id="result"></div>

        <script>
        async function getRecommendation() {

            const response = await fetch("/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    occasion: document.getElementById("occasion").value,
                    weather: document.getElementById("weather").value,
                    budget: parseInt(document.getElementById("budget").value),
                    style: document.getElementById("style").value
                })
            });

            const data = await response.json();
            document.getElementById("result").innerHTML =
                "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
        }
        </script>

    </body>
    </html>
    """

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)