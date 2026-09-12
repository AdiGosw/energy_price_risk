# Electricity Market Risk & Trading Analytics

## Overview

This project is a historical-simulation risk engine for wholesale electricity-market positions, built on five years of hourly German day-ahead prices (Germany/Luxembourg bidding zone, EPEX SPOT / SMARD.de, Sep 2021–Aug 2026). It quantifies the financial risk a power trader faces from electricity-price volatility and extreme price movements, using techniques standard in quantitative risk management: Value-at-Risk (VaR), Expected Shortfall (ES), and scenario-based stress testing.

Unlike equity or FX markets, wholesale electricity prices are driven by physical constraints — supply and demand must balance in real time, storage is limited, and renewable generation is weather-dependent. This produces price behavior rarely seen in other asset classes: frequent negative prices, extreme positive spikes, and heavy-tailed, non-normal return distributions. This project is built around those characteristics rather than treating electricity prices as a generic financial time series.

This is an analytics and risk-measurement project, not a forecasting or live-trading system. All positions are hypothetical, and no trading recommendations are implied.

## Research Question

> How much financial risk does a power trader face from electricity-price volatility and extreme price movements?

## Market Context

- **Wholesale electricity markets**: Prices are set through day-ahead auctions where generation must be matched to demand every hour, with no large-scale storage to smooth out imbalances.
- **MWh exposure**: A trading position is expressed in megawatt-hours (MWh) — the quantity of power bought or sold at the market-clearing price for a given hour.
- **Price volatility**: Driven by demand swings, weather, fuel costs, and renewable output; electricity price volatility is materially higher than most traditional financial assets.
- **Negative prices**: When renewable generation exceeds demand and plants cannot economically shut down, prices can go negative — generators effectively pay to keep producing. Negative-price hours: 1836 out of 43824 (4.19%) in this dataset.
- **Price spikes**: Sudden generation shortfalls or demand surges can send prices sharply higher within a single hour, creating large tail risk for short positions in particular.

## Methodology

- **Price changes, not returns**: Percentage returns are unreliable near zero or negative prices, so this project uses absolute price changes, ΔP_t = P_t − P_{t-1}, as the basis for volatility and P&L calculations.
- **Simulated position**: A hypothetical long position of 100 MWh is used as the default exposure (Q = 100 MWh), with P&L calculated as PnL_t = Q · ΔP_t.
- **Historical-simulation VaR**: VaR at the 95% and 99% confidence levels is calculated as the corresponding quantile of the historical loss distribution — no parametric distribution is assumed.
- **Expected Shortfall**: ES is calculated as the average loss in the tail beyond the VaR threshold, capturing the severity of extreme outcomes that VaR alone does not.
- **Stress testing**: Volatility-based shocks (−2σ, −3σ, −4σ of historical price changes) and the single worst historical price move are applied to the position to illustrate tail-scenario losses.
- **Position-sizing sensitivity**: VaR and ES are recalculated across a range of position sizes (25–500 MWh) to show how risk scales with exposure.
- **Optional trading extension**: A simple percentile-threshold long/short rule is included to demonstrate that the same risk functions generalize to any position — this is illustrative only, not a validated trading strategy.

## Results

| Metric | Value |
|---|---|
| Mean price | €124.53/MWh |
| Median price | €102.75/MWh |
| Std. deviation | €100.62/MWh |
| Minimum price | −€500.00/MWh |
| Maximum price | €936.28/MWh |
| Share of negative-price hours | 4.19% |
| σ (std. dev. of hourly price changes) | €23.75/MWh |
| VaR 95% (100 MWh, long) | €3,234.80 |
| VaR 99% (100 MWh, long) | €6,216.56 |
| Expected Shortfall 95% | €5,281.04 |
| Worst historical price move | −€355.08/MWh (Nov 6, 2024, 19:00) |
| Worst historical stress loss (100 MWh) | €35,508.00 |

