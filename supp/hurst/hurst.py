import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54


def hurst(ts):
    ts = list(ts)
    N = len(ts)
    max_k = int(np.floor(N/2))
    R_S_dict = []
    for k in range(10,max_k+1):
        R,S = 0,0
        # split ts into subsets
        subset_list = [ts[i:i+k] for i in range(0,N,k)]
        if np.mod(N,k)>0:
            subset_list.pop()
        # calc mean of every subset
        mean_list=[np.mean(x) for x in subset_list]
        for i in range(len(subset_list)):
            cumsum_list = pd.Series(subset_list[i]-mean_list[i]).cumsum()
            R += max(cumsum_list)-min(cumsum_list)
            S += np.std(subset_list[i])
        R_S_dict.append({"R":R/len(subset_list),"S":S/len(subset_list),"n":k})
    log_R_S = []
    log_n = []
    for i in range(len(R_S_dict)):
        R_S = (R_S_dict[i]["R"]+np.spacing(1)) / (R_S_dict[i]["S"]+np.spacing(1))
        log_R_S.append(np.log(R_S))
        log_n.append(np.log(R_S_dict[i]["n"]))
    #fit hurst
    indices = np.where((log_n > np.log(10)) & (log_n < np.log(200)))
    fit_res,cov = np.polyfit(np.array(log_n)[indices],np.array(log_R_S)[indices],1,cov = True)
    return fit_res, log_R_S, log_n


output_fit = []
for stock in ["GME","NOK","BB","AMC"]:
    ################################################################
    with open("../../main/data/"+stock+"_input_dcca.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    y = 290
    x = 210
    fontsize = 210
    fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
    ################################################################
    fit_res, R_S, n = hurst(df["occurrences"])
    indices = np.where((n > np.log(10)) & (n < np.log(200)))
    R_S = np.array(R_S)
    n = np.array(n)
    fits = fit_res[1]+fit_res[0]*n
    R_S = np.power(np.e,R_S)
    n = np.power(np.e,n)
    fits = np.power(np.e,fits)
    ax1 = fig.add_subplot(3,1,1)
    ax1.scatter(n,R_S,s = 1_500,marker = "s", color = "#44CC00")
    reddit_ax = ax1.plot(n,R_S,lw = 18, color = "#44CC00",label = "Reddit")
    ax1.plot(n,fits,lw = 24,color = "#9AA3B3")
    ax1.set_title(stock,fontsize = fontsize,loc = "left")
    ax1.set_ylabel("R/S",fontsize = fontsize)
    ax1.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax1.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax1.set_yscale("log")
    ax1.set_xscale("log")
    ax1.set_ylim([1,1_000])
    ax1.set_xlim([10,1_000])
    ax1.set_xticklabels([], rotation = 0, ha='right')
    output_fit.append(
        {
            "stock":stock,
            "kind":"Reddit",
            "H":fit_res[0],
        }
    )
    props = dict(boxstyle='round', facecolor='grey', alpha = 0.1)
    ax1.text(0.85, 0.95, "H = {h}".format(h = round(fit_res[0],3)),
            transform = ax1.transAxes,
            fontsize = fontsize/2, verticalalignment='top', bbox = props)
    ################################################################
    fit_res, R_S, n = hurst(df["volume"])
    R_S = np.array(R_S)
    n = np.array(n)
    fits = fit_res[1]+fit_res[0]*n
    R_S = np.power(np.e,R_S)
    n = np.power(np.e,n)
    fits = np.power(np.e,fits)
    ax = fig.add_subplot(3,1,2)
    ax.scatter(n,R_S,s = 1_500,marker = "s", color = "#1E5299")
    trad_ax = ax.plot(n,R_S,lw = 18, color = "#1E5299",label = "Trading Volume")
    ax.plot(n,fits,lw = 24,color = "#9AA3B3")
    ax.set_ylabel("R/S",fontsize = fontsize)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.set_ylim([1,1_000])
    ax.set_xlim([10,1_000])
    ax.set_xticklabels([], rotation = 0, ha='right')
    output_fit.append(
        {
            "stock":stock,
            "kind":"Trading Volume",
            "H":fit_res[0],
        }
    )
    props = dict(boxstyle='round', facecolor='grey', alpha = 0.1)
    ax.text(0.85, 0.95, "H = {h}".format(h = round(fit_res[0],3)),
            transform = ax.transAxes,
            fontsize = fontsize/2, verticalalignment='top', bbox=props)
    ################################################################
    fit_res, R_S, n = hurst(df["price"])
    R_S = np.array(R_S)
    n = np.array(n)
    fits = fit_res[1]+fit_res[0]*n
    R_S = np.power(np.e,R_S)
    n = np.power(np.e,n)
    fits = np.power(np.e,fits)
    ax = fig.add_subplot(3,1,3)
    ax.scatter(n,R_S,s = 1_500,marker = "s", color = "#BF000D")
    price_ax = ax.plot(n,R_S,lw = 18,color = "#BF000D",label = "Price")
    ax.plot(n,fits,lw = 24,color = "#9AA3B3")
    ax.set_ylabel("R/S",fontsize = fontsize)
    ax.set_xlabel("t [hour]",fontsize = fontsize)
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylim([1,1_000])
    ax.set_xlim([10,1_000])
    output_fit.append(
        {
            "stock":stock,
            "kind":"Price",
            "H":fit_res[0],
        }
    )
    props = dict(boxstyle='round', facecolor='grey', alpha = 0.1)
    ax.text(0.85, 0.95, "H = {h}".format(h = round(fit_res[0],3)),
            transform=ax.transAxes,
            fontsize = fontsize/2, verticalalignment='top', bbox=props)
    ################################
    lns = reddit_ax + price_ax + trad_ax
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc = "upper center",bbox_to_anchor=[0.55, +1.1],ncol = 4,fontsize = fontsize/2,frameon = False)
    ################################
    fig.subplots_adjust(left = 0.1,right = 0.9,top = 0.95,bottom = 0.05,hspace = 0.1,wspace = 0.05)
    fig.savefig("fig/"+stock+"_hurst.pdf")
df = pd.DataFrame(output_fit)
print(df.to_latex(index=False))