import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################
with open("data/market_cap_GME.csv","r") as inpuf:
    market_cap = pd.read_csv(inpuf)
market_cap["date"] = pd.to_datetime(market_cap["date"])
with open("data/WSB_portfolio.csv","r") as inpuf:
    wsb_portfolio = pd.read_csv(inpuf)
wsb_portfolio["date"] = pd.to_datetime(wsb_portfolio["date"])
df = pd.merge(market_cap,wsb_portfolio,on = "date")
df = df[df["date"].dt.date > datetime(2020,12,1).date()]
avg_ratio = (df["portfolio"]/df["market_cap"]).mean()
print(avg_ratio)
y = 120
x = 130
fontsize = 120
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
tax = ax.twinx()
ax_line = ax.plot(df["date"], df["portfolio"], lw = 15, color="#FFA666",label = "WSB Portfolio")
tax_line = tax.plot(df["date"], df["market_cap"], lw = 20, color="#24748F",ls = "dashed",label = "Market Capitalization")
ax.scatter(df["date"], df["portfolio"],s = 4_500,edgecolor = "#FFA666", facecolor = (1.0, 0.6509803921568628, 0.4, 0.5),linewidths = 10,marker = "o")
#######################################
ax.axvline(datetime(2021,1,13),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.axvline(datetime(2021,1,27),ymin = 0.1,ymax = 0.9,lw = 27,color = "#9AA3B3",ls = "dashed")
ax.set_ylabel("WSB Portfolio", fontsize=fontsize)
tax.set_ylabel("Market Capitalization", fontsize=fontsize,labelpad = 120,rotation = 270)
ax.set_xlabel("Date", fontsize=fontsize)
#######################################
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
tax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
tax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
tax.set_xticks([datetime(2020,12,1),
                datetime(2020,12,15),
                datetime(2021,1,1),
                datetime(2021,1,15),
                datetime(2021,2,1)
                ])
tax.set_xticks([datetime(2020,12,1),
                datetime(2020,12,15),
                datetime(2021,1,1),
                datetime(2021,1,15),
                datetime(2021,2,1)
                ])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
lns = ax_line + tax_line
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc = "upper center",bbox_to_anchor=[0.55, +1.05],ncol = 4,fontsize = fontsize/2,frameon = False)
ax.set_yscale("log")
tax.set_yscale("log")
ax.set_ylim([3*10**6,10**9])
tax.set_ylim([3*10**8,10**11])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.12,right = 0.9)
fig.savefig("fig/fig_1_B.pdf")
################################################################
import powerlaw
with open("data/WSB_first_screenshot.csv","r") as inpuf:
    screenshot = pd.read_csv(inpuf)
y = 120
x = 130
fontsize = 120
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
data = screenshot["value_first_screenshot"]
fit = powerlaw.Fit(data, xmin = 1_00,xmax = 10**8)
powerlaw.plot_pdf(data, ax=ax,
                  linestyle='-', lw = 20,
                  markersize = 80, marker='.', color="#B92113",markerfacecolor='white',markeredgewidth = 12
                  )
print(fit.distribution_compare("lognormal","power_law"))
mu = round(fit.lognormal.parameter1,2)
sigma = round(fit.lognormal.parameter2,2)
fit.lognormal.plot_pdf(data, ax=ax,
                       linestyle='solid', lw = 20,
                       color="#7E8BA0",alpha = 0.5,
                       label = "Fit LogNormal(μ = {mu}, σ = {sigma})".format(mu = mu, sigma = sigma),
                       )
ax.set_ylabel("PDF", fontsize=fontsize)
ax.set_xlabel("Value Screenshot", fontsize=fontsize)
ax.set_aspect('auto')
ax.set_xlim([0.5*100,10**8])
desired_ticks = [10**(-i) for i in range(1, 12)]
ax.set_yticks(desired_ticks)
ax.set_ylim(ymin = 10**(-11),ymax = 10**(-2))
ax.yaxis.get_minor_locator().set_params(numticks = 120, subs=[.2, .4, .6, .8])
ax.tick_params(axis='both', which='major', labelsize=fontsize * 0.5, size=fontsize * 0.3)
ax.tick_params(axis='both', which='minor', labelsize=fontsize * 0.5, size=fontsize * 0.3)
ax.legend(fontsize = fontsize*0.5,
          loc='upper right', ncol = 6,
          frameon = False)
fig.savefig("fig/fig_1_B_inset.pdf")
################################################################
with open("data/GME_all_signals.csv","r") as inpuf:
    gme = pd.read_csv(inpuf)
gme = gme.groupby(by = ["date"]).agg({
    "tweets":"sum",
    "occurrences":"sum",
    "volume":"sum",
    "close":"mean"
}).reset_index()
gme["date"] = pd.to_datetime(gme["date"],format = "%Y-%m-%d")
gme_all_signals = pd.merge(gme,df, on = "date")
print(gme_all_signals["occurrences"].corr(gme_all_signals["portfolio"]))