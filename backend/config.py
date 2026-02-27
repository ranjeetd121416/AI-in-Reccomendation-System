


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_MOVIES = os.path.join(BASE_DIR, "data", "raw", "movies.csv")
DATA_RATINGS = os.path.join(BASE_DIR, "data", "raw", "ratings.csv")

TOP_K = 10
HYBRID_ALPHA = 0.6