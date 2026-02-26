def generate_explanation(mood, context, category):

    reasons = [
        f"You like {category} movies",
        f"Current mode: {context}",
        f"Detected mood: {mood}"
    ]

    return "Recommended because:\n✔ " + "\n✔ ".join(reasons)