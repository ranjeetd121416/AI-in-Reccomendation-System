def diversify(df, recs):
    extra = df.sample(3)
    return recs._append(extra).drop_duplicates()