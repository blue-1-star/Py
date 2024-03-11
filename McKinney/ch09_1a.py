import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import scipy as sc
import seaborn as sns
data = np.arange(10)
print(data)
# plt.plot(data)
# plt.show()
# pic 9.8


# p 305
tips = pd.read_csv("McKinney/examples/tips.csv")
print(tips.head())
party_counts = pd.crosstab(tips["day"], tips["size"])
party_counts = party_counts.reindex(index=["Thur", "Fri", "Sat", "Sun"])
party_counts = party_counts.loc[:,2:5]
# Нормировка на сумму 1
# print(party_counts)
party_pcts = party_counts.div(party_counts.sum(axis="columns"),
axis="index")
# print(party_pcts)
# party_pcts.plot.bar(stacked=True)
import seaborn as sns
tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])
print(tips.head())
# sns.barplot(x="tip_pct", y="day", data=tips, orient="h")
# sns.barplot(x="tip_pct", y="day", hue="time", data=tips, orient="h")
# tips["tip_pct"].plot.hist(bins=50)
# tips["tip_pct"].plot.density()
comp1 = np.random.standard_normal(200)
comp2 = 10 + 2 * np.random.standard_normal(200)
values = pd.Series(np.concatenate([comp1, comp2]))
# sns.histplot(values, bins=100, color="black")
macro = pd.read_csv("McKinney/examples/macrodata.csv")
data = macro[["cpi", "m1", "tbilrate", "unemp"]]
trans_data = np.log(data).diff().dropna()
# print(trans_data)
# ax = sns.regplot(x="m1", y="unemp", data=trans_data)
# sns.pairplot(trans_data, diag_kind="kde", plot_kws={"alpha": 0.2})
# ax.title("Changes in log(m1) versus log(unemp)")
# sns.catplot(x="day", y="tip_pct", hue="time", col="smoker",
# kind="bar", data=tips[tips.tip_pct < 1])
# sns.catplot(x="day", y="tip_pct", row="time", col="smoker",
# kind="bar", data=tips[tips.tip_pct < 1])
sns.catplot(x="tip_pct", y="day", kind="box",
data=tips[tips.tip_pct < 0.5])
plt.show()

