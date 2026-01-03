# app.py
# Disaster Alert Fatigue Control System (PS-6)
# Team: Crisis Coders

import streamlit as st
import os

# Import core logic
from logic import (
    calculate_risk,
    calculate_fatigue,
    make_decision,
    generate_explanation
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Disaster Alert Fatigue Control",
    page_icon="🌱",
    layout="centered"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "sound_on" not in st.session_state:
    st.session_state.sound_on = True

# --------------------------------------------------
# Custom CSS (Peaceful Theme)
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom right, #e8f5e9, #f1f8e9);
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #1b5e20;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #388e3c;
        margin-bottom: 25px;
    }
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0px 8px 18px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("<div class='title'>🌱 Disaster Alert Fatigue Control</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Explainable & Responsible AI for Disaster Alerts (PS-6)</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Notification Toggle
# --------------------------------------------------
st.toggle(
    "🔔 Voice Notifications",
    value=st.session_state.sound_on,
    key="sound_on"
)

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📥 Alert Input Parameters")

col1, col2 = st.columns(2)

with col1:
    severity = st.selectbox(
        "🔥 Disaster Severity",
        ["low", "medium", "high"]
    )

with col2:
    area_risk = st.selectbox(
        "📍 Area Risk Level",
        ["low", "medium", "high"]
    )

hours = st.slider(
    "⏱ Hours Since Last Alert",
    min_value=0,
    max_value=10,
    value=2
)

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Decision Button
# --------------------------------------------------
if st.button("🧠 Evaluate Alert Decision", use_container_width=True):

    # Core logic calls
    risk = calculate_risk(severity, area_risk)
    fatigue = calculate_fatigue(hours)
    decision = make_decision(risk, fatigue, severity, area_risk)
    explanation = generate_explanation(decision, severity, area_risk, fatigue)

    # --------------------------------------------------
    # Voice Alert Handling (Safe)
    # --------------------------------------------------
    if st.session_state.sound_on:
        base_path = os.path.dirname(__file__)

        if decision == "SEND":
            audio_path = os.path.join(base_path, "alert_send.wav")
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/wav", autoplay=True)

        elif decision == "DELAY":
            audio_path = os.path.join(base_path, "alert_delay.wav")
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/wav", autoplay=True)
        # SUPPRESS → no sound (intentional)

    # --------------------------------------------------
    # Output Section
    # --------------------------------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Decision & Explanation")

    if decision == "SEND":
        st.success(f"✅ Decision: {decision}")
    elif decision == "DELAY":
        st.warning(f"⚠️ Decision: {decision}")
    else:
        st.info(f"ℹ️ Decision: {decision}")

    st.markdown(explanation)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    "<center style='color:#2e7d32;'>"
    "Team Crisis Coders | Presidency University, Bangalore | PS-6"
    "</center>",
    unsafe_allow_html=True
)
