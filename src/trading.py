import pandas as pd
import numpy as np

def position(quantity: float, direction:str = "long") -> dict:
    return {"quantity": quantity, "direction": direction}

def signals(df: pd.DataFrame, price_col: str = "price_eur_mwh", low_pct: float = 0.25, high_pct: float = 0.75) -> pd.Series:
    # Long when price is below the low_pct historical percentile,
    # short when price is above the high_pct historical percentile,
    # flat otherwise.
    # Returns a Series of {-1, 0, 1}.

    low_thresh = df[price_col].quantile(low_pct)
    high_thresh = df[price_col].quantile(high_pct)

    signal = pd.Series(0, index= df.index)
    signal[df[price_col] < low_thresh] = 1
    signal[df[price_col] > high_thresh] = -1
    return signal

def strategy_pnl(delta_p: pd.Series, signal: pd.Series, quantity: float) -> pd.Series:
    # PnL_t = signal_t * Q * delta_p_t
    # Signal is applied to delta_p at the SAME index — decide on your convention
    # for whether signal_t uses info available before delta_p_t (avoid lookahead).
    return signal * delta_p * quantity

def evaluate_strategy(pnl: pd.Series) -> dict:
    pnl = pnl.dropna()
    cumulative = pnl.cumsum()
    running_max = cumulative.cummax()
    drawdown = cumulative - running_max

    trades = pnl[pnl != 0]
    wins = trades[trades > 0]

    return {
        "total_pnl": pnl.sum(),
        "average_pnl": pnl.mean(),
        "voltality": pnl.std(),
        "max drawdown": drawdown.min(),
        "num_trades": (trades != 0).sum(),
        "win_rate": len(wins) / len(trades) if len(trades) > 0 else np.nan
    }

