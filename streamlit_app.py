import streamlit as st
import joblib
import json
import numpy as np

# Page config
st.set_page_config(
    page_title="Football Player Wage Predictor", page_icon="⚽", layout="centered"
)

# Custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        }
        .title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00d2ff, #7b2ff7, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            text-align: center;
            color: #a0a0b0;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        .result-box {
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-top: 1.5rem;
            background: linear-gradient(135deg, #00b09b, #96c93d);
            box-shadow: 0 8px 32px rgba(0, 176, 155, 0.4);
        }
        .result-label {
            font-size: 2rem;
            font-weight: 800;
            color: white;
        }
        .result-sub {
            font-size: 1rem;
            color: rgba(255,255,255,0.85);
            margin-top: 0.5rem;
        }
        .info-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
            color: #c0c0d0;
            font-size: 0.9rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Load model and features
@st.cache_resource
def load_model():
    model = joblib.load("wage_predictor_model.pkl")
    with open("model_features.json", "r") as f:
        features = json.load(f)
    return model, features


model, features = load_model()

# Header
st.markdown('<div class="title">⚽ Player Wage Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Enter a player\'s stats to predict their weekly wage</div>',
    unsafe_allow_html=True,
)

# Input fields
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (16 - 45)", min_value=16, max_value=45, value=25)
    overall = st.number_input(
        "Overall Rating (50 - 99)", min_value=50, max_value=99, value=75
    )
    potential = st.number_input(
        "Potential (50 - 99)", min_value=50, max_value=99, value=80
    )
    value_eur = st.number_input(
        "Market Value in € (0 - 200,000,000)",
        min_value=0,
        max_value=200000000,
        value=1000000,
        step=100000,
    )
    pace = st.number_input("Pace (0 - 99)", min_value=0, max_value=99, value=70)

with col2:
    shooting = st.number_input("Shooting (0 - 99)", min_value=0, max_value=99, value=70)
    passing = st.number_input("Passing (0 - 99)", min_value=0, max_value=99, value=70)
    dribbling = st.number_input(
        "Dribbling (0 - 99)", min_value=0, max_value=99, value=70
    )
    defending = st.number_input(
        "Defending (0 - 99)", min_value=0, max_value=99, value=50
    )
    physic = st.number_input("Physic (0 - 99)", min_value=0, max_value=99, value=70)

# Calculate engineered features
overall_per_age = overall / age
potential_gap = potential - overall
attacking_avg = (shooting + dribbling + pace) / 3
defensive_avg = (defending + physic) / 2
overall_squared = overall**2

# Predict
if st.button("Predict Wage", use_container_width=True):
    input_data = np.array(
        [
            [
                age,
                overall,
                potential,
                value_eur,
                pace,
                shooting,
                passing,
                dribbling,
                defending,
                physic,
                overall_per_age,
                potential_gap,
                attacking_avg,
                defensive_avg,
                overall_squared,
            ]
        ]
    )

    predicted_wage = model.predict(input_data)[0]

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">💰 €{predicted_wage:,.0f} / week</div>
            <div class="result-sub">Estimated weekly wage based on player stats</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

# Info card
st.markdown(
    """
    <div class="info-card">
        📊 <b>Model:</b> Gradient Boosting &nbsp;|&nbsp;
        🎯 <b>MAE:</b> €3,744 &nbsp;|&nbsp;
        📁 <b>Dataset:</b> FIFA 22 (17k players)
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-card" style="text-align: center; margin-top: 1rem;">
        ⚠️ <b>Disclaimer:</b> This tool is for educational and portfolio purposes only.
    </div>
""",
    unsafe_allow_html=True,
)
