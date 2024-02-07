import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54
################################################################
with open("data/GME_dcca.csv","r") as inpuf:
    df = pd.read_csv(inpuf)
skip_col = ["window_size","price_price","volume_volume","occurrences_occurrences"]
y = 120
x = 130
fontsize = 120
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
dict_color = {
    "price_volume":"#C493EC",
    "price_occurrences":"#FC9CB5",
    "occurrences_volume":"#FFD480",
}
dict_labels = {
    "price_volume":"Price - Trading V.",
    "price_occurrences":"Price - Reddit",
    "occurrences_volume":"Trading V. - Reddit",
}
columns = list(dict_labels.keys())
columns.append("null_hyp")
for col in columns:
    df = df.dropna()
    df = df[df[col]>0.0]
    xs = df["window_size"]
    ys = df[col]
    if col == "null_hyp":
        ax.fill_between(xs,0,ys, color="#998EA1",label = "95% CI",alpha = 0.3)
        ax.plot(xs,ys,ls = "dashed",color="#998EA1",lw = 27)
    else:
        ax.plot(xs,ys, lw = 30,color = dict_color[col],label = dict_labels[col])
        ax.scatter(xs[:len(xs)-1],ys[:len(xs)-1], s = 5_000,linewidth = 30,edgecolors = dict_color[col],facecolors = dict_color[col])
ax.legend(fontsize = 0.5*fontsize,bbox_to_anchor=[0.55, +1.10],loc='upper center', ncol = 4, frameon=False)
ax.set_ylabel("Detrended Cross-Correlation",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
ax.set_xlabel("Window",fontsize = fontsize*0.7)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_ylim([0,1])
ax.set_xlim([0,100])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.08,right = 0.92)
fig.savefig("fig/fig_1_C_inset.pdf")
################################################################################
################################################################################
################################################################################
################################################################################
y = 120
x = 130
fontsize = 120
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
dict_color = {
    "price_volume_coeff":"#C493EC",
    "price_occurrences_coeff":"#FC9CB5",
    "occurrences_volume_coeff":"#FFD480",
    "price_price_coeff":"#46B998",
    "volume_volume_coeff":"#073D74",
    "occurrences_occurrences_coeff":"#EF6939"
}
dict_labels = {
    "price_volume_coeff":"Price - Trading V.",
    "price_occurrences_coeff":"Price - Reddit",
    "occurrences_volume_coeff":"Trading V. - Reddit",
    "volume_volume_coeff":"Trading V. - Trading V.",
    "price_price_coeff":"Price - Price",
    "occurrences_occurrences_coeff":"Reddit - Reddit"
}
ax = fig.add_subplot(1,1,1)
with open("data/GME_dcca.csv","r") as inpuf:
    df = pd.read_csv(inpuf)
for col in dict_labels.keys():
    df = df.dropna()
    df = df[df[col]>0.0]
    xs = df["window_size"]
    ys = df[col]
    ax.plot(xs,ys, lw = 20,color = dict_color[col],label = dict_labels[col])
    ax.scatter(xs,ys, s = 5_000,color = dict_color[col],marker = "s")
ax.set_xlabel("Window",fontsize = fontsize*0.7)
ax.legend(fontsize = 0.5*fontsize,bbox_to_anchor=[0.55, +1.10],loc='upper center', ncol = 3, frameon=False)
ax.set_ylabel("Detrended Cov./Var.",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_ylim([10**(-6),10**(0)])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.1,left = 0.12,right = 0.9)
fig.savefig("fig/fig_1_C.pdf")