def diversify(movie_list, top_k=None):

    if not movie_list:
        return []

    seen_genres = set()
    diversified = []
    remaining = []

    for movie in movie_list:

        genres = movie["genres"]
        primary_genre = genres.split("|")[0] if genres else "Unknown"

        if primary_genre not in seen_genres:
            diversified.append(movie)
            seen_genres.add(primary_genre)
        else:
            remaining.append(movie)

    # Fill remaining slots to maintain length
    final_list = diversified + remaining

    if top_k:
        return final_list[:top_k]

    return final_list