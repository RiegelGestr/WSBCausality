import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Cairo')
matplotlib.style.use("fast")
centrimeters = 1/2.54

#######################################################################################################################
with open("data/final_data_hand.json","r") as inpuf:
    data = json.load(inpuf)
df_human = pd.DataFrame([{"pic_name":k,"value_human":v} for (k,v) in data.items()])
##################################################################################
with open("../../main/data/screenshot_ocr.csv","r") as inpuf:
    df_ocr = pd.read_csv(inpuf)
with open("../../main/data/wsb_screenshots_metadata.csv","r") as inpuf:
    wsb_metadata = pd.read_csv(inpuf)
wsb_metadata["dttime"] = pd.to_datetime(wsb_metadata["time"])
wsb_metadata["name_pic"] = wsb_metadata["pic_name"].str.split(".", n=1).str[0]
df = pd.merge(df_ocr,wsb_metadata, left_on = "pic_name",right_on = "name_pic",how = "inner")
fdf = pd.merge(df_human,df, left_on = "pic_name",right_on = "pic_name_x",how = "inner")
fdf = fdf[["value_human","value_screenshot"]]
fdf = fdf[(fdf["value_human"] > 0)&(fdf["value_screenshot"] > 0)]
print(fdf.shape)
##################################################################################
x = (np.log10(fdf["value_human"])-np.log10(fdf["value_screenshot"]))**2
rmse = np.sqrt(x.mean())
correct_predictions = np.abs((np.log10(fdf["value_human"]) - np.log10(fdf["value_screenshot"]))/np.log10(fdf["value_human"])) < 0.05
correctness = correct_predictions.astype(int)
y_true = correctness
y_pred = np.ones_like(y_true)
accuracy = accuracy_score(y_true, y_pred)
print(rmse)
print(accuracy)
#######################################################################################################################
y = 200
x = 200
fontsize = 200
fig = plt.figure(figsize = (x*centrimeters,y*centrimeters))
ax = fig.add_subplot(1,1,1)
ax.scatter(fdf["value_human"],fdf["value_screenshot"],s = 4_500,color = "#293099",alpha = 0.75)
xs = np.arange(10,10**7,10)
ax.plot(xs,xs,lw = 18,color = "#9AA3B3")
ax.set_xlabel("Human",fontsize = fontsize*0.7)
ax.set_ylabel("OCR",fontsize = fontsize*0.7,rotation = 90,labelpad = 48)
ax.tick_params(axis='both', which='major', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.tick_params(axis='both', which='minor', labelsize = fontsize*0.6,size = fontsize*0.4)
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_ylim([10,10**7])
ax.set_xlim([10,10**7])
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
fig.subplots_adjust(top = 0.9, bottom = 0.15,left = 0.1,right = 0.9)
fig.savefig("fig/check_human.pdf")