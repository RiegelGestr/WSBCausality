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
y = 140
x = 260
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
with open("data/posts_reply_speed.csv","r") as inpuf:
    df = pd.read_csv(inpuf)
#
df = df.dropna()
df["init_post"] = df.apply(lambda x: datetime.fromtimestamp(int(x["init_post"]),tz = est),axis = 1)
df["wd"] = df["init_post"].dt.dayofweek
df = df[df["wd"] < 5]
df["hour"] = df["init_post"].dt.hour
df = df[df["hour"].isin(list(range(9,16)))]
df["rank_num_comments"] = df.groupby(by = ["date"])["num_comments"].rank("first", ascending = False)
df = df.sort_values(by = ["rank_num_comments"])
df["date"] = pd.to_datetime(df["date"],format = "%d/%m/%Y")
df = df.sort_values(by = ["date"])
df["delta_answs"] = df["delta_answs"]/3600
gdf = df.groupby(by = ["date"]).apply(
    lambda x: pd.Series({
        'delta_answs' : np.average(x['delta_answs'], weights=x['num_comments']),
        'error_answs': np.sqrt(
            np.average(
                np.power(x['delta_answs']
                         - np.average(x['delta_answs'], weights = x['num_comments']),2),
                weights = x['num_comments'])),
        'number_answs' : x['delta_answs'].shape[0]
    })).reset_index()
gdf["date"] = pd.to_datetime(gdf["date"],format = "%d/%m/%Y")
gdf = gdf.sort_values(by = ["date"])
gdf["error_answs"] = gdf["error_answs"]/np.sqrt(gdf["number_answs"])
gdf["delta_answs"] = gdf["delta_answs"].rolling(5).mean()
gdf["error_answs"] = gdf["error_answs"].rolling(5).mean()
gdf = gdf[gdf["date"] > datetime(2021,1,5)]
gdf = gdf[gdf["date"] < datetime(2021,2,5)]
#
answer_tax = ax.scatter(gdf["date"],gdf["delta_answs"],s = 15_000,edgecolor = "#DB4375",facecolor=(0.8588235294117647,0.2627450980392157,0.4588235294117647,0.5),marker = "o",linewidths = 25,label = "Reply")
ax.plot(gdf["date"],gdf["delta_answs"],lw = 30,color = "#DB4375")
ax.fill_between(gdf["date"],gdf["delta_answs"]-gdf["error_answs"],gdf["delta_answs"]+gdf["error_answs"],alpha = 0.3, color = "#DB4375")
#tax.set_ylim([0.5,3])
ax.set_ylabel("Reply Speed [hour]",fontsize = fontsize*0.7 )
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_ylim([0.0,3])
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
#
ax.legend([], [], fontsize = fontsize*0.5,bbox_to_anchor=[0.5, +1.1],loc='upper center', ncol = 6, frameon=False)
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.92, bottom = 0.08,left = 0.1,right = 0.9)
fig.savefig("fig/fig_2_C.pdf")