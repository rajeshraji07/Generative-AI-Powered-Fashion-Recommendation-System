# StyleSense - Dynamic AI Fashion Recommendation System
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import openai
import json

# Set your OpenAI API key in environment variable first
# Linux/Mac: export OPENAI_API_KEY="your_api_key"
# Windows: setx OPENAI_API_KEY "your_api_key"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
# User Input Model
# -----------------------------
class UserInput(BaseModel):
    occasion: str
    weather: str
    budget: int
    style: str

# -----------------------------
# Fetch Fashion Data from AI
# -----------------------------
def fetch_fashion_from_ai(prompt: str):
    """
    Calls OpenAI API and generates fashion items dynamically.
    Returns a list of dictionaries with 'name', 'category', 'price'.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fashion recommendation AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        text = response.choices[0].message.content.strip()
        
        # Try to parse JSON from AI response
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # fallback: parse line by line if AI didn't return strict JSON
            data = []
            for line in text.split("\n"):
                parts = line.split(",")
                if len(parts) >= 3:
                    name, category, price = parts[:3]
                    try:
                        data.append({"name": name.strip(), "category": category.strip(), "price": int(price.strip())})
                    except:
                        continue
        return data
    except Exception as e:
        print("AI API Error:", e)
        return []

# -----------------------------
# API Endpoint - Recommend Fashion
# -----------------------------
@app.post("/recommend")
def get_recommendation(user: UserInput):
    prompt = (
        f"Generate 5 fashion items for occasion '{user.occasion}', "
        f"weather '{user.weather}', style '{user.style}', with max budget {user.budget}. "
        "Return a JSON list of objects with 'name', 'category', and 'price'."
    )
    recommendations = fetch_fashion_from_ai(prompt)
    if not recommendations:
        return {"message": "No dresses found from AI"}
    return {"recommended_dresses": recommendations}

# -----------------------------
# Frontend + Backend Together
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>StyleSense AI</title></head>
    <body style="font-family: Arial; text-align:center;">
        <h2>StyleSense AI Fashion Recommendation</h2>

        <input id="occasion" placeholder="Occasion"><br><br>
        <input id="weather" placeholder="Weather"><br><br>
        <input id="budget" type="number" placeholder="Budget"><br><br>
        <input id="style" placeholder="Style"><br><br>

        <button onclick="getRecommendation()">Get AI Recommendation</button>

        <h3>Result:</h3>
        <div id="result"></div>

        <script>
        async function getRecommendation() {
            const response = await fetch("/recommend", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
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
