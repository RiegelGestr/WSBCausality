import pandas as pd
from datetime import timedelta


with open("data/screenshot_ocr.csv","r") as inpuf:
    df_ocr = pd.read_csv(inpuf)
with open("data/wsb_screenshots_metadata.csv","r") as inpuf:
    wsb_metadata = pd.read_csv(inpuf)
wsb_metadata["dttime"] = pd.to_datetime(wsb_metadata["time"])
wsb_metadata["name_pic"] = wsb_metadata["pic_name"].str.split(".", n=1).str[0]
df = pd.merge(df_ocr,wsb_metadata, left_on = "pic_name",right_on = "name_pic",how = "inner")
gme_df = df[df["bool_gme"]|df["bool_gamestop"]|df["has_gme_text"]]
gme_df["dttime"] = gme_df["dttime"] + pd.Timedelta(hours = -5)
gme_df = gme_df.sort_values(by = ["dttime"])
print(gme_df["dttime"].min())
print(gme_df["dttime"].max())
print(gme_df.shape)
tmp = []
first_investment = []
for (author,author_data) in gme_df.groupby(by = ["author"]):
    if author_data.shape[0] == 1:
        row = author_data.iloc[0]
        tmp.append({
            "author":author,
            "value_portfolio":row["value_screenshot"],
            "dttime":row["dttime"],
            "pic_name":row["name_pic"]
        })
        first_investment.append({
            "author":author,
            "value_first_screenshot":row["value_screenshot"],
            "pic_name":row["name_pic"]
        })
    else:
        gdf = author_data.copy()
        gdf["sub"] = gdf['value_screenshot'].sub(gdf['value_screenshot'].shift(1))
        gdf['sub'].iloc[0] = gdf['value_screenshot'].iloc[0]
        first_investment.append({
            "author":author,
            "value_first_screenshot":gdf['value_screenshot'].iloc[0],
            "pic_name":gdf['name_pic'].iloc[0],
        })
        for _,row in gdf.iterrows():
            tmp.append({
                "author":author,
                "value_portfolio":row["sub"],
                "dttime":row["dttime"],
                "pic_name":row["name_pic"]
            })
###############
df_invest = pd.DataFrame(first_investment)
##############
df_invest = pd.DataFrame([{
    "author":row["author"],
    "value_first_screenshot":row["value_screenshot"],
    "pic_name":row["name_pic"],
} for _,row in gme_df.iterrows()]
)
df_invest.to_csv("data/WSB_first_screenshot.csv",sep = ",", index = False)
################################################################
gme_portfolio = pd.DataFrame(tmp)
gme_portfolio = gme_portfolio.sort_values(by = ["dttime"])
gme_portfolio['date'] = pd.to_datetime(gme_portfolio['dttime']).dt.date
start_date = gme_portfolio["date"].min()
end_date = gme_portfolio["date"].max()
dates_generated = [start_date + timedelta(days = x) for x in range(0, (end_date-start_date).days)]
portfolio_value = 0
portf = []
for d in dates_generated:
    gmp = gme_portfolio[gme_portfolio['date'] == d]
    portfolio_value += gmp["value_portfolio"].sum()
    portf.append({
        "portfolio":portfolio_value,
        "date":d
    })
gme_portfolio = pd.DataFrame(portf)
gme_portfolio["date"] = pd.to_datetime(gme_portfolio["date"])
gme_portfolio.to_csv("data/WSB_portfolio.csv",sep = ",",index = False)