import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("carbon_model.pkl")

st.set_page_config(
    page_title="EcoTrack AI",
    page_icon="🌍",
    layout="centered"
)

# -------- CUSTOM CSS --------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.stButton>button {
    background: linear-gradient(90deg, #00C9A7, #92FE9D);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stSlider label, .stSelectbox label {
    font-weight: bold;
}
.result-card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: black;
    font-size: 18px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.title("🌍 EcoTrack AI")
st.caption("Carbon Footprint Estimator ")

st.divider()

st.subheader("Enter Your Lifestyle Details")

# -------- INPUT SECTION --------
transport = st.slider("🚗 Monthly Transport Distance (km)", 0, 100, 20)
electricity = st.slider("⚡ Monthly Electricity Usage (kWh)", 50, 1000, 300)
flights = st.slider("✈ Flights Per Year", 0, 20, 2)
diet = st.selectbox("🥗 Diet Type", ["Vegetarian", "Non-Vegetarian"])
shopping = st.slider("🛍 Shopping Frequency Score (1-10)", 1, 10, 5)

diet_value = 0 if diet == "Vegetarian" else 1

st.divider()

# -------- PREDICTION --------
if st.button("🌱 Calculate My Carbon Footprint"):

    input_data = np.array([[transport, electricity, flights, diet_value, shopping]])
    prediction = model.predict(input_data)[0]

    # Eco Category
    if prediction < 1000:
        category = "Low Impact 🌱"
        color = "#00C897"
    elif prediction < 2000:
        category = "Medium Impact ⚖"
        color = "#FFC300"
    else:
        category = "High Impact 🔥"
        color = "#FF4B4B"

    # Result Card
    st.markdown(f"""
    <div class="result-card">
        <b>Estimated Carbon Emission:</b> {prediction:.2f} kg <br><br>
        <b>Eco Category:</b> <span style="color:{color}; font-weight:bold;">{category}</span>
    </div>
    """, unsafe_allow_html=True)

    # Eco Score
    eco_score = max(0, 100 - (prediction / 3000 * 100))
    st.subheader("🌎 Eco Score")
    st.progress(int(eco_score))
    st.write(f"Your Sustainability Score: **{eco_score:.1f}/100**")

    # Breakdown
    st.subheader("📊 Emission Breakdown")

    breakdown = {
        "Transport": transport * 0.21,
        "Electricity": electricity * 0.5,
        "Flights": flights * 90,
        "Diet": diet_value * 200,
        "Shopping": shopping * 15
    }

    st.bar_chart(breakdown)

    # Smart Recommendations
    st.subheader("💡 Personalized Recommendations")

    if flights > 3:
        st.write("✈ Consider reducing air travel or using carbon offset programs.")
    if electricity > 400:
        st.write("⚡ Switch to energy-efficient appliances and turn off idle devices.")
    if diet_value == 1:
        st.write("🥗 Reducing meat consumption can significantly lower emissions.")
    if transport > 40:
        st.write("🚲 Use public transport, carpooling, or cycling when possible.")

    st.success("🌍 Small lifestyle changes create big environmental impact!")