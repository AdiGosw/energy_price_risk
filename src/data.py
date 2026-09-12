import pandas as pd
import matplotlib.pyplot as plt


def load_prices(path: str, country:str = "Germany/Luxembourg") -> pd.DataFrame:

    df = pd.read_csv(
    path,
    sep=";",
    encoding="utf-8-sig",
    thousands=","
    )
    col_name = f"{country} [€/MWh] Calculated resolutions"
    df = df[["Start date", col_name]].copy()
    df.columns = ["timestamp", "price_eur_mwh"]
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%b %d, %Y %I:%M %p")
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df

def summary(df: pd.DataFrame) -> pd.Series:
    p = df["price_eur_mwh"]
    return pd.Series({
        "mean": p.mean(),
        "median": p.median(),
        "std": p.std(),
        "min": p.min(),
        "max": p.max(),
    })