![Historical electricity price](figures/electricity_price.pdf)
*Figure 1: German day-ahead price, Sep 2021–Aug 2026, showing negative-price periods and spike events.*

![Rolling volatility](figures/volatility.pdf)
*Figure 2: 24-hour rolling volatility of price changes.*


![P&L distribution](figures/pnl_distribution.pdf)
*Figure 3: Historical P&L distribution for a 100 MWh long position, with 95%/99% VaR marked.*

![Stress-test losses](figures/risk_stress_test.pdf)
*Figure 4: Losses under normal, VaR, sigma-shock, and worst-historical scenarios.*

**Key findings:**

- Electricity prices exhibited substantial volatility over the sample period, with a standard deviation of hourly price changes (σ) of €23.75/MWh, and visible volatility clustering around periods of market stress (see `figures/volatility.pdf`).
- A 100 MWh long position faced a 95% one-hour VaR of €3,234.80 — meaning historical losses exceeded this amount in roughly 5% of hours — and a 99% VaR of €6,216.56.
- Expected Shortfall at the 95% level (€5,281.04) was noticeably larger than VaR at the same confidence level, confirming that the loss distribution has a heavy tail: when losses do exceed the VaR threshold, they tend to be considerably worse on average than the threshold itself.
- Risk scaled linearly with position size, as expected given PnL = Q · ΔP: a 500 MWh position carries exactly 5× the VaR/ES of a 100 MWh position, illustrating how MWh-based exposure limits translate directly into €-based loss limits.
- The single worst historical price move in the sample was a €355.08/MWh drop on November 6, 2024 at 19:00 — an evening hour, when demand is typically peaking. Applied to a 100 MWh long position, this single hour would have produced a €35,508 loss, over 10× the 95% VaR estimate and comfortably beyond even the −4σ stress scenario, illustrating why tail risk in electricity markets cannot be fully captured by volatility-based shocks alone.

See `figures/` for the four core visualizations: historical price, rolling volatility, P&L distribution with VaR thresholds marked, and stress-test losses by scenario.

## Limitations

- Historical simulation assumes that the historical sample is representative of future risk; it does not adapt to regime changes (e.g., new interconnectors, changing renewable capacity, policy shifts).
- Electricity markets can undergo structural regime changes (e.g., the 2021–2022 European energy crisis) that historical VaR calculated over a mixed sample may over- or under-state depending on the window used.
- Historical VaR is a statistical estimate based on past observations, not a guaranteed maximum loss — actual future losses can exceed any VaR estimate.
- This analysis is based on a single market (Germany/Luxembourg) and a single historical period; results may not generalize to other bidding zones or time periods.
- The simulated position ignores transaction costs, liquidity constraints, collateral/margin requirements, imbalance costs, and any hedging activity a real trading desk would use to manage this exposure.
- The optional trading-strategy extension uses full-sample percentile thresholds, which a real trader would not have known in advance (a lookahead simplification) — it is illustrative only and not a validated or executable trading strategy.
- This is a research/analytics project, not a production risk-management system.

## Future Work

- Incorporate intraday (15-minute) prices for higher-resolution risk measurement.
- Extend to cross-market spreads (e.g., Germany vs. France, Germany vs. Netherlands) to analyze interconnector risk.
- Add weather, load, and renewable-generation variables to explain price volatility drivers.
- Include gas and CO₂ prices to analyze fuel-cost pass-through effects.
- Monte Carlo simulation as an alternative to historical simulation for VaR/ES.
- Extreme Value Theory (EVT) / peaks-over-threshold modeling for more rigorous tail-risk estimation.
- Portfolio-level risk across multiple positions or markets.
- Explicit hedging strategies (e.g., forward contracts) layered on top of the spot position.
- Battery storage trading strategies, which can exploit price spreads rather than directional price views.
- Forecast-based (rather than purely historical) risk scenarios.

---

*This project was built as a compact, research-quality case study demonstrating historical-simulation risk analysis applied to wholesale electricity markets. It uses real historical market data; no prices, results, or performance figures in this repository are fabricated.*
