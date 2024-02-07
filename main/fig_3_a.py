import pandas as pd
import numpy as np
import json
from scipy.stats import entropy
import matplotlib.pyplot as plt
from random import shuffle
from datetime import datetime
import seaborn as sns
from itertools import combinations
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################################
################################################################################
################################################################################
################################################################################
with open("data/ranking.csv","r") as inpuf:
    df = pd.read_csv(inpuf,sep = ",")
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"]>datetime(2020,12,15)]
df = df[df["date"]<datetime(2021,2,15)]
df = df.sort_values(by = ["date"])
dict_colors = {
    "GME":"#B92113",
    "AMC":"#FF8000",
    "BB":"#FFD700",
    "NOK":"#00CC66",
    "NIO":"#00A8E8",
    "TSLA":"#5E35B1",
    "PLTR":"#28367B"
}
y = 140
x = 220
fontsize = 120
dict_data = {}
for symbol in ["GME","AMC","BB","NOK","NIO","TSLA","PLTR"]:
    xdf = df[df["Symbol"] == symbol]
    xdf["value"] = xdf["value"].cumsum()
    dict_data[symbol] = (xdf["date"],xdf["value"])
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
for symbol in ["AMC","BB","NOK","NIO","TSLA","PLTR"]:
    if symbol in ["AMC","BB","NOK"]:
        ax = ax1
    else:
        ax = ax2
    gme = dict_data["GME"]
    oth_symbol = dict_data[symbol]
    ax.plot(gme[0],gme[1],c = dict_colors["GME"],lw = 30)
    ax.plot(oth_symbol[0],oth_symbol[1],c = dict_colors[symbol],lw = 30)
    for symbol2 in ["AMC","BB","NOK","NIO","TSLA","PLTR"]:
        if symbol2 == symbol:
            continue
        oth_symbol = dict_data[symbol2]
        ax.plot(oth_symbol[0],oth_symbol[1],c = "#A0ACBA",lw = 5)
    ax.set_yscale("log")
    ax.set_ylim([10**1,10**6])
    if symbol in ["AMC","BB","NOK"]:
        ax.set_ylabel("Cumulative Occurrences",fontsize = fontsize*0.7)
    else:
        ax.set_yticklabels([], rotation = 0, ha='right')
    ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 25,color = "#9AA3B3",ls = "dashed")
    ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 25,color = "#9AA3B3",ls = "dashed")
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
    ax.set_xlabel("Date",fontsize = fontsize*0.7)
    #ax.set_title(symbol, fontsize = fontsize)
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.1,right = 0.9,hspace = 0.1,wspace = 0.05)
fig.savefig("fig/fig_3_A.pdf")
