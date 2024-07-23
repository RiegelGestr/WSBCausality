import pandas as pd
from datetime import timedelta
from statsmodels.tsa.stattools import lagmat2ds
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant

########################################################################
with open("data/GME_causality_with_twitter.csv", "r") as inpuf:
    df = pd.read_csv(inpuf)
df["date"] = pd.to_datetime(df["date"])
start_date = df.iloc[0]["date"]
dates = [(start_date +i*timedelta(days = 1),start_date +i*timedelta(days = 1)+timedelta(days = 15)) for i in range(1,60)]
max_lag = 7
results = []
for date in dates:
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    #in the second column Granger causes the time series in the first column
    #second column is cause, first column is effect
    #Fit Reddit (all three together)
    #
    dta = lagmat2ds(gdf[["occurrences","volume","tweets"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    cols.extend(["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["occurrences"]]
    for i in range(1,max_lag+1):
        cols2 = ["volume.L.{i}".format(i = str(i)),"occurrences.L.{i}".format(i = str(i)),"tweets.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Reddit",
        })
    #in the second column Granger causes the time series in the first column
    #second column is cause, first column is effect
    #Fit Market (all three together)
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["volume","tweets","occurrences"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    cols.extend(["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["volume"]]
    for i in range(1,max_lag+1):
        cols2 = ["volume.L.{i}".format(i = str(i)),"occurrences.L.{i}".format(i = str(i)),"tweets.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Market",
        })
    #in the second column Granger causes the time series in the first column
    #second column is cause, first column is effect
    #Fit Twitter (all three together)
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["tweets","occurrences","volume"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    cols.extend(["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["tweets"]]
    for i in range(1,max_lag+1):
        cols2 = ["volume.L.{i}".format(i = str(i)),"occurrences.L.{i}".format(i = str(i)),"tweets.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Tweets",
        })
    #in the second column Granger causes the time series in the first column
    #second column is cause, first column is effect
    #Fit Twitter - Reddit
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["tweets","occurrences"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["tweets"]]
    for i in range(1,max_lag+1):
        cols2 = ["occurrences.L.{i}".format(i = str(i)),"tweets.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":0.0,
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":0.0,
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Tweets (Reddit)",
        })
    #Fit Reddit - Twitter
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["occurrences","tweets"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["occurrences"]]
    for i in range(1,max_lag+1):
        cols2 = ["occurrences.L.{i}".format(i = str(i)),"tweets.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":0.0,
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":0.0,
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Reddit (Tweets)",
        })
    #Fit Reddit - Market
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["occurrences","volume"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["occurrences"]]
    for i in range(1,max_lag+1):
        cols2 = ["occurrences.L.{i}".format(i = str(i)),"volume.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":0.0,
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":0.0,
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Reddit (Market)",
        })
    #Fit Market - Reddit
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["volume","occurrences"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["volume"]]
    for i in range(1,max_lag+1):
        cols2 = ["occurrences.L.{i}".format(i = str(i)),"volume.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
            "coeff_tweets":0.0,
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
            "p_tweets":0.0,
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Market (Reddit)",
        })
    #Fit Market - Twitter
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["volume","tweets"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["volume"]]
    for i in range(1,max_lag+1):
        cols2 = ["tweets.L.{i}".format(i = str(i)),"volume.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":0.0,
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":0.0,
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Market (Tweets)",
        })
    #Fit Twitter - Market
    #
    gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
    dta = lagmat2ds(gdf[["tweets","volume"]], max_lag, trim="both", dropex=1,use_pandas = True)
    cols = ["tweets.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
    cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
    dtaown = add_constant(dta[cols],prepend=False)
    Y = dta[["tweets"]]
    for i in range(1,max_lag+1):
        cols2 = ["tweets.L.{i}".format(i = str(i)),"volume.L.{i}".format(i = str(i)),"const"]
        dta2 = dtaown[cols2]
        res2down = OLS(Y,dta2).fit()
        #
        results.append({
            "date":date[1],
            "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
            "coeff_occurrences":0.0,
            "coeff_tweets":res2down.params["tweets.L.{i}".format(i = str(i))],
            "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
            "p_occurrences":0.0,
            "p_tweets":res2down.pvalues["tweets.L.{i}".format(i = str(i))],
            "const":res2down.params["const"],
            "lag":i,
            "kind":"Tweets (Market)",
        })
#
xdf = pd.DataFrame(results)
xdf.to_csv("data/mva_GME_with_twitter.csv",index = False, sep = ";")
