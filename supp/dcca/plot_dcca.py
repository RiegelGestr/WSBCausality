import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
#
y = 200
x = 300
fontsize = 150
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
dict_color = {
    "price_volume_coeff":"#fee440",
    "price_occurrences_coeff":"#f15bb5",
    "occurrences_volume_coeff":"#00bbf9",
    "price_price_coeff":"#BF000D",
    "volume_volume_coeff":"#1E5299",
    "occurrences_occurrences_coeff":"#44CC00"
}
dict_labels = {
    "price_volume_coeff":"Price - Trading V.",
    "price_occurrences_coeff":"Price - Reddit",
    "occurrences_volume_coeff":"Trading V. - Reddit",
    "volume_volume_coeff":"Trading V. - Trading V.",
    "price_price_coeff":"Price - Price",
    "occurrences_occurrences_coeff":"Reddit - Reddit"
}
for id,stock in enumerate(["BB","AMC","NOK"]):
    ax = fig.add_subplot(1,3,id+1)
    with open("../../main/data/"+stock+"_dcca.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    for col in dict_labels.keys():
        df = df.dropna()
        df = df[df[col]>0.0]
        xs = df["window_size"]
        ys = df[col]
        ax.plot(xs,ys, lw = 18,color = dict_color[col],label = dict_labels[col])
        ax.scatter(xs,ys, s = 3_000,color = dict_color[col])
        ax.set_xlabel("Window",fontsize = fontsize*0.7)
        ax.legend(fontsize = 0.3*fontsize,bbox_to_anchor=[0.55, +1.05],loc='upper center', ncol=3, frameon=False)
        ax.set_ylabel("Detrended Cov./Var.",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.set_title(stock,fontsize = fontsize*0.8,loc = "left")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylim([10**(-8),10**(1)])
    ax.set_xlim([1,100])
    ls2 = ax.get_yticklabels()
    ax.set_yticklabels(['$\\mathdefault{10^{-10}}$',
                        '$\\mathdefault{10^{-8}}$',
                        '$\\mathdefault{10^{-6}}$',
                        '$\\mathdefault{10^{-4}}$',
                        '$\\mathdefault{10^{-2}}$',
                        '$\\mathdefault{1}$',
                        '$\\mathdefault{10^{2}}$',
                        '$\\mathdefault{10^{4}}$'
                        ])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.08,right = 0.92,wspace = 0.4)
fig.savefig("fig/dcovar.pdf")
################################################################################
################################################################################
################################################################################
################################################################################
y = 200
x = 300
fontsize = 150
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
dict_color = {
    "price_volume":"#fee440",
    "price_occurrences":"#f15bb5",
    "occurrences_volume":"#00bbf9",
}
dict_labels = {
    "price_volume":"Price - Trading V.",
    "price_occurrences":"Price - Reddit",
    "occurrences_volume":"Trading V. - Reddit",
}
for id,stock in enumerate(["BB","AMC","NOK"]):
    ax = fig.add_subplot(1,3,id+1)
    with open("../../main/data/"+stock+"_dcca.csv","r") as inpuf:
        df = pd.read_csv(inpuf)
    for col in dict_labels.keys():
        df = df.dropna()
        df = df[df[col]>0.0]
        xs = df["window_size"]
        ys = df[col]#.rolling(10).mean()
        ax.plot(xs,ys, lw = 18,color = dict_color[col],label = dict_labels[col])
        ax.scatter(xs,ys, s = 3_000,color = dict_color[col])
        ax.set_xlabel("Window",fontsize = fontsize*0.7)
        ax.legend(fontsize = 0.3*fontsize,bbox_to_anchor=[0.55, +1.05],loc='upper center', ncol=3, frameon=False)
        ax.set_ylabel("Detrended Cross Correlation",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
    ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
    ax.set_title(stock,fontsize = fontsize*0.8,loc = "left")
    ax.set_ylim([0,1])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.08,right = 0.92,wspace = 0.4)
fig.savefig("fig/dcca.pdf")
