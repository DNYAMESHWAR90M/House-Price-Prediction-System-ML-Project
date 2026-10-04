import pickle
import pandas as pd
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="House Price Prediction API")

# Load trained model
model = pickle.load(open("house_model.pkl", "rb"))

# Pydantic validation for input data
class House(BaseModel):
    Square_Feet: int = Field(..., ge=300, le=10000, example=1500)
    BHK: int = Field(..., ge=1, le=10, example=3)
    Bathrooms: int = Field(..., ge=1, le=10, example=2)
    Age_Years: int = Field(..., ge=0, le=50, example=5)
    Parking: int = Field(..., ge=0, le=5, example=1)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Updated TemplateResponse syntax for newer Starlette/Jinja versions
    return templates.TemplateResponse(request, "index.html")

@app.post("/predict")
def predict(house: House):
    data = pd.DataFrame([{
        "Square_Feet": house.Square_Feet,
        "BHK": house.BHK,
        "Bathrooms": house.Bathrooms,
        "Age_Years": house.Age_Years,
        "Parking": house.Parking
    }])

    price = float(model.predict(data)[0])
    return {
        "estimated_price": round(price, 2),
        "formatted_price": f"₹ {price:,.2f}"
    }