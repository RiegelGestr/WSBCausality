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
stock = "BB"
with open("data/mva_"+stock+".csv") as inpuf:
    df = pd.read_csv(inpuf,sep = ";")
df["date"] = pd.to_datetime(df["date"],format = "%Y-%m-%d")
xdf = df[df["lag"] == 1]
thr = 0.1
start_date = datetime(2021,1,5)
final_date = datetime(2021,2,5)
xdf = xdf[(xdf["date"]>start_date) & (xdf["date"]<final_date)]
y = 280
x = 220
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
################################################################################################
#################################################
color_reddit = "#FF7733"
color_market = "#0006B3"
ax = fig.add_subplot(2,1,1)
ldf = xdf[xdf["kind"] == "Reddit"]
#
ax.plot(ldf["date"],ldf["coeff_occurrences"],color = color_reddit,lw = 30,label = "Reddit",ls = "solid")
ax.plot(ldf["date"],ldf["coeff_volume"],color = color_market,lw = 30,label = "Market",ls = "dashed")
ax.axhline(0.0,color = "#9AA3B3",lw = 16,ls = "solid")
#
pldf = ldf[ldf["p_occurrences"] < thr]
ax.scatter(pldf["date"],pldf["coeff_occurrences"],color = color_reddit,s = 15_000,alpha = .5, marker = "^")
pldf = ldf[ldf["p_volume"] < thr]
ax.scatter(pldf["date"],pldf["coeff_volume"],color = color_market,s = 15_000,alpha = .5, marker = "^")
#
#ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.set_ylabel("Coefficient",fontsize = fontsize*0.7,labelpad = 32)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
#ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
ax.set_xticklabels([])
ax.legend(fontsize = fontsize*0.5,loc='upper right', ncol = 6, frameon=False)
ax.set_title("Reddit",fontsize = fontsize*0.7,loc = "left")
ax.set_ylim([-2,+2])
#
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
#################################################
ax = fig.add_subplot(2,1,2)
ldf = xdf[xdf["kind"] == "Market"]
#
ax.plot(ldf["date"],ldf["coeff_occurrences"],color = color_reddit,lw = 30,label = "Reddit",ls ="solid")
ax.plot(ldf["date"],ldf["coeff_volume"],color = color_market,lw = 30,label = "Market",ls = "dashed")
ax.axhline(0.0,color = "#9AA3B3",lw = 16,ls = "solid")
#
pldf = ldf[ldf["p_occurrences"] < thr]
ax.scatter(pldf["date"],pldf["coeff_occurrences"],color = color_reddit,s = 15_000,alpha = .5, marker = "^")
pldf = ldf[ldf["p_volume"] < thr]
ax.scatter(pldf["date"],pldf["coeff_volume"],color = color_market,s = 15_000,alpha = .5, marker = "^")
#
ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.set_ylabel("Coefficient",fontsize = fontsize*0.7,labelpad = 32)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
ax.legend(fontsize = fontsize*0.5,loc='upper right', ncol = 6, frameon=False)
ax.set_title("Market",fontsize = fontsize*0.7,loc = "left")
ax.set_ylim([-2,+2])
#
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
################################################################################################
fig.subplots_adjust(left = 0.1,right = 0.9,top = 0.95,bottom = 0.05,hspace = 0.1,wspace = 0.05)
fig.savefig("fig/fig_3_C.pdf")
