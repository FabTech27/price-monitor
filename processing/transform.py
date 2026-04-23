import pandas as pd

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def clean_data(data):
    df = pd.DataFrame(data)

    # Limpiar precio
    df["price"] = (
        df["price_raw"]
        .str.replace("£", "", regex=False)
        .astype(float)
    )

    # Limpiar rating
    df["rating"] = df["rating"].str.split().str[-1]
    df["rating"] = df["rating"].map(RATING_MAP)

    # Drop columna original
    df = df.drop(columns=["price_raw"])

    return df