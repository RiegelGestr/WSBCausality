import warnings
import PIL
import pytesseract
import os
from tqdm import tqdm


def true_df(odf):
    df = odf[["left", "top", "width", "text"]]
    df['left+width'] = df['left'] + df['width']
    df = df.sort_values(by=['top'], ascending=True)
    df = df.groupby(['top', 'left+width'], sort=False)['text'].sum().unstack('left+width')
    df = df.reindex(sorted(df.columns), axis=1).dropna(how='all').dropna(axis='columns', how='all')
    df = df.fillna('')
    return df


warnings.filterwarnings("ignore")
pics = [f for f in os.listdir("data_only_zenodo/pictures/") if f != ".DS_Store"]
for id, pic in tqdm(enumerate(pics), total=len(pics)):
    csv_name = pic.split(".")[0] + ".csv"
    image_path = "data_only_zenodo/pictures/" + pic
    img_pl = PIL.Image.open(image_path)
    data = pytesseract.image_to_data(img_pl, output_type='data.frame')
    tdf = true_df(data)
    tdf = tdf.astype(str)
    tdf.to_csv("data_only_zenodo/csvs/" + pic.split(".")[0] + ".csv", sep="\t", index=True)
