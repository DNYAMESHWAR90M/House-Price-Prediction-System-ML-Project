import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# 1. Load dataset (or generate data beforehand using generate_data)df = pd.read_csv("Data/house_prices.csv")
FEATURES = ["Square_Feet", "BHK", "Bathrooms", "Age_Years", "Parking"]
X = df[FEATURES]
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")

# 3. Save Model
pickle.dump(model, open("house_model.pkl", "wb"))
print("Model saved as house_model.pkl")