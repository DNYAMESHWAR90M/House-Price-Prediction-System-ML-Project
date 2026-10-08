import pickle
import pandas as pd

# 1. Load the trained machine learning model from the pickle file
model = pickle.load(open("house_model.pkl", "rb"))

# 2. Define the input features for a sample house (Square Feet, BHK, Bathrooms, Age, Parking)
house = pd.DataFrame([{
    "Square_Feet": 1500,
    "BHK": 3,
    "Bathrooms": 2,
    "Age_Years": 5,
    "Parking": 1
}])

# 3. Predict the house price using the trained model
predicted_price = model.predict(house)[0]

# 4. Display the estimated price in the console
print(f"Estimated House Price: ₹ {predicted_price:,.2f}")
