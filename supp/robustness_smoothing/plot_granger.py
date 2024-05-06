import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import seaborn as sns
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
est = pytz.timezone('US/Eastern')
################################################################################
################################################################################
################################################################################
################################################################################
with open("data/granger_index_GME_with_twitter.csv") as inpuf:
    df = pd.read_csv(inpuf,sep = ";")
df["date"] = pd.to_datetime(df["date"],format = "%Y-%m-%d")
xdf = df[df["lag"] == 1]
thr = 0.1
start_date = datetime(2021,1,5)
final_date = datetime(2021,2,5)
xdf = xdf[(xdf["date"]>start_date) & (xdf["date"]<final_date)]
color_market_to_reddit = "#004E89"
color_reddit_to_market = "#CC132F"
color_market_to_twt = "#BBB09B"
color_reddit_to_twt = "#F7B538"
y = 140
x = 260
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
#
kind = "Market --> Reddit"
df = xdf[(xdf["kind"] == kind)]
ax.plot(df["date"],df["gc_index"],color = color_market_to_reddit,lw = 30,label = "M.Shares --> Reddit")
df = df[df["gc_p"] < thr]
ax.scatter(df["date"],df["gc_index"],color = color_market_to_reddit,s = 15_000,alpha = .5, marker = "^")
#
kind = "Reddit --> Market"
df = xdf[(xdf["kind"] == kind)]
ax.plot(df["date"],df["gc_index"],color = color_reddit_to_market,lw = 30,label = "Reddit --> M.Shares")
df = df[df["gc_p"] < thr]
ax.scatter(df["date"],df["gc_index"],color = color_reddit_to_market,s = 15_000,alpha = .5, marker = "^")
#
kind = "Market --> Twitter"
df = xdf[(xdf["kind"] == kind)]
ax.plot(df["date"],df["gc_index"],color = color_market_to_twt,lw = 30,label = "M.Shares --> Twitter")
df = df[df["gc_p"] < thr]
ax.scatter(df["date"],df["gc_index"],color = color_market_to_twt,s = 15_000,alpha = .5, marker = "^")
#
kind = "Reddit --> Twitter"
df = xdf[(xdf["kind"] == kind)]
ax.plot(df["date"],df["gc_index"],color = color_reddit_to_twt,lw = 32,label = kind)
df = df[df["gc_p"] < thr]
ax.scatter(df["date"],df["gc_index"],color = color_reddit_to_twt,s = 15_000,alpha = .5, marker = "^")
#
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
################################################################################################
ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.set_ylabel("Granger Index",fontsize = fontsize*0.7,labelpad = 32)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
ax.legend(fontsize = fontsize*0.5,bbox_to_anchor=[0.5, +1.1],loc='upper center', ncol = 6, frameon=False)
ax.set_ylim([-0.01,0.5])
################################################################################################
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.08,right = 0.92)
fig.savefig("fig/fig_granger.pdf")