import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="House Price Prediction API")

# Load trained model
model = pickle.load(open("house_model.pkl", "rb"))

# Advanced Neighborhood Multipliers & Details
LOCATION_DATA = {
    "Suburbs (Standard)": {"multiplier": 1.0, "type": "Residential", "growth": "Moderate"},
    "City Center (Prime Location)": {"multiplier": 1.25, "type": "Commercial/Hub", "growth": "High"},
    "IT Park / Tech Zone": {"multiplier": 1.35, "type": "Tech Corridor", "growth": "Very High"},
    "Greenwood Outskirts": {"multiplier": 0.9, "type": "Eco-Friendly / Quiet", "growth": "Developing"}
}

class House(BaseModel):
    Square_Feet: int = Field(..., ge=300, le=10000, example=1500)
    BHK: int = Field(..., ge=1, le=10, example=3)
    Bathrooms: int = Field(..., ge=1, le=10, example=2)
    Age_Years: int = Field(..., ge=0, le=50, example=5)
    Parking: int = Field(..., ge=0, le=5, example=1)
    Location: str = Field(..., example="City Center (Prime Location)")

@app.get("/")
def home():
    return {"message": "Welcome to House Price Prediction API"}

@app.post("/predict")
def predict(house: House):
    data = pd.DataFrame([{
        "Square_Feet": house.Square_Feet,
        "BHK": house.BHK,
        "Bathrooms": house.Bathrooms,
        "Age_Years": house.Age_Years,
        "Parking": house.Parking
    }])

    base_price = float(model.predict(data)[0])
    
    # Get location info
    loc_info = LOCATION_DATA.get(house.Location, {"multiplier": 1.0, "type": "Standard", "growth": "Normal"})
    final_price = base_price * loc_info["multiplier"]

    return {
        "estimated_price": round(final_price, 2),
        "formatted_price": f"₹ {final_price:,.2f}",
        "location_type": loc_info["type"],
        "market_growth": loc_info["growth"],
        "applied_multiplier": loc_info["multiplier"]
    }