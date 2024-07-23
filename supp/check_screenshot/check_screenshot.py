import os
import random
import json
from PIL import Image
import pandas as pd

pics_folder = "../../main/data_only_zenodo/pictures/"
data_file = "data/user_data.json"

user_data = {}
if os.path.exists(data_file):
    with open(data_file, 'r') as file:
        user_data = json.load(file)

with open("../../main/data/screenshot_ocr.csv","r") as inpuf:
    df_ocr = pd.read_csv(inpuf)
with open("../../main/data/wsb_screenshots_metadata.csv","r") as inpuf:
    wsb_metadata = pd.read_csv(inpuf)
wsb_metadata["dttime"] = pd.to_datetime(wsb_metadata["time"])
wsb_metadata["name_pic"] = wsb_metadata["pic_name"].str.split(".", n=1).str[0]
df = pd.merge(df_ocr,wsb_metadata, left_on = "pic_name",right_on = "name_pic",how = "inner")
df = df[df["bool_gme"]|df["bool_gamestop"]|df["has_gme_text"]]
names_pics = df["name_pic"].tolist()
pics = [f for f in os.listdir(pics_folder) if f != ".DS_Store"]
tpics = [pic for pic in pics if pic.split(".")[0] in names_pics]
random.shuffle(pics)
pics = pics[:1000]

print(len(user_data))
for pic in pics:
    csv_name = pic.split(".")[0] + ".csv"
    image_path = os.path.join(pics_folder, pic)
    img_pl = Image.open(image_path)
    img_pl.show()

    user_input = input("Enter the value of the screenshot (or 'q' to quit): ")

    if user_input.lower() == 'q':
        break

    user_data[pic] = user_input

    print(f"You entered: {user_input}")
    print(f"Total: {len(user_data)}")

    with open(data_file, 'w') as file:
        json.dump(user_data, file)

with open(data_file, 'w') as file:
    json.dump(user_data, file)