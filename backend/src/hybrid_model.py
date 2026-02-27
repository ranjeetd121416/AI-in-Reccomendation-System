class HybridModel:

    def __init__(self, cf_model, cb_model, alpha=0.6):
        self.cf = cf_model
        self.cb = cb_model
        self.alpha = alpha


    def recommend(self, user_id, seed_movie_id, mood=None, top_k=10):

        # Get recommendations
        cf_recs = self.cf.recommend(user_id, top_k * 2)
        cb_recs = self.cb.recommend(seed_movie_id, top_k * 2)

        # Assign scores
        scores = {}

        # CF scoring
        for rank, movie_id in enumerate(cf_recs):
            score = self.alpha * (1 / (rank + 1))
            scores[movie_id] = scores.get(movie_id, 0) + score

        # CB scoring
        for rank, movie_id in enumerate(cb_recs):
            score = (1 - self.alpha) * (1 / (rank + 1))
            scores[movie_id] = scores.get(movie_id, 0) + score

        # Sort by combined score
        sorted_movies = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [movie_id for movie_id, _ in sorted_movies[:top_k]]