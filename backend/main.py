from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from config import *
from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.collaborative_filtering import CollaborativeFiltering
from src.content_based import ContentBased
from src.hybrid_model import HybridModel
from src.context_engine import apply_context
from src.diversity_engine import diversify
from src.mood_detector import detect_mood
from explanations.explanation_generator import generate_explanation

app = FastAPI(title="Context-Aware OTT Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- LOAD DATA ONCE ----------
movies, ratings = load_data(DATA_MOVIES, DATA_RATINGS)
movies, ratings = preprocess_data(movies, ratings)

cf_model = CollaborativeFiltering(ratings)
cb_model = ContentBased(movies)
hybrid_model = HybridModel(cf_model, cb_model, alpha=HYBRID_ALPHA)


# ---------- REQUEST MODEL ----------
class RecommendationRequest(BaseModel):
    user_id: int
    seed_movie_id: int
    image: str | None = None
    top_k: int = 10


# ---------- ROUTE ----------
@app.post("/recommend")
def recommend(req: RecommendationRequest):

    # 1️⃣ Debug: Check if image received
    print("Image received:", req.image is not None)

    # 2️⃣ Detect mood from image
    mood = detect_mood(req.image)

    # 3️⃣ Detect time context
    current_hour = datetime.now().hour
    time_context = "academic" if 9 <= current_hour <= 17 else "leisure"

    print("Detected mood:", mood)
    print("Time context:", time_context)

    # 4️⃣ Hybrid recommendation
    hybrid_ids = hybrid_model.recommend(
        user_id=req.user_id,
        seed_movie_id=req.seed_movie_id,
        top_k=req.top_k
    )

    # 5️⃣ Apply contextual ranking
    context_movies = apply_context(
        movies_df=movies,
        movie_ids=hybrid_ids,
        mood=mood,
        time_context=time_context
    )

    # 6️⃣ Diversity enhancement
    final_movies = diversify(context_movies) if context_movies else []

    # 7️⃣ Build response
    results = [
        {
            "title": movie["title"],
            "genres": movie["genres"],
            "explanation": generate_explanation(movie, mood, time_context)
        }
        for movie in final_movies
    ]

    return {
        "detected_mood": mood,
        "time_context": time_context,
        "recommendations": results
    }