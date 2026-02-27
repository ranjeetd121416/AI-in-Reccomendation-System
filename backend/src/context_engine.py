from datetime import datetime


def apply_context(movies_df, movie_ids, mood, time_context=None):

    # Detect time context if not provided
    if time_context is None:
        hour = datetime.now().hour
        time_context = "academic" if 9 <= hour <= 16 else "leisure"

    # Create fast lookup dictionary
    movie_lookup = {
        row["movieId"]: row
        for _, row in movies_df.iterrows()
    }

    prioritized = []
    others = []

    for movie_id in movie_ids:

        if movie_id not in movie_lookup:
            continue

        movie = movie_lookup[movie_id]
        genres = movie["genres"]

        # Academic context
        if time_context == "academic":
            if "Documentary" in genres or "Education" in genres:
                prioritized.append(movie)
            else:
                others.append(movie)

        # Leisure context
        else:
            if mood == "happy" and "Comedy" in genres:
                prioritized.append(movie)
            elif mood == "sad" and "Drama" in genres:
                prioritized.append(movie)
            elif mood == "angry" and "Action" in genres:
                prioritized.append(movie)
            else:
                others.append(movie)

    # Return prioritized first, then others
    return prioritized + others