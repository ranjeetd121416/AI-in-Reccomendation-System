def preprocess_data(movies, ratings, min_ratings=20):

    # Work on copies (avoid side effects)
    movies = movies.copy()
    ratings = ratings.copy()

    # Remove missing values
    movies = movies.dropna()
    ratings = ratings.dropna()

    # Filter movies with sufficient ratings
    rating_counts = ratings.groupby("movieId").size()
    popular_movies = rating_counts[rating_counts > min_ratings].index

    ratings = ratings[ratings["movieId"].isin(popular_movies)]
    movies = movies[movies["movieId"].isin(popular_movies)]

    return movies, ratings