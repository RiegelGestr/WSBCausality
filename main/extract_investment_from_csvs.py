import pandas as pd
import os
import numpy as np
import re
from tqdm import tqdm


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


with open("data/wsb_screenshots_metadata.csv", "r") as inpuf:
    df = pd.read_csv(inpuf)
dict_flags = {row["pic_name"].split(".")[0]:row["has_gme_text"] for _,row in df.iterrows()}
files = [f for f in os.listdir("data_only_zenodo/csvs/") if f != ".DS_Store"]
dict_infos_screenshot = {}
dict_output = {}
for file in tqdm(files):
    key = file.split(".")[0]
    if key == "unknown":
        continue
    with open("data_only_zenodo/csvs/"+file, "r") as inpuf:
        df = pd.read_csv(inpuf,sep  = "\t",dtype = "string")
    tdf = df.astype(str)
    mdata = tdf.to_numpy()
    flag = False
    for x in mdata.reshape(-1):
        y = x.strip().lower()
        for z in ["value","gme","gamestop","investing"]:
            if z in y:
                flag = True
                if key not in dict_infos_screenshot:
                    dict_infos_screenshot[key] = {}
                    dict_infos_screenshot[key]["value"] = False
                    dict_infos_screenshot[key]["gme"] = False
                    dict_infos_screenshot[key]["gamestop"] = False
                    dict_infos_screenshot[key]["investing"] = False
                dict_infos_screenshot[key][z] = True
    if flag:
        dict_output[key] = []
        for x in mdata.reshape(-1):
            if has_numbers(x):
                dict_output[key].append(x)
################################################################
screenshots_to_keep = [
    "3v4e73djr6e61",
    "osxhcv505ld61",
    "r557em3t5ce61",
    "nzzcsmufgce61",
    "xho46kzt7yc61",
    "umexi73bv7e61",
    "muwvrqsbf9d61",
    "1ubfvqedmjd61",
    "oigq1k1r5yc61",
]
dict_values = {}
for (k, vs) in dict_output.items():
    for v in vs:
        if "C" in v:
            continue
        if "¥" in v:
            continue
        if "%" in v:
            continue
        if "/" in v:
            continue
        if "U" in v:
            continue
        if "#" in v:
            continue
        if "=" in v:
            continue
        if "~" in v:
            continue
        if "\\" in v:
            continue
        if "@" in v:
            continue
        if "s" in v:
            continue
        if "@" in v:
            continue
        if ":" in v:
            continue
        if "a" in v:
            continue
        if "N" in v:
            continue
        if "_" in v:
            continue
        if "+" in v:
            continue
        if "-" in v:
            continue
        if "*" in v:
            continue
        if "?" in v:
            continue
        if "!" in v:
            continue
        if "M" in v:
            continue
        if "$" in v:
            if k not in dict_values:
                dict_values[k] = []
            c = v.replace("$", "").replace(")", "").replace("(", "").replace("‘", "").replace("“", "").replace("'", "")
            c = c.split(".")[0].replace(",", "")
            try:
                s = float(c)
            except:
                continue
            if k in screenshots_to_keep:
                dict_values[k].append(s)
            if s > 10_000_000:
                continue
            if s < 100:
                continue
            dict_values[k].append(s)
tmp = []
for k in dict_values.keys():
    if len(dict_values[k]) == 0:
        continue
    dict_info = dict_infos_screenshot[k]
    tmp.append({
        "pic_name":k,
        "bool_value":dict_info["value"],
        "bool_gme":dict_info["gme"],
        "bool_gamestop":dict_info["gamestop"],
        "bool_investing":dict_info["investing"],
        "value_screenshot":np.max(dict_values[k])
    })
df_ocr = pd.DataFrame(tmp)
df_ocr.to_csv("data/screenshot_ocr.csv",sep = ",",index = False)