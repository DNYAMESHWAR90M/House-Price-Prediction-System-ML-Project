# 🏠 DreamHome AI - House Price Prediction System

An end-to-end Machine Learning web application that predicts real estate market valuations using a **Random Forest Regressor**, backed by a **FastAPI** REST API and powered by an interactive **Streamlit** user interface.

---

## 🚀 Features
* **Machine Learning Model:** Trained using Scikit-learn with property features (Square Feet, BHK, Bathrooms, Age, and Parking) achieving high regression accuracy ($R^2$ Score: ~0.86).
* **REST API Backend:** Built with **FastAPI** and **Pydantic** for robust, high-performance data validation and prediction endpoints.
* **Modern Web Frontend:** Interactive dashboard built using **Streamlit** featuring property sliders, dynamic insights, price-per-sq.ft calculation, and instant CSV report downloads.
* **Model Serialization:** Uses `pickle` for model persistence (`house_model.pkl`).

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** Streamlit
* **Styling & Layout:** Custom CSS, HTML/Markdown

---

## 📂 Project Structure
```text
House_Price_Project/
│
├── Data/
│   └── house_prices.csv        # Dataset used for training
├── templates/
│   └── index.html              # FastAPI default HTML template
├── train.py                    # Script to train and save the ML model
├── predict.py                  # CLI script for command-line predictions
├── api.py                      # FastAPI backend server
├── app.py                      # Streamlit frontend web application
├── house_model.pkl             # Serialized Machine Learning model
├── requirements.txt            # Project dependencies
└── README.md                   # Project Documentation
