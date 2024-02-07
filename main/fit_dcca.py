import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


def func_linlaw(x, a,b):
    return a + b*x


def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c


#
dict_labels = {
    "price_volume_coeff":"Price - Trading V.",
    "price_occurrences_coeff":"Price - Reddit",
    "occurrences_volume_coeff":"Trading V. - Reddit",
    "volume_volume_coeff":"Trading V. - Trading V.",
    "price_price_coeff":"Price - Price",
    "occurrences_occurrences_coeff":"Reddit - Reddit"
}
results = []
for id,stock in enumerate(["BB","AMC","NOK"]):
    with open("data/"+stock+"_dcca.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    for col in dict_labels.keys():
        df = df.dropna()
        df = df[df[col]>0.0]
        xs = df["window_size"]
        ys = df[col]
        popt, pcov = curve_fit(func_linlaw, np.log10(xs)[12:], np.log10(ys)[12:])
        results.append({
            "stock": stock,
            "label": dict_labels[col],
            "lambda": round(popt[1]*0.5,3)
        })
for id,stock in enumerate(["GME"]):
    with open("data/"+stock+"_dcca.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    for col in dict_labels.keys():
        df = df.dropna()
        df = df[df[col]>0.0]
        xs = df["window_size"]
        ys = df[col]
        popt, pcov = curve_fit(func_linlaw, np.log10(xs)[13:], np.log10(ys)[13:])
        results.append({
            "stock": stock,
            "label": dict_labels[col],
            "lambda":round(popt[1]*0.5,3)
        })
df = pd.DataFrame(results)

print(df.to_latex(index=False))