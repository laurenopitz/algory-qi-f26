"""Homework 4 starter — Algory QI Education, Fall 2026

"""
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

LOOKBACK = 60


# ---------------------------------------------------------------- Q1
def load_and_split(split_date="2011-09-09", prices=None, warmup=LOOKBACK):
    if prices is None:
        data = yf.download("^SP500TR", start="1990-01-01",
                           progress=False)
        prices = data["Close"]

        if isinstance(prices, pd.DataFrame):
            prices = prices.iloc[:, 0]

    prices = prices.dropna()

    train = prices.loc[:split_date]

    split_index = len(train) - 1
    test = prices.iloc[split_index - warmup + 1:]

    print("Training days:", len(train))
    print("Training mean price:", train.mean())
    print("Test days:", len(test))  
    print("Test mean price:", test.mean())

    return train, test


# ---------------------------------------------------------------- Q2, Q4, Q5
def always_hold(window):
   
    return True


def always_cash(window):
    
    return False


def make_random_hold(p=0.7, seed=0):
   
    rng = np.random.default_rng(seed)

    def random_hold(window):
        return bool(rng.random() < p)

    return random_hold


def five_day_reversal(window):
   
    return bool(window[-1]<=window[-6])

def momentum_30(window):
    return bool(window[-1]>window[-31])

def moving_average_30(window):
    average=np.mean(window[-30:])
    return bool(window[-1]>average)

def mean_reversion(window):
    average=np.mean(window[-30:])
    return bool(window[-1]<average)

def low_volatility(window):
    returns=np.diff(window)/window[:-1]
    recent_vol=np.std(returns[-15:])
    longer_vol=np.std(returns)
    return bool(recent_vol<longer_vol)

def linear_trend(window):
    x=np.arange(len(window))
    slope=np.polyfit(x, window, 1)[0]
    return bool(slope>0)

def buy_the_dip(window):
    change=window[-1]/window[-16]-1
    return bool(change<-0.05)


def my_strategy(window):
   
    x= np.arange(len(window))
    slope=np.polyfit(x, window, 1)[0]
    return bool(slope>0)

# ---------------------------------------------------------------- Q3
def backtest(prices, strategy, lookback=LOOKBACK):
   

    prices=np.asarray(prices,dtype=float)
    portfolio=1.0
    index_value=1.0
    
    portfolio_values=[1.0]
    index_values=[1.0]
    
    days_invested=0
    
    for i in range(lookback-1, len(prices)-1):
        window=prices[i-lookback+1: i+1]
        hold=strategy(window)
        daily_return=prices[i+1]/ prices[i]-1
        
        index_value*=(1+ daily_return)
        
        if hold: 
            portfolio*= (1+ daily_return)
            days_invested+=1
            
            
        portfolio_values.append(portfolio)
        index_values.append(index_value)
    days=len(portfolio_values)-1
    total_return=portfolio-1
    annualised_return=portfolio**(252/days)-1
    
    peaks=np.maximum.accumulate(portfolio_values)
    drawdowns=np.array(portfolio_values)/peaks-1
    max_drawdown=np.min(drawdowns)
    
    fraction_invested=days_invested/days 
    
    return{
        "total_return": total_return,
        "annualised_return": annualised_return,
        "max_drawdown": max_drawdown,
        "fraction_invested": fraction_invested,
        "portfolio_values": portfolio_values,
        "index_values": index_values 
        }

def plot_backtest(prices, strategy, name):
    result=backtest(prices, strategy)
    
    plt.figure(figsize=(10,5))
    
    plt.plot(result["portfolio_values"], label=name)
    plt.plot(result["index_values"], label= "S&P 500")
    plt.title(name+ "vs. S&P 500")
    plt.xlabel("Trading days")
    plt.ylabel("Portfolio value (starting at $1)")
    plt.legend()
    plt.grid(True)
    
    plt.show()
    
    


def main():
    train, test = load_and_split()
    for name, strat in [("always hold", always_hold),
                        ("always cash", always_cash),
                        ("random 70%", make_random_hold(0.7, seed=0)),
                        ("5-day reversal", five_day_reversal)]:
        r = backtest(train, strat)
        print(f"{name:<16} total {r['total_return']:+.1%}   annual {r['annualised_return']:+.2%}")
    plot_backtest(train, always_hold, "Always Hold")
    plot_backtest(train, always_cash, "Always Cash")
    plot_backtest(train, make_random_hold(0.7, seed=0), "Random 70%")
    plot_backtest(train, five_day_reversal, "Five-Day Reversal")
    
    strategies= [
        ("30-day momentum", momentum_30),
        ("30-day moving average", moving_average_30),
        ("Mean Reversion", mean_reversion),
        ("Low volatility", low_volatility),
        ("Linear regression", linear_trend),
        ("Buy the dip", buy_the_dip)
        ]
    print("\nQUESTION 6: STRATEGY RESULTS")
    for name, strategy in strategies:
        result=backtest(train, strategy)
        print(name, "Annual Return:", f"{result['annualised_return']: .2%}")
    
    
    print("\nQUESTION 8: TEST SET RESULTS")
    
    strategy_result= backtest(test, my_strategy)
    index_result=backtest(test, always_hold)
    
    print("FINAL STRATEGY:")
    print("Total Return:", f"{strategy_result['total_return']: .2%}") 
    print("Annualised Return:", f"{strategy_result['annualised_return']:.2%}")
    print("Maximum Drawdown:",
          f"{strategy_result['max_drawdown']:.2%}")
    print("Fraction Invested:",
          f"{strategy_result['fraction_invested']:.2%}")
    
    
    print("\nS&P 500 BUY AND HOLD:")
    print("Total Return:",
          f"{index_result['total_return']:.2%}")
    print("Annualised Return:",
          f"{index_result['annualised_return']:.2%}")
    print("Maximum Drawdown:",
          f"{index_result['max_drawdown']:.2%}")
    print("Fraction Invested:",
          f"{index_result['fraction_invested']:.2%}")

    plt.figure(figsize=(10, 5))
    plt.plot(strategy_result["portfolio_values"],
             label="Linear Regression Strategy")
    plt.plot(strategy_result["index_values"],
             label="S&P 500")
    plt.title("Test Set: Strategy vs. S&P 500")
    plt.xlabel("Trading days")
    plt.ylabel("Portfolio value (starting at $1)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\nQUESTION 9: CURRENT SIGNAL")

    latest_data = yf.download("^SP500TR",
                              start="2026-01-01",
                              progress=False)

    latest_prices = latest_data["Close"]

    if latest_prices.ndim > 1:
        latest_prices = latest_prices.iloc[:, 0]

    latest_prices = latest_prices.dropna()

    latest_window = latest_prices.iloc[-60:].to_numpy()

    decision = my_strategy(latest_window)

    print("Decision:", "HOLD INDEX" if decision else "HOLD CASH")
    print("Last closing date:", latest_prices.index[-1].date())


if __name__ == "__main__":
    main()
