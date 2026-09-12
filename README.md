# Electricity Market Risk & Trading Analytics

A historical-simulation risk engine for wholesale electricity trading positions, built on real German/Luxembourg day-ahead power prices (EPEX SPOT).

**Status:** Core analysis complete — data cleaning, exploratory analysis, volatility, P&L, and VaR/Expected Shortfall are implemented. Stress testing and final polish are in progress and will be completed this weekend.

---

## 1. Overview

Electricity is unlike most traded commodities: prices can go negative, spike by hundreds of euros per MWh within a single hour, and cluster into periods of extreme volatility driven by weather, demand, and renewable generation. For a power trader, this creates real financial exposure that is very different from the risk profile of equities or bonds.

This project applies standard quantitative risk-management techniques — historical-simulation Value-at-Risk (VaR), Expected Shortfall (ES), and stress testing — to a simulated wholesale electricity trading position, using real hourly day-ahead prices. It is an analytics and risk-measurement exercise, not a price-forecasting model and not a live trading system.

## 2. Research Question

> How much financial risk does a power trader face from electricity-price volatility and extreme price movements?

## 3. Market Context

- **Wholesale electricity markets**: prices are set day-ahead (e.g. EPEX SPOT) for each hour of the next day, based on supply and demand across the grid.
- **MWh exposure**: a trading position is expressed in megawatt-hours (MWh) — the notional volume of electricity bought or sold at the market price.
- **Price volatility**: driven by demand swings, weather, fuel costs, and renewable output; electricity price volatility is materially higher than in most financial markets.
- **Negative prices**: during periods of high renewable generation and low demand, prices can fall below zero — producers effectively pay to offload power.
- **Price spikes**: scarcity events (low wind/solar, high demand, outages) can send prices to extreme highs within a single hour.

## 4. Data

- **Source**: [SMARD – Bundesnetzagentur day-ahead price data](https://www.smard.de) *(confirm/replace with your actual source)*
- **Market**: Germany/Luxembourg day-ahead auction
- **Frequency**: hourly
- **Units**: €/MWh
- **Period covered**: *[fill in start–end date of your dataset]*

Raw data is provided as `Day_ahead_prices.csv`. Cleaning steps include timestamp parsing, sorting, duplicate detection, missing-value checks, and outlier inspection — with negative prices and extreme spikes explicitly preserved and analyzed rather than treated as errors.

## 5. Methodology

- **Price changes over returns**: because prices can be negative or near zero, percentage returns are misleading or undefined for electricity. The analysis uses absolute price changes (ΔP = Pₜ − Pₜ₋₁) as the primary risk driver.
- **Simulated position**: a hypothetical 100 MWh position is used to translate price changes into € P&L (P&L = Q × ΔP). Position size is varied (25–500 MWh) in a sensitivity analysis.
- **Historical VaR**: 95% and 99% Value-at-Risk are estimated directly from the empirical distribution of historical P&L, with no distributional assumptions.
- **Expected Shortfall**: the average loss in the tail beyond the VaR threshold, capturing the severity of extreme events that VaR alone does not.
- **Stress testing**: volatility shocks (−2σ, −3σ, −4σ) and the worst observed historical price move are applied to the position to assess losses under extreme but plausible scenarios. *(in progress)*

## 6. Results

*To be finalized once the stress-testing section is complete. Will include:*

- Summary statistics of the price series (mean, std dev, min/max, 5th/95th percentile, share of negative prices)
- Rolling volatility chart and discussion of volatility clustering
- P&L distribution for the 100 MWh position, with VaR thresholds marked
- 95%/99% VaR and Expected Shortfall figures, with practical interpretation
- Stress-test table (volatility shocks + worst historical move)
- Position-size sensitivity analysis (VaR/ES at 25–500 MWh)

## 7. Limitations

- Historical simulation assumes that past price behavior is informative about future risk; electricity markets can undergo regime changes (policy, fuel mix, extreme weather) that break this assumption.
- Historical VaR and ES are not guarantees of future maximum loss — they describe risk under the historical simulation window only.
- Based on a single market (Germany/Luxembourg) and time period; results may not generalize to other markets or periods.
- The simulated position ignores transaction costs, liquidity constraints, collateral/margin requirements, imbalance costs, and hedging — it is a simplified analytical exposure, not an executable trading strategy.
- This is a research/portfolio project, not a production risk system.

## 8. Future Work

- Intraday price data
- Cross-market spread risk
- Weather, load, and renewable-generation variables
- Gas and CO₂ price correlations
- Monte Carlo simulation of price paths
- Extreme Value Theory (EVT) / peaks-over-threshold tail modeling
- Portfolio-level risk across multiple positions
- Simple hedging strategies
- Battery/storage trading economics

## 9. Project Structure

```text
energy_price_risk/
│
├── README.md
├── Day_ahead_prices.csv
├── energy_risk.ipynb
└── src/
```

## 10. Tech Stack

Python, pandas, NumPy, matplotlib.

---

*This project is for educational and portfolio purposes. It does not constitute financial or trading advice, and does not represent a live or production trading/risk system.*
