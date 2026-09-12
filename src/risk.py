import numpy as np
import pandas as pd

def price_change(df: pd.DataFrame, price_col: str = "price_eur_mwh"):
    df = df.copy()
    df["delta_p"] = df[price_col].diff()
    return df

def rolling_volatility(df: pd.DataFrame, window:int = 24,
                       delta_col: str = "delta_p"): 
    return df[delta_col].rolling(window).std()

def pnl(delta_p: pd.Series, quantity: float, direction:str = "long"):
    # PnL_t = Quantity * delta_p_t   (long)
    # PnL_t = -Quantity * delta_p_t  (short)

    sign = 1 if direction == "long" else -1
    return sign * delta_p * quantity

def var(pnl: pd.Series, confidence: float = 0.95):
    # Historical-simulation VaR, returned as a POSITIVE loss number.
    # e.g. confidence=0.95 -> the loss that is exceeded ~5% of the time.

    pnl = pnl.dropna()
    loss = -pnl
    var = loss.quantile(confidence)
    return var

def expected_shortfall(pnl:pd.Series, confidence: float = 0.95):
    # Average loss in the tail beyond VaR. Also returned as a POSITIVE number
    pnl = pnl.dropna()
    loss = -pnl
    var = loss.quantile(confidence)
    tail = loss[loss > var]
    return tail.mean()

def run_stress_test(delta_p:pd.Series , quantity:float, direction:str = "long"):
    # Apply volatility shocks (-2sigma, -3sigma, -4sigma) and the worst historical
    # move, and report resulting PnL for the given position.

    sign = 1 if direction == "long" else -1
    sigma = delta_p.std()
    worst_move = delta_p.min()

    scenarios = {
        "-2sigma shock": -2 * sigma,
        "-3sigma shock": -3 * sigma,
        "-4sigma shock": -4 * sigma,
        "worst historical move": worst_move
    }

    rows = []
    for name, shock in scenarios.items():
        pnl = sign * quantity * shock
        rows.append({"scenario": name, "price_shock_eur": shock, "position_mwh": quantity, "pnl_eur": pnl})

    return pd.DataFrame(rows)

