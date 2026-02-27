def generate_explanation(movie, mood, time_context=None):

    genres = movie.get("genres", "varied genres")
    primary_genre = genres.split("|")[0] if genres else "content"

    explanation = f"This {primary_genre} movie is recommended because "

    # Mood reasoning
    if mood and mood != "neutral":
        explanation += f"you appear to be feeling {mood}, and {primary_genre.lower()} content often aligns with this mood. "

    # Time context reasoning
    if time_context == "academic":
        explanation += "Since it is academic hours, educational or informative content is prioritized. "
    elif time_context == "leisure":
        explanation += "Since it is leisure time, entertainment-based content is prioritized. "

    explanation += "It also aligns with your viewing patterns through our hybrid recommendation model."

    return explanation