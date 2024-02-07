import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz

matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################################
################################################################################
################################################################################
################################################################################
est = pytz.timezone('US/Eastern')
y = 180
x = 250
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
################################################################################################
with open("data/adopting_bb_amc_nok.csv", "r") as inpuf:
    df = pd.read_csv(inpuf,sep = ";")
df["first_time"] = df["first_time"].apply(lambda x: datetime.fromtimestamp(int(x),tz = est))
df["first_time"] = df["first_time"].apply(lambda x: datetime(x.year,x.month,x.day))
gdf = df.groupby(by = ["first_time"]).agg({"author":"count"}).reset_index()
gdf["author"] = gdf["author"].rolling(5).mean()
start_date = datetime(2020,12,5)
final_date = datetime(2021,2,5)
gdf = gdf[(gdf["first_time"] > start_date) & (gdf["first_time"] < final_date)]
################################################################
ax = fig.add_subplot(1,1,1)
lab_ax = ax.plot(gdf["first_time"],gdf["author"],color = "#e63946",lw = 30,ls = "solid",label = "BB, AMC, NOK")
ax.set_xlabel("Date",fontsize = fontsize*0.7)
ax.set_ylabel("Number of Users BB,AMC,NOK",fontsize = fontsize*0.7,labelpad = 32)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dotted")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.set_yscale("log")
ax.set_ylim([10,10**5])
################################################################
with open("data/not_talking_nio.csv", "r") as inpuf:
    df = pd.read_csv(inpuf,sep = ";")
df["last_time"] = df["last_time"].apply(lambda x: datetime.fromtimestamp(int(x),tz = est))
df["last_time"] = df["last_time"].apply(lambda x: datetime(x.year,x.month,x.day))
gdf = df.groupby(by = ["last_time"]).agg({"author":"count"}).reset_index()
gdf["author"] = gdf["author"].rolling(5).mean()
start_date = datetime(2020,12,5)
final_date = datetime(2021,2,5)
gdf = gdf[(gdf["last_time"] > start_date) & (gdf["last_time"] < final_date)]
################################################################
tax = ax.twinx()
lab_tax = tax.plot(gdf["last_time"],gdf["author"],color = "#1d3557",lw = 30,ls = "solid",label = "NIO")
tax.set_ylabel("Number of Users NIO",fontsize = fontsize*0.7,labelpad = 220, rotation = 270)
tax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
tax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
tax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
tax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
tax.set_ylim([40,400])
################################################################################################
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.1,right = 0.9)
lns = lab_ax+lab_tax
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc = "upper center",bbox_to_anchor=[0.55, +1.05],ncol = 4,fontsize = fontsize/2,frameon = False)
fig.savefig("fig/leaving_adopting.pdf")
