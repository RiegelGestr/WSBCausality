import json
from datetime import timedelta
import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
##############################################################################################################
with open("../../main/data_only_zenodo/stocks_infos_authors.json","r") as inpuf:
    data = json.load(inpuf)
stocks = ["GME","AMC","BB","NOK","NIO","PLTR","TSLA"]
dates = [datetime.strptime(k, "%d/%m/%Y") for k in data.keys()]
dates.sort()
dates = dates[30:]
window_dates = {d.strftime(format = "%d/%m/%Y"):[(d-timedelta(days = i)).strftime(format = "%d/%m/%Y") for i in range(0,5)]for d in dates}
######################
dict_data = []
for (starting_date, sdates) in window_dates.items():
    tmp_dict = {}
    dict_stocks = {stock:[] for stock in stocks}
    for sdate in sdates:
        dict_stock_list = data[sdate]
        for (stock,marked_data) in dict_stock_list.items():
            if stock in stocks:
                for author in marked_data:
                    dict_stocks[stock].append(author[3])
    date = datetime.strptime(starting_date,"%d/%m/%Y")
    dict_data.append({
        "sdate": starting_date,
        "date":date,
        "GME":len(set(dict_stocks["GME"])),
        "AMC":len(set(dict_stocks["AMC"])),
        "BB":len(set(dict_stocks["BB"])),
        "NOK":len(set(dict_stocks["NOK"])),
        "NIO":len(set(dict_stocks["NIO"])),
        "PLTR":len(set(dict_stocks["PLTR"])),
        "TSLA":len(set(dict_stocks["TSLA"])),
        "GME-BB": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["BB"]))
        ),
        "GME-u-BB": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["BB"]))
        ),
        "GME-AMC": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["AMC"]))
        ),
        "GME-u-ACM": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["AMC"]))
        ),
        "GME-NOK": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["NOK"]))
        ),
        "GME-u-NOK": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["NOK"]))
        ),
        "GME-NIO": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["NIO"]))
        ),
        "GME-u-NIO": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["NIO"]))
        ),
        "GME-PLTR": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["PLTR"]))
        ),
        "GME-u-PLTR": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["PLTR"]))
        ),
        "GME-TSLA": len(
            set(dict_stocks["GME"]).intersection(set(dict_stocks["TSLA"]))
        ),
        "GME-u-TSLA": len(
            set(dict_stocks["GME"]).union(set(dict_stocks["TSLA"]))
        ),
    })
########################################################################################
df = pd.DataFrame(dict_data)
df = df[df["date"].dt.date > datetime(2020,12,15).date()]
df = df[df["date"].dt.date < datetime(2021,2,15).date()]
########################################################################################
dict_color = {
    "GME":"#B92113",
    "AMC":"#FF8000",
    "BB":"#FFD700",
    "NOK":"#00CC66",
    "NIO":"#00A8E8",
    "TSLA":"#5E35B1",
    "PLTR":"#28367B",
    #
    "GME-NOK":"#FFD6E0",
    "GME-AMC":"#FF99B3",
    "GME-BB":"#FF4775",
    "GME-NIO":"#35AC90",
    "GME-TSLA":"#74D2BC",
    "GME-PLTR":"#BDEFE3",
}
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
y = 180
x = 250
fontsize = 200
stocks = ["AMC","BB","NOK","NIO","PLTR","TSLA"]
for stock in stocks:
    #
    fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
    #
    ax = fig.add_subplot(1,1,1)
    #
    ax.plot(df.date,df["GME"], lw = 30,color = dict_color["GME"],label = "GME")
    ax.plot(df.date,df[stock], lw = 30,color = dict_color[stock],label = stock)
    ax.plot(df.date,df["GME-"+stock], lw = 30,color = dict_color["GME-"+stock],label = "GME - "+stock)
    #
    ax.set_xlabel("Date",fontsize = fontsize*0.7)
    ax.set_ylabel("Number of Users",fontsize = fontsize*0.7,labelpad = 32)
    #
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, ha='right')
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.3)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.3)
    #
    ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dotted")
    ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
    #
    ax.set_yscale("log")
    ax.set_ylim([1,10**6])
    #
    fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.1,right = 0.9)
    ax.legend(loc = "upper center",bbox_to_anchor=[0.55, +1.05],ncol = 4,fontsize = fontsize/2,frameon = False)
    #
    fig.savefig("fig/"+stock+".pdf")

