import pandas as pd
import json
from itertools import combinations
from tqdm import tqdm
from datetime import datetime,timedelta


#
def overlap_without_c(list_x,list_y,list_c):
    set_x = set(list_x)
    set_y = set(list_y)
    set_c = set(list_c)
    set_x = set_x.difference(set_c)
    set_y = set_y.difference(set_c)
    den = min(len(set_x),len(set_y))
    nominator = set_x.intersection(set_y)
    if den == 0:
        return 0
    else:
        return len(nominator)/den


#
def jaccard_sim_without_c(list_x,list_y,list_c):
    set_x = set(list_x)
    set_y = set(list_y)
    set_c = set(list_c)
    set_x = set_x.difference(set_c)
    set_y = set_y.difference(set_c)
    nominator = set_x.intersection(set_y)
    denominator = set_x.union(set_y)
    if len(denominator) == 0:
        return 0
    else:
        return len(nominator)/len(denominator)


#
def overlap(list_x,list_y):
    set_x = set(list_x)
    set_y = set(list_y)
    den = min(len(set_x),len(set_y))
    nominator = set_x.intersection(set_y)
    return len(nominator)/den


#
def overlap_users(list_x,list_y):
    set_x = set(list_x)
    set_y = set(list_y)
    nominator = set_x.intersection(set_y)
    return len(nominator)


#
def jaccard_sim(list_x,list_y):
    set_x = set(list_x)
    set_y = set(list_y)
    nominator = set_x.intersection(set_y)
    denominator = set_x.union(set_y)
    return len(nominator)/len(denominator)


################################################################################################
with open("data_only_zenodo/stocks_infos_authors.json","r") as inpuf:
    data = json.load(inpuf)
stocks = ["GME","AMC","BB","NOK","NIO","PLTR","TSLA"]
combos = list(combinations(stocks,2))
cooc_tot = []
dates = [datetime.strptime(k, "%d/%m/%Y") for k in data.keys()]
dates.sort()
dates = dates[30:]
window_dates = {d.strftime(format = "%d/%m/%Y"):[(d-timedelta(days = i)).strftime(format = "%d/%m/%Y") for i in range(0,5)]for d in dates}
for (starting_date, sdates) in tqdm(window_dates.items()):
    tmp_dict = {}
    for sdate in sdates:
        dict_stock_list = data[sdate]
        for (stock,marked_data) in dict_stock_list.items():
            for datum in marked_data:
                if datum[3] not in tmp_dict:
                    tmp_dict[datum[3]] = []
                tmp_dict[datum[3]].append(stock)
    #HERE We are doing users > 1
    which_ones = {k:v for k,v in tmp_dict.items() if len(v) > 1}
    dict_combo = {c[0]+"_"+c[1]+"_jaccard":0 for c in combos}
    for c in combos:
        dict_combo[c[0]+"_"+c[1]+"_overlap"] = 0
        dict_combo[c[0]+"_"+c[1]+"_overlap_users"] = 0
        dict_combo[c[0]+"_"+c[1]+"_jaccard_noGME"] = 0
        dict_combo[c[0]+"_"+c[1]+"_overlap_noGME"] = 0
    stock_pool_users = {stock:[] for stock in stocks}
    #
    for (k,vs) in which_ones.items():
        for v in vs:
            if v in stocks:
                stock_pool_users[v].append(k)
    for stock in stocks:
        dict_combo[stock+"_users"] = len(set(stock_pool_users[stock]))
    for combo in combos:
        usersA = stock_pool_users[combo[0]]
        usersB = stock_pool_users[combo[1]]
        if len(usersA) == 0 or len(usersB) == 0:
            continue
        js = jaccard_sim(usersA,usersB)
        ovs = overlap(usersA,usersB)
        ovs_users = overlap_users(usersA,usersB)
        dict_combo[combo[0]+"_"+combo[1]+"_jaccard"] = js
        dict_combo[combo[0]+"_"+combo[1]+"_overlap"] = ovs
        dict_combo[combo[0]+"_"+combo[1]+"_overlap_users"] += ovs_users
        #
        if combo[0] == "GME" or combo[1] == "GME":
            continue
        usersC = stock_pool_users["GME"]
        js = jaccard_sim_without_c(usersA,usersB,usersC)
        ovs = overlap_without_c(usersA,usersB,usersC)
        dict_combo[c[0]+"_"+c[1]+"_jaccard_noGME"] = js
        dict_combo[c[0]+"_"+c[1]+"_overlap_noGME"] = ovs
    dict_combo["date"] = datetime.strptime(starting_date,"%d/%m/%Y")
    dict_combo["sdate"] = starting_date
    cooc_tot.append(dict_combo)
df = pd.DataFrame(cooc_tot)
df = df.sort_values(by = ["date"])
df.to_csv("data/users_stocks_jaccard_overlap.csv",index = False)