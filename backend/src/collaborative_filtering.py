import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class CollaborativeFiltering:

    def __init__(self, ratings):

        # Create user-item matrix
        self.user_movie = ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)

        # Precompute similarity matrix
        self.similarity = cosine_similarity(self.user_movie)

        # Store movie popularity (for cold start fallback)
        self.movie_popularity = ratings.groupby("movieId")["rating"].mean().sort_values(ascending=False)


    def recommend(self, user_id, top_k=10, n_similar_users=5):

        # Cold start: user not found
        if user_id not in self.user_movie.index:
            return self.movie_popularity.head(top_k).index.tolist()

        user_index = self.user_movie.index.get_loc(user_id)

        similarity_scores = list(enumerate(self.similarity[user_index]))

        # Sort by similarity (excluding self)
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:n_similar_users+1]

        similar_users = [self.user_movie.index[i[0]] for i in similarity_scores]

        # Average ratings of similar users
        similar_users_ratings = self.user_movie.loc[similar_users]
        mean_ratings = similar_users_ratings.mean()

        # Remove movies already rated by target user
        user_rated_movies = self.user_movie.loc[user_id]
        unseen_movies = mean_ratings[user_rated_movies == 0]

        recommendations = unseen_movies.sort_values(ascending=False)

        return recommendations.head(top_k).index.tolist()