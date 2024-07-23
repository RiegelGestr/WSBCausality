import pandas as pd
import json
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54


remove_garbage = [
    "cost","exp","ago","nov","live","net","max","cash","gain","jan","view",
    "best","mar","apr","app","iii","lmt","dow","expr","val"
]
with open("data/screenshot_tickers.json","r") as inpuf:
    data = json.load(inpuf)
outpuf = []
for (_,list_tickers) in data.items():
    if len(list_tickers) < 2:
        continue
    combos = combinations(list_tickers,2)
    for combo in combos:
        min_c = min(combo)
        max_c = max(combo)
        if min_c in remove_garbage or max_c in remove_garbage:
            continue
        if min_c == max_c:
            continue
        outpuf.append({"comb":min_c.upper() + "--" + max_c.upper(),"value":1})
df = pd.DataFrame(outpuf)
gdf = df.groupby(by = ["comb"]).agg({"value":"sum"}).reset_index()
gdf = gdf.sort_values(by = ["value"])
only_these_stocks = ["NIO","TSLA","PLTR","GME","AMC","NOK","BB"]
odf = pd.DataFrame([{
                    "Source":row["comb"].split("--")[0],
                    "Target":row["comb"].split("--")[1],
                    "weight":row["value"]
                    } for _,row in gdf.iterrows() if row["comb"].split("--")[0] in only_these_stocks or row["comb"].split("--")[1] in only_these_stocks])
odf = odf[odf["weight"] > 50]
odf.to_csv("data/network.csv",sep = ",",index = False)
print(odf.to_latex(index = False))