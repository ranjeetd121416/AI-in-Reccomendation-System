import pandas as pd

def load_data():
    movies = pd.read_csv("data/raw/movies.csv")
    ratings = pd.read_csv("data/raw/ratings.csv")

    df = ratings.merge(movies, on="movieId")
    df.rename(columns={"genres": "category"}, inplace=True)

    return df