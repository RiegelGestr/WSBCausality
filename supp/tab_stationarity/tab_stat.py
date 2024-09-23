import pandas as pd
import numpy as np
from datetime import timedelta,datetime
from statsmodels.tsa.stattools import grangercausalitytests,adfuller

########################################################################
with open("../../main/data/GME_causality_with_twitter.csv","r") as inpuf:
    df = pd.read_csv(inpuf)
df["date"] = pd.to_datetime(df["date"])
start_date = df.iloc[0]["date"]
dates = [(start_date +i*timedelta(days = 1),start_date +i*timedelta(days = 1)+timedelta(days = 15)) for i in range(1,60)]
max_lag = 1
results = []
for date in dates:
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    #
    dftest = adfuller(gdf["occurrences"],regression = "c", maxlag = max_lag)
    df_p_occ = dftest[1]
    df_ts_occ = dftest[0]
    dftest = adfuller(gdf["volume"],regression = "c", maxlag = max_lag)
    df_p_vol = dftest[1]
    df_ts_vol = dftest[0]
    dftest = adfuller(gdf["tweets"],regression = "c", maxlag = max_lag)
    df_p_twt = dftest[1]
    df_ts_twt = dftest[0]
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["occurrences","volume"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_market_to_reddit = np.log10(ssr_single/ssr_both)
    p_value_market_to_reddit = gc_p
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["volume","occurrences"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_reddit_to_market = np.log10(ssr_single/ssr_both)
    p_value_reddit_to_market = gc_p
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["tweets","occurrences"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_reddit_to_twitter = np.log10(ssr_single/ssr_both)
    p_value_reddit_to_twitter = gc_p
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["occurrences","tweets"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_twitter_to_reddit = np.log10(ssr_single/ssr_both)
    p_value_twitter_to_reddit = gc_p
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["tweets","volume"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_market_to_twitter = np.log10(ssr_single/ssr_both)
    p_value_market_to_twitter = gc_p
    #
    #in the second column Granger causes the time series in the first column
    gc_res = grangercausalitytests(gdf[["volume","tweets"]], max_lag,verbose = False,addconst = True)[1]
    gc_p = gc_res[0]["ssr_ftest"][1]
    #pvalue
    res_single = gc_res[1][0]
    res_both = gc_res[1][1]
    ssr_single = res_single.ssr
    ssr_both = res_both.ssr
    gc_index_twitter_to_market = np.log10(ssr_single/ssr_both)
    p_value_twitter_to_market = gc_p
    #save
    results.append({"Date":date[1],
                    "t (Twitter)":round(df_ts_twt,3),
                    "p-value (Twitter)":round(df_p_twt,3),
                    "t (Trading Volume)":round(df_ts_vol,3),
                    "p-value (Trading Volume)":round(df_p_vol,3),
                    "t (Reddit)":round(df_ts_occ,3),
                    "p-value (Reddit)":round(df_p_occ,3),
                    "GC-index (Reddit --> Trading Volume)":round(gc_index_reddit_to_market,3),
                    "p-value (Reddit --> Trading Volume)":round(p_value_reddit_to_market,3),
                    "GC-index (Trading Volume --> Reddit)":round(gc_index_market_to_reddit,3),
                    "p-value (Trading Volume --> Reddit)":round(p_value_market_to_reddit,3),
                    "GC-index (Twitter --> Reddit)":round(gc_index_twitter_to_reddit,3),
                    "p-value (Twitter --> Reddit)":round(p_value_twitter_to_reddit,3),
                    "GC-index (Reddit --> Twitter)":round(gc_index_reddit_to_twitter,3),
                    "p-value (Reddit --> Twitter)":round(p_value_reddit_to_twitter,3),
                    "GC-index (Twitter --> Trading Volume)":round(gc_index_twitter_to_market,3),
                    "p-value (Twitter --> Trading Volume)":round(p_value_twitter_to_market,3),
                    "GC-index (Trading Volume --> Twitter)":round(gc_index_market_to_twitter,3),
                    "p-value (Trading Volume --> Twitter)":round(p_value_market_to_twitter,3),
                    })
df = pd.DataFrame(results)
print(df[[
    "Date","t (Twitter)","p-value (Twitter)","t (Trading Volume)","p-value (Trading Volume)","t (Reddit)","p-value (Reddit)"
]].to_latex(index = False))
df = df[df["Date"] > datetime(2021,1,1)]
print(df[[
    "Date",
    "p-value (Reddit --> Trading Volume)","p-value (Trading Volume --> Reddit)",
    "p-value (Reddit --> Twitter)","p-value (Twitter --> Reddit)",
    "p-value (Twitter --> Trading Volume)","p-value (Trading Volume --> Twitter)",
]].to_latex(index = False))
