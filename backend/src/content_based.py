from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ContentBased:

    def __init__(self, movies):

        self.movies = movies.reset_index(drop=True)

        # Create movieId → index mapping for fast lookup
        self.movie_id_to_index = {
            movie_id: idx
            for idx, movie_id in enumerate(self.movies["movieId"])
        }

        # TF-IDF on genres
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.movies["genres"].fillna("")
        )

        # Precompute similarity matrix
        self.similarity = cosine_similarity(self.tfidf_matrix)


    def recommend(self, seed_movie_id, top_k=10):

        # Cold start handling
        if seed_movie_id not in self.movie_id_to_index:
            return self.movies["movieId"].sample(top_k).tolist()

        idx = self.movie_id_to_index[seed_movie_id]

        similarity_scores = list(enumerate(self.similarity[idx]))

        # Sort by similarity score
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:top_k+1]

        recommended_ids = [
            self.movies.iloc[i[0]]["movieId"]
            for i in similarity_scores
        ]

        return recommended_ids