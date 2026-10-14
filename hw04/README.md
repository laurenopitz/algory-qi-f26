## S&P 500 Trading Strategy Backtester: Algory QI HW04

## Overview
For this project, I built a Python backtester to test different trading strategies using historical S&P 500 data starting in 1990. The program uses the last 60 trading days to decide whether to hold cash or invest in the S&P 500. 

## Files
- 'hw04_starter.py' — strategies, backtester, performance calculations, plots, and current trading signal.
- `check_hw04.py' and `_check.py' — provided self-checks for backtest correctness.

## How the backtester works
I downloaded daily '^SP500TR' closing prices starting January 1, 1990. The backtester starts with $1 and calculates how much the portfolio would grow over time based on each strategy's decisions. Each strategy uses the previous 60 trading days of closing prices to decide whether to invest in the index or hold cash. If the strategy returns 'True', the portfolio earns the index's next day return, otherwise, it holds cash with a 0% return. Strategies can only access prices that were available when the trading decision was made, so future information is not used. 

## Strategies 
I tested six strategies including momentum, moving averages, mean reversion, volatility, linear regression, and buying the dip. 
My final strategy was linear regression. If the trend over the previous 60 days is positive, it invests in the S&P 500, otherwise it holds cash. 

## Results 
| Strategy | Training annualised return |
| --- | ---: |
| 30-day momentum | 3.28% |
| 30-day moving average | 3.84% |
| Mean reversion | 4.11% |
| Low volatility | 2.16% |
| Linear regression trend-following | 6.50% |
| Buy the dip | 2.09% |

| Metric | Linear regression | Buy-and-hold |
| --- | ---: | ---: |
| Total return | 280.47% | 780.22% |
| Annualised return | 9.28% | 15.54% |
| Maximum drawdown | -27.70% | -33.79% |
| Fraction invested | 77.87% | 100.00% |

This data shows that on the test set, my strategy earned 9.28% annually, while the S&P 500 earned 15.54%. My strategy had a smaller maximum drawdown of -27.70% for the index than the S&P 500's being -33.79%.

## What I Learned 
I learned that a strategy can have positive returns yet still not outperform the market. This project also showed me why testing strategies on unseen data is important to understand whether they actually work beyond the training period. 

## How to Run 
```bash
python -m pip install numpy pandas yfinance matplotlib
```

Place `hw04_starter.py`, `check_hw04.py`, and `_check.py` in the same folder. Then run:

```bash
python hw04_starter.py
python check_hw04.py
