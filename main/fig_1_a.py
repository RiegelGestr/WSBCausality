import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
with open("data/GME_all_signals.csv","r") as inpuf:
    df = pd.read_csv(inpuf)
gdf = df.groupby(by = ["date"]).agg({
    "tweets":"sum",
    "occurrences":"sum",
    "volume":"sum",
    "close":"mean"
}).reset_index()
gdf["date"] = pd.to_datetime(gdf["date"],format = "%Y-%m-%d")
################################################################
corr_twt_market = gdf["volume"].corr(gdf["tweets"])
corr_reddit_market = gdf["volume"].corr(gdf["occurrences"])
corr_reddit_twt = gdf["tweets"].corr(gdf["occurrences"])
corr_reddit_price = gdf["occurrences"].corr(gdf["close"])
corr_twitter_price = gdf["tweets"].corr(gdf["close"])
corr_market_price = gdf["volume"].corr(gdf["close"])
print("Twitter-Reddit")
print(corr_reddit_twt)
print("Market-Reddit")
print(corr_reddit_market)
print("Market-Twitter")
print(corr_twt_market)
print("Market-Price")
print(corr_market_price)
print("Price-Reddit")
print(corr_reddit_price)
print("Price-Twitter")
print(corr_twitter_price)
m_v = gdf["volume"].mean()
m_t = gdf["tweets"].mean()
m_r = gdf["occurrences"].mean()
#m_p = gdf["close"].mean()
gdf["volume"] = (gdf["volume"]/m_v)
gdf["tweets"] = (gdf["tweets"]/m_t)
gdf["occurrences"] = (gdf["occurrences"]/m_r)
gdf["close"] = (gdf["close"]/8)
################################################################
y = 90
x = 210
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
tax = ax.twinx()
################################################################################
m_lax = ax.plot(gdf["date"],gdf["volume"],color = "#073D74",lw = 30,label = "Trading Volume")
r_lax = ax.plot(gdf["date"],gdf["occurrences"],color = "#EF6939",lw = 30,label = "Reddit")
t_lax = ax.plot(gdf["date"],gdf["tweets"],color = "#70ADE9",lw = 30,label = "Twitter")
ax.set_ylabel("Volume",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
#ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_yscale("log")
ax.set_ylim([0.001,100])
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dotted")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
################################################################################
p_lax = tax.plot(gdf["date"],gdf["close"],color = "#46B998",lw = 30,label = "Price")
tax.set_ylabel("Price",fontsize = fontsize*0.7,rotation = 270,labelpad = 100)
tax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
tax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
tax.set_yscale("log")
tax.set_ylim([1,100])
################################################################################
lns = m_lax + r_lax + t_lax + p_lax
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc = "upper center",bbox_to_anchor=[0.55, +1.1],ncol = 4,fontsize = fontsize/2,frameon = False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.1,right = 0.9)
fig.savefig("fig/fig_1_A.pdf")
