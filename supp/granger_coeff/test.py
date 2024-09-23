import pandas as pd
from datetime import timedelta, datetime
from statsmodels.tsa.stattools import lagmat2ds
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant


for stock in ["GME"]:
    ################################################################
    with open("../../main/data/"+stock+"_causality.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    df["date"] = pd.to_datetime(df["date"])
    start_date = datetime(2020,12,1)
    dates = [(start_date +i*timedelta(days = 1),start_date +i*timedelta(days = 1)+timedelta(days = 15)) for i in range(1,60)]
    max_lag = 7
    results = []
    for date in dates:
        gdf = df[(df["date"] > date[0]) & (df["date"] < date[1])]
        #in the second column Granger causes the time series in the first column
        #second column is cause, first column is effect
        #"Market --> Reddit
        #
        dta = lagmat2ds(gdf[["occurrences","volume"]], max_lag, trim="both", dropex=1,use_pandas = True)
        dta = lagmat2ds(gdf[["occurrences"]], max_lag, trim="both", dropex=1,use_pandas = True)
        cols = ["occurrences.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
        #cols.extend(["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)])
        dtaown = add_constant(dta[cols],prepend=False)
        Y = dta[["occurrences"]]
        for i in range(1,max_lag+1):
            cols2 = ["volume.L.{i}".format(i = str(i)),"occurrences.L.{i}".format(i = str(i)),"const"]
            cols2 = ["occurrences.L.{i}".format(i = str(i)),"const"]
            dta2 = dtaown[cols2]
            res2down = OLS(Y,dta2).fit()
            #
            results.append({
                "date":date[1],
                "coeff_occurrences":res2down.params["occurrences.L.{i}".format(i = str(i))],
                "const":res2down.params["const"],
                "p_occurrences":res2down.pvalues["occurrences.L.{i}".format(i = str(i))],
                "lag":i,
                "kind":"Reddit",
            })
            #
        #in the second column Granger causes the time series in the first column
        #second column is cause, first column is effect
        #Reddit --> Market
        dta = lagmat2ds(gdf[["volume","occurrences"]], max_lag, trim="both", dropex=1,use_pandas = True)
        dta = lagmat2ds(gdf[["volume"]], max_lag, trim="both", dropex=1,use_pandas = True)
        cols = ["volume.L.{i}".format(i = str(i)) for i in range(1,max_lag+1)]
        dtaown = add_constant(dta[cols],prepend=False)
        Y = dta[["volume"]]
        for i in range(1,max_lag+1):
            cols2 = ["volume.L.{i}".format(i = str(i)),"occurrences.L.{i}".format(i = str(i)),"const"]
            cols2 = ["volume.L.{i}".format(i = str(i)),"const"]
            dta2 = dtaown[cols2]
            res2down = OLS(Y,dta2).fit()
            #
            results.append({
                "date":date[1],
                "coeff_volume":res2down.params["volume.L.{i}".format(i = str(i))],
                "const":res2down.params["const"],
                "p_volume":res2down.pvalues["volume.L.{i}".format(i = str(i))],
                "lag":i,
                "kind":"Market",
            })
            #
    #
    xdf = pd.DataFrame(results)
    xdf.to_csv("mva_single_"+stock+".csv",index = False, sep = ";")
