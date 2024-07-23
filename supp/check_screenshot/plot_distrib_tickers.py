import pandas as pd
import squarify
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54


with open("data/ticker_in_screenshots.csv","r") as inpuf:
    df = pd.read_csv(inpuf, sep = ",")
df = df.sort_values(by = ["count"])
remove_garbage = [
                    "cost","exp","ago","nov","live","net","max","cash","gain","jan","view",
                    "best","mar","apr","app","iii","lmt","dow","expr","val"
                  ]
df = df[df["count"]>100]
df = df[~df.symbol.isin(remove_garbage)]
dict_colors = {
    "gme":"#B92113",
    "amc":"#FF8000",
    "bb":"#FFD700",
    "nok":"#00CC66",
    "nio":"#00A8E8",
    "tsla":"#5E35B1",
    "pltr":"#28367B",
}
other = df[~df.symbol.isin(dict_colors.keys())]["count"].sum()
total = df["count"].sum()
values = []
colors = []
labels = []
for (k,v) in dict_colors.items():
    value = df[df["symbol"] == k]["count"].iloc[0]
    color = v
    values.append(value)
    colors.append(color)
    labels.append("{stock}: {value} %".format(stock = k.upper(), value = round(100*(value/total),1)))
values.append(other)
colors.append("#A0ACBA")
labels.append("Other (less than 2%): {value} %".format(value = round(100*(other/total),1)))
#colors = [ImageColor.getcolor(c, "RGB") for c in colors]
#
y = 140
x = 220
fontsize = 100
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
squarify.plot(
                ax = ax,
                sizes = values,color = colors,label = labels,
                text_kwargs = {'fontsize': fontsize, 'color': 'black'},
                pad = 0.25,alpha = 0.75
                )
ax.axis("off")
fig.savefig("fig/treemap.pdf")