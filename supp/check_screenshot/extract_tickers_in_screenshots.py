import pandas as pd
import os
from tqdm import tqdm
import json

with open("data/nasdaq.csv","r") as inpuf:
    nasdaq = pd.read_csv(inpuf, sep = ",")
symbols = [x.strip() for x in nasdaq["Symbol"].tolist() if len(x.strip()) > 2]
remove_stocks = ["COIN","YOU","ARE","EDIT","FOR","CAT","HAS","GOOD","ALL","WISH","HUGE","REAL","PLAY","VERY","LMAO","NOW","CAN","LINK","MMM","GET","OUT","SEE","BIG","PLUG","LOVE","POST","ANY","CUZ","IMO","RIDE","GAME","GMED","NEXT","NEW","LIFE","LOW","EVER","OPEN","FUND","TELL","USA","TECH","NYT","MAN","WELL","FREE","MARK","RUN","TWO","PAY","FLEX","LFG","VIA","GOLD"]
set_symbols = set(symbols)-set(remove_stocks)
symbols = list(set_symbols)
symbols.append("BB")
symbols = [x.lower() for x in symbols]
with open("../../main/data/wsb_screenshots_metadata.csv", "r") as inpuf:
    df = pd.read_csv(inpuf)
dict_flags = {row["pic_name"].split(".")[0]:row["has_gme_text"] for _,row in df.iterrows()}
files = [f for f in os.listdir("../../main/data_only_zenodo/csvs/") if f != ".DS_Store"]
dict_output = {}
dict_symbol_count = {k:0 for k in symbols}
for file in tqdm(files):
    key = file.split(".")[0]
    if key == "unknown":
        continue
    with open("../../main/data_only_zenodo/csvs/"+file, "r") as inpuf:
        df = pd.read_csv(inpuf,sep  = "\t",dtype = "string")
    tdf = df.astype(str)
    mdata = tdf.to_numpy()
    dict_output[key] = []
    for x in mdata.reshape(-1):
        y = x.strip().lower()
        if y in symbols:
            dict_output[key].append(y)
            dict_symbol_count[y] += 1
fdf = pd.DataFrame([{"symbol":k,"count":v} for (k,v) in dict_symbol_count.items()])
fdf.to_csv("data/ticker_in_screenshots.csv",sep = ",",index = False)
with open("data/screenshot_tickers.json", 'w') as file:
    json.dump(dict_output, file)