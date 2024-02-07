import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################################
################################################################################
################################################################################
################################################################################
y = 140
x = 220
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
dict_color = {
    "NOK":{
        "Market --> Reddit":"green",
        "Reddit --> Market":"#C9AA9C",
    },
    "AMC":{
        "Market --> Reddit":"green",
        "Reddit --> Market":"#611305",
    },
    "BB":{
        "Market --> Reddit":"#FFE6A7",
        "Reddit --> Market":"#B91321",
    }
}
for stock in ["NOK","BB","AMC"]:
    with open("data/granger_index_"+stock+".csv") as inpuf:
        df = pd.read_csv(inpuf,sep = ";")
    df["date"] = pd.to_datetime(df["date"],format = "%Y-%m-%d")
    xdf = df[df["lag"] == 1]
    thr = 0.1
    start_date = datetime(2021,1,5)
    final_date = datetime(2021,2,5)
    xdf = xdf[(xdf["date"]>start_date) & (xdf["date"]<final_date)]
    #
    if stock == "BB":
        kind = "Market --> Reddit"
        color = dict_color[stock][kind]
        df = xdf[(xdf["kind"] == kind)]
        ax.plot(df["date"],df["gc_index"],color = color,lw = 30)
        df = df[df["gc_p"] < thr]
        ax.scatter(df["date"],df["gc_index"],color = color,s = 15_000,alpha = .5, marker = "^")
    #
    kind = "Reddit --> Market"
    color = dict_color[stock][kind]
    df = xdf[(xdf["kind"] == kind)]
    ax.plot(df["date"],df["gc_index"],color = color,lw = 30)
    df = df[df["gc_p"] < thr]
    ax.scatter(df["date"],df["gc_index"],color = color,s = 15_000,alpha = .5, marker = "^")
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
ax.legend(fontsize = fontsize*0.4,bbox_to_anchor=[0.5, +1.05],loc='upper center', ncol = 6, frameon=False)
ax.set_ylim([-0.01,0.3])
################################################################################################
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.08,right = 0.92)
fig.savefig("fig/fig_3_B.pdf")
