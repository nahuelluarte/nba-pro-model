import streamlit as st
import numpy as np
import pandas as pd
from math import erf, sqrt

st.set_page_config(page_title="NBA Player Points – Pro Model", layout="wide")

st.title("🏀 NBA Player Points – Statistical Probability Model (PRO)")
st.caption("Statistical analysis only • No betting • No odds")

st.header("📥 Player Data")

c1, c2, c3 = st.columns(3)

with c1:
    pts_avg = st.number_input("Season avg points", 0.0, 50.0, 22.5)
    minutes_avg = st.number_input("Avg minutes", 0.0, 48.0, 34.0)
    usage = st.slider("Usage rate (%)", 10, 40, 25)

with c2:
    pts_last5 = st.number_input("Last 5 games avg points", 0.0, 50.0, 24.0)
    minutes_proj = st.number_input("Projected minutes", 0.0, 48.0, 35.0)

with c3:
    injury_status = st.selectbox(
        "Injury status",
        ["Healthy", "Minor issue", "Questionable", "Limited"]
    )
    home_away = st.selectbox("Game location", ["Home", "Away"])

st.header("🛡️ Opponent Context")

d1, d2, d3 = st.columns(3)

with d1:
    defense = st.selectbox(
        "Opponent defense vs position",
        ["Elite", "Good", "Average", "Weak", "Very Weak"]
    )

with d2:
    pace = st.selectbox(
        "Opponent pace",
        ["Very Slow", "Slow", "Average", "Fast", "Very Fast"]
    )

with d3:
    blowout = st.slider("Blowout risk (%)", 0, 40, 10)

line = st.number_input("Reference points line", 0.0, 50.0, pts_avg)

injury_factor = {
    "Healthy": 1.00,
    "Minor issue": 0.96,
    "Questionable": 0.88,
    "Limited": 0.78
}

defense_factor = {
    "Elite": 0.88,
    "Good": 0.94,
    "Average": 1.00,
    "Weak": 1.06,
    "Very Weak": 1.12
}

pace_factor = {
    "Very Slow": 0.92,
    "Slow": 0.96,
    "Average": 1.00,
    "Fast": 1.05,
    "Very Fast": 1.10
}

home_factor = 1.03 if home_away == "Home" else 0.97
blowout_factor = 1 - (blowout / 100) * 0.25

base_pts = pts_avg * 0.6 + pts_last5 * 0.4
minutes_factor = minutes_proj / minutes_avg if minutes_avg > 0 else 1

expected_pts = (
    base_pts
    * minutes_factor
    * (usage / 25)
    * injury_factor[injury_status]
    * defense_factor[defense]
    * pace_factor[pace]
    * home_factor
    * blowout_factor
)

std_dev = max(4.5, expected_pts * 0.22)

def normal_cdf(x, mu, sigma):
    return 0.5 * (1 + erf((x - mu) / (sigma * sqrt(2))))

prob_over = 1 - normal_cdf(line, expected_pts, std_dev)
prob_under = 1 - prob_over

st.header("📊 Model Output")

df = pd.DataFrame({
    "Metric": [
        "Expected Points",
        "Std Deviation",
        "Over Probability",
        "Under Probability"
    ],
    "Value": [
        round(expected_pts, 2),
        round(std_dev, 2),
        f"{prob_over:.2%}",
        f"{prob_under:.2%}"
    ]
})

st.dataframe(df, use_container_width=True)

st.caption("Statistical model for analysis only. No betting or guarantees.")
