import streamlit as st
from streamlit_webrtc import webrtc_streamer

from src.data_loader import load_data
from src.recommender import build_similarity, recommend
from src.context_engine import get_context
from src.mood_detector import detect_mood
from src.diversity_engine import diversify
from explanations.explanation_generator import generate_explanation
from utils.ui_components import status_box, recommendation_card


# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="AI YouTube Recommender",
    layout="wide"
)

st.title("🧠 Context-Aware Explainable YouTube Recommendation System")

st.markdown("""
This system recommends videos using:
- Mood Detection
- Time Context Awareness
- User Interest Modeling
- Explainable AI
""")


# ---------------------------------
# SIDEBAR CONTROLS
# ---------------------------------
st.sidebar.header("Demo Controls")

demo_mode = st.sidebar.checkbox("Enable Demo Mode (Cloud Safe)", True)

if demo_mode:
    mood_option = st.sidebar.selectbox(
        "Select Mood (Simulated)",
        ["Happy", "Sad", "Neutral", "Tired", "Angry"]
    )
else:
    mood_option = None


# ---------------------------------
# LOAD DATA
# ---------------------------------
df = load_data()
similarity = build_similarity(df)

video = st.selectbox(
    "Select a video you previously watched:",
    df["title"]
)


# ---------------------------------
# LIVE CAMERA (Only if not demo)
# ---------------------------------
if not demo_mode:
    st.subheader("📷 Live Mood Detection Camera")
    webrtc_streamer(key="camera")


# ---------------------------------
# RECOMMEND BUTTON
# ---------------------------------
if st.button("🚀 Generate Smart Recommendations"):

    col1, col2, col3 = st.columns(3)

    # Mood Detection
    if demo_mode:
        mood = mood_option
    else:
        mood = detect_mood()

    with col1:
        status_box("Detected Mood", mood, "😊")

    # Context Detection
    context = get_context()
    with col2:
        status_box("Context Mode", context, "⏰")

    # System Status
    with col3:
        status_box("AI Engine", "Active", "🤖")

    # Recommendation Logic
    index = df[df["title"] == video].index[0]
    recs = recommend(df, similarity, index)
    recs = diversify(df, recs)

    st.subheader("🎯 Personalized Recommendations")

    for _, row in recs.head(5).iterrows():

        explanation = generate_explanation(
            mood,
            context,
            row["category"]
        )

        recommendation_card(row["title"], explanation)