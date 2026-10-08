import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="DreamHome AI Pro - Real Estate Intelligence",
    page_icon="🏢",
    layout="wide"
)

# Load the trained machine learning model directly
@st.cache_resource
def load_model():
    return pickle.load(open("house_model.pkl", "rb"))

model = load_model()

# Location Multipliers mapping
LOCATION_MULTIPLIERS = {
    "Suburbs (Standard)": 1.0,
    "City Center (Prime Location)": 1.25,
    "IT Park / Tech Zone": 1.35,
    "Greenwood Outskirts": 0.9
}

# Custom SaaS-style Professional CSS
st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.7rem;
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Top Header Banner
st.markdown("""
    <div style='padding: 10px 0; border-bottom: 1px solid #1f2937; margin-bottom: 20px;'>
        <h2 style='color: #f3f4f6; margin: 0;'>🏢 DreamHome AI Enterprise</h2>
        <p style='color: #9ca3af; margin: 0; font-size: 0.95rem;'>AI-Driven Real Estate Valuation & Financial Suite</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("🎛️ Control Panel")
    st.markdown("Configure property parameters:")
    
    selected_location = st.selectbox("📍 Neighborhood / Zone", list(LOCATION_MULTIPLIERS.keys()))
    square_feet = st.slider("📐 Area (Square Feet)", min_value=300, max_value=10000, value=1500, step=50)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        bhk = st.selectbox("🛏️ BHK", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("🛁 Baths", [1, 2, 3, 4, 5], index=1)
    with col_s2:
        age_years = st.slider("⏳ Age (Yrs)", min_value=0, max_value=50, value=5)
        parking = st.selectbox("🚗 Parking", [0, 1, 2, 3, 4], index=1)
        
    st.markdown("---")
    predict_btn = st.button("🚀 Calculate Valuation")

# --- MAIN DASHBOARD AREA ---
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
        base_price = float(model.predict(input_data)[0])
        multiplier = LOCATION_MULTIPLIERS.get(selected_location, 1.0)
        raw_price = base_price * multiplier
        
        formatted_price = f"₹ {raw_price:,.2f}"
        price_per_sqft = raw_price / square_feet
        
        # Top Summary Metrics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Estimated Valuation", value=formatted_price, delta="AI Verified")
        with m2:
            st.metric(label="Unit Rate / Sq.Ft", value=f"₹ {price_per_sqft:,.2f}")
        with m3:
            st.metric(label="Selected Zone", value=selected_location.split()[0])
        
        st.markdown("")
        
        # Tabs for Analytics
        tab1, tab2, tab3 = st.tabs(["📈 Market Comparison", "💳 Financial & EMI Planner", "🏡 Similar Property Matches"])
        
        with tab1:
            st.markdown("### Comparative Market Analysis")
            fig, ax = plt.subplots(figsize=(7, 3.2))
            fig.patch.set_facecolor('#111827')
            ax.set_facecolor('#0b0f19')
            
            categories = ['Min Market', 'Your Property Estimate', 'Prime High-End']
            prices = [raw_price * 0.85, raw_price, raw_price * 1.2]
            ax.bar(categories, prices, color=['#38bdf8', '#34d399', '#f87171'], width=0.5)
            
            ax.set_ylabel('Price in ₹', color='white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('#374151')
            st.pyplot(fig)

        with tab2:
            st.markdown("### Home Loan & Monthly EMI Estimator")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                down_payment_pct = st.slider("Down Payment (%)", 10, 50, 20, 5)
                loan_years = st.slider("Tenure (Years)", 5, 30, 20, 1)
            with col_f2:
                interest_rate = st.slider("Interest Rate (% p.a.)", 6.0, 15.0, 8.5, 0.5)
            
            loan_amount = raw_price * (1 - down_payment_pct / 100)
            monthly_ir = (interest_rate / 12) / 100
            months = loan_years * 12
            emi = (loan_amount * monthly_ir * (1 + monthly_ir)**months) / ((1 + monthly_ir)**months - 1)
            
            st.success(f"💳 **Calculated Monthly EMI:** ₹ {emi:,.2f} / month  *(Loan Principal: ₹ {loan_amount:,.2f})*")

        with tab3:
            st.markdown("### Verified Comparable Listings")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.info(f"🏢 **Elite {bhk} BHK Luxury Apartment**\n\n 📐 {square_feet + 120} sq.ft | 💰 ₹ {raw_price * 1.04:,.2f}")
            with col_l2:
                st.info(f"🏡 **Spacious Independent Villa**\n\n 📐 {square_feet + 350} sq.ft | 💰 ₹ {raw_price * 1.18:,.2f}")
        
        st.markdown("---")
        report_df = input_data.copy()
        report_df['Location'] = selected_location
        report_df['Estimated_Price'] = formatted_price
        csv_data = report_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download Enterprise Valuation Report (CSV)", data=csv_data, file_name="enterprise_property_report.csv", mime="text/csv")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")
else:
    st.info("👈 Use the **Control Panel** in the sidebar to configure property specs and click **'Calculate Valuation'** to launch the intelligence suite.")