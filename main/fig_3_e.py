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
dict_color = {
    "GME_NOK_jaccard":"#D389FB",
    "GME_AMC_jaccard":"#A532EC",
    "GME_BB_jaccard":"#5F198A",
    "GME_NIO_jaccard":"#E0B000",
    "GME_TSLA_jaccard":"#FFDA1F",
    "GME_PLTR_jaccard":"#FFF799",
    #
    "GME_NOK_overlap":"#FFD6E0",
    "GME_AMC_overlap":"#FF99B3",
    "GME_BB_overlap":"#FF4775",
    "GME_NIO_overlap":"#35AC90",
    "GME_TSLA_overlap":"#74D2BC",
    "GME_PLTR_overlap":"#BDEFE3",
}
#
with open("data/users_stocks_jaccard_overlap.csv","r") as inpuf:
    df = pd.read_csv(inpuf,sep = ",")
stocks = ["AMC","BB","NOK"]
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"].dt.date > datetime(2020,12,15).date()]
df = df[df["date"].dt.date < datetime(2021,2,15).date()]
y = 150
x = 280
fontsize = 150
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
#1
ax = fig.add_subplot(1,2,1)
xs = df.date
for stock in stocks:
    ts = df["GME_"+stock+"_jaccard"]
    ax.plot(xs,ts, lw = 30,label = "GME-"+stock,color = dict_color["GME_"+stock+"_jaccard"])
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.set_ylabel("Jaccard",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_ylim([0,0.8])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend(fontsize = 0.5*fontsize,bbox_to_anchor=[0.5, 1.05],loc='center', ncol = 3, frameon=False)
ax = fig.add_subplot(1,2,2)
xs = df.date
for stock in ["NIO","PLTR","TSLA"]:
    ts = df["GME_"+stock+"_jaccard"]
    ax.plot(xs,ts, lw = 30,label = "GME-"+stock,color = dict_color["GME_"+stock+"_jaccard"])
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_ylim([0,0.8])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
ax.set_yticklabels([], rotation = 0, ha='right')
ax.legend(fontsize = 0.5*fontsize,bbox_to_anchor=[0.5, 1.05],loc='center', ncol = 3, frameon=False)
#
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.1,right = 0.9,wspace = 0.1)
fig.savefig("fig/fig_3_E.pdf")
