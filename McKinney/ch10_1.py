import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import scipy as sc
import seaborn as sns
df = pd.DataFrame({"key1" : ["a", "a", None, "b", "b", "a", None],
"key2" : pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
"data1" : np.random.standard_normal(7),
"data2" : np.random.standard_normal(7)})
print(df)
grouped = df["data1"].groupby(df["key1"])
# print(grouped)
print(grouped.mean())
means = df["data1"].groupby([df["key1"], df["key2"]]).mean()
print(means)
print(means.unstack())
states = np.array(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
years = [2005, 2005, 2006, 2005, 2006, 2005, 2006]
print(df["data1"].groupby([states, years]).mean())
# print(df)
print(df.groupby(["key1", "key2"]).size())
print(df.groupby("key1", dropna=False).size())
print(df.groupby(["key1", "key2"],dropna=False ).size())
# p 339  случайная выборка и перестановка
# сконструируем колоду игральных карт
# Hearts (черви), Spades (пики), Clubs (трефы), Diamonds (бубны)
suits = ["H", "S", "C", "D"]
card_val = (list(range(1, 11)) + [10] * 3) * 4
# print(card_val)
base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
print(base_names)
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)
deck = pd.Series(card_val, index=cards)
# print(deck)
def draw(deck, n=5):
    return deck.sample(n)
print(draw(deck))
# p 341
df = pd.DataFrame({"category": ["a", "a", "a", "a",
"b", "b", "b", "b"],
"data": np.random.standard_normal(8),
"weights": np.random.uniform(size=8)})
print(df)
grouped = df.groupby("category")
def get_wavg(group):
    return np.average(group["data"], weights=group["weights"])
print(grouped.apply(get_wavg))
# print(category)    
close_px = pd.read_csv("McKinney/examples/stock_px.csv", parse_dates=True,
index_col=0)
close_px.info()
print(close_px.tail(4))
# p 342
def spx_corr(group):
    return group.corrwith(group["SPX"])
rets = close_px.pct_change().dropna()
def get_year(x):
    return x.year    
by_year = rets.groupby(get_year)
print(by_year.apply(spx_corr))    
def corr_aapl_msft(group):
    return group["AAPL"].corr(group["MSFT"])
print(by_year.apply(corr_aapl_msft))
import statsmodels.api as sm
def regress(data, yvar=None, xvars=None):
    Y = data[yvar]
    X = data[xvars]
    X["intercept"] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params
print(by_year.apply(regress, yvar="AAPL", xvars=["SPX"]))

# p 344
df = pd.DataFrame({'key': ['a', 'b', 'c'] * 4,
'value': np.arange(12.)})
print(df)
g = df.groupby('key')['value']
print(g.mean())
def get_mean(group):
    return group.mean()
print(g.transform(get_mean))    
print(g.transform('mean'))
def times_two(group):
    return group * 2
print(g.transform(times_two))    
def normalize(x):
    return (x - x.mean()) / x.std()
print(g.transform(normalize))    
print(g.apply(normalize))






