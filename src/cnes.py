from zipfile import ZipFile
import pandas as pd
import os

for path in os.listdir("assets/Health/CNES/raw/"):
    cnesZip = ZipFile("assets/Health/CNES/raw/"+path)
    csvName = "tbEstabelecimento"+path.split(".")[0].split("_")[-1]+".csv"
    print(csvName)
    cnesZip.extract(csvName, "assets/Health/CNES/")
    cnesFrame = pd.read_csv("assets/Health/CNES/"+csvName, encoding="latin", sep=';', on_bad_lines="skip")
    print(cnesFrame)