from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity(df):

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["category"])

    return cosine_similarity(matrix)


def recommend(df, similarity, index, top_n=10):

    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    movie_indices = [i[0] for i in scores[1:top_n+1]]

    return df.iloc[movie_indices]