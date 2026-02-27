import pandas as pd


def load_data(movies_path, ratings_path):

    try:
        movies = pd.read_csv(movies_path)
        ratings = pd.read_csv(ratings_path)

        # Basic validation
        required_movie_cols = {"movieId", "title", "genres"}
        required_rating_cols = {"userId", "movieId", "rating"}

        if not required_movie_cols.issubset(movies.columns):
            raise ValueError("Movies file missing required columns")

        if not required_rating_cols.issubset(ratings.columns):
            raise ValueError("Ratings file missing required columns")

        return movies, ratings

    except Exception as e:
        raise RuntimeError(f"Error loading data: {str(e)}")