def clean_data(df):

    df.dropna(inplace=True)

    df["category"] = df["category"].apply(
        lambda x: x.split("|")[0]
    )

    return df