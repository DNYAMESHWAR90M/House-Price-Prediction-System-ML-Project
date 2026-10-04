import streamlit as st
import pickle
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="DreamHome AI - House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Load the trained machine learning model directly
@st.cache_resource
def load_model():
    return pickle.load(open("house_model.pkl", "rb"))

model = load_model()

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff3333 0%, #ff7722 100%);
        color: white;
    }
    .metric-card {
        background-color: #1e2530;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #303846;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("🏠 DreamHome AI: House Price Predictor")
st.markdown("Get accurate, instant real estate market valuations powered by Machine Learning.")
st.markdown("---")

# Layout Split: Two Columns
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.subheader("📝 Enter Property Details")
    
    square_feet = st.slider("Square Feet Area", min_value=300, max_value=10000, value=1500, step=50)
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        bhk = st.selectbox("BHK (Bedrooms)", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
    with sub_col2:
        age_years = st.slider("Age of Property (Years)", min_value=0, max_value=50, value=5)
        parking = st.selectbox("Parking Spaces", [0, 1, 2, 3, 4], index=1)
        
    st.markdown("")
    predict_btn = st.button("🔮 Calculate Estimated Price")

with col2:
    st.subheader("📊 Valuation & Insights")
    
    if predict_btn:
        # Prepare input data for the model
        input_data = pd.DataFrame([{
            "Square_Feet": square_feet,
            "BHK": int(bhk),
            "Bathrooms": int(bathrooms),
            "Age_Years": age_years,
            "Parking": int(parking)
        }])
        
        try:
            # Direct prediction using the loaded model
            raw_price = float(model.predict(input_data)[0])
            formatted_price = f"₹ {raw_price:,.2f}"
            
            # Display Result Card
            st.markdown(f"""
                <div class="metric-card">
                    <p style='color: #a0aec0; font-size: 1.1rem; margin-bottom: 0;'>Estimated Market Value</p>
                    <h1 style='color: #48bb78; font-size: 2.6rem; margin-top: 10px;'>{formatted_price}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Extra Financial Metrics
            price_per_sqft = raw_price / square_feet
            st.markdown("### Key Metrics")
            st.info(f"📌 **Price per Sq.Ft:** ₹ {price_per_sqft:,.2f} / sq.ft")
            st.success(f"🏡 **Configuration:** {bhk} BHK • {bathrooms} Baths • {parking} Parking • {age_years} Yrs Old")
            
            # Download Valuation Report Button
            report_df = input_data.copy()
            report_df['Estimated_Price'] = formatted_price
            csv_data = report_df.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 Download Valuation Report (CSV)",
                data=csv_data,
                file_name="house_valuation_report.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Prediction Error: {e}")
    else:
        st.info("👈 Adjust the property parameters on the left and click **'Calculate Estimated Price'** to view the live valuation report.")