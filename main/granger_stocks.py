import pandas as pd
import numpy as np
from datetime import timedelta,datetime
from statsmodels.tsa.stattools import grangercausalitytests

for stock in ["NOK","BB","AMC"]:
    with open("data/"+stock+"_causality.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    df["date"] = pd.to_datetime(df["date"])
    start_date = datetime(2020,12,1)
    dates = [(start_date +i*timedelta(days = 1),start_date +i*timedelta(days = 1)+timedelta(days = 15)) for i in range(1,60)]
    max_lag = 7
    #
    results = []
    for date in dates:
        #
        gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
        #test stationarity DF
        #in the second column Granger causes the time series in the first column
        gc_res = grangercausalitytests(gdf[["occurrences","volume"]], max_lag,verbose = False,addconst = True)
        #
        for (k,v) in gc_res.items():
            #pvalue
            gc_p = v[0]["ssr_ftest"][1]
            #pvalue
            res_single = v[1][0]
            res_both = v[1][1]
            ssr_single = res_single.ssr
            ssr_both = res_both.ssr
            params_single = res_single.params
            params_both = res_both.params
            results.append({
                "date":date[1],
                "gc_index":np.log10(ssr_single/ssr_both),
                "gc_p":gc_p,
                "lag":k,
                "kind":"Market --> Reddit",
            })
        #in the second column Granger causes the time series in the first column
        gc_res = grangercausalitytests(gdf[["volume","occurrences"]], max_lag,verbose = False,addconst = True)
        for (k,v) in gc_res.items():
            #pvalue
            gc_p = v[0]["ssr_ftest"][1]
            #pvalue
            res_single = v[1][0]
            res_both = v[1][1]
            ssr_single = res_single.ssr
            ssr_both = res_both.ssr
            params_single = res_single.params
            params_both = res_both.params
            results.append({
                "date":date[1],
                "gc_index":np.log(ssr_single/ssr_both),
                "gc_p":gc_p,
                "lag":k,
                "kind":"Reddit --> Market",
            })
    xdf = pd.DataFrame(results)
    xdf.to_csv("data/granger_index_"+stock+".csv",index = False, sep = ";")
