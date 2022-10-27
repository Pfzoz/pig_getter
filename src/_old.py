from zipfile import ZipFile
import pandas as pd
import os
import json

for path in os.listdir("assets/Health/CNES/raw/"):
    cnesZip = ZipFile("assets/Health/CNES/raw/"+path)
# head

TP_JSON_PATH = "assets/tipounidades.json"
jsonFile = open(TP_JSON_PATH, "r")
jsonObj = json.load(jsonFile)
tpDict = {}
for item in jsonObj["tipos_unidade"]:
    tpDict[item["codigo_tipo_unidade"]] = item["descricao_tipo_unidade"]
jsonFile.close()

MUN_PATH = "assets/municipios.xls"
MUN_FRAME = pd.read_excel(MUN_PATH)
munDict = {}
for i, item in enumerate(MUN_FRAME["codmunisu"]):
    munDict[str(item)[:6]] = MUN_FRAME.at[i, "nome_municipio"]

print(len(munDict))

# body

mainFrame = {
        "municipio" : [],
        "qtd_estabelecimentos": [],
        "ano": [],
        "mes": []
    }

# Fixed Data Types = CO_CNES, CO_UNIDADE, CO_MUNICIPIO_GESTOR, TP_UNIDADE, CO_CEP 

for path in os.listdir("resources/Health/CNES/"):
    if path[-4:] == ".csv":
        year = path.split("tbEstabelecimento")[-1].split(".")[0][:4]
        month = path.split("tbEstabelecimento")[-1].split(".")[0][-2:]
        
        print("FRAME: "+path)
        currentFrame = pd.read_csv("resources/Health/CNES/"+path, sep=';', encoding="latin")
        currentFrame = currentFrame[["CO_MUNICIPIO_GESTOR", "TP_UNIDADE"]]
        for i, cod in enumerate(currentFrame["CO_MUNICIPIO_GESTOR"]):
            currentFrame.at[i, "CO_MUNICIPIO_GESTOR"] = int(str(cod)[:6])
        currentCodes = currentFrame.groupby("CO_MUNICIPIO_GESTOR").size()
        for i, munKey in enumerate(munDict.keys()):
            print("Getting mun:", i)
            mainFrame["ano"].append(year) # 2018
            mainFrame["mes"].append(month) # 03
            for cod in currentCodes.index.values:
                if cod == int(munKey):
                    mainFrame["qtd_estabelecimentos"].append(currentCodes[cod]) # X Amount
            mainFrame["municipio"].append(munDict[munKey]) # Santo Cabo de Agostinho

mainFrame = pd.DataFrame(mainFrame)
mainFrame.sort_values(by=["ano", "mes"], inplace=True, ascending=[False, False])
print(mainFrame)
mainFrame.to_csv("gEstabelecimentos.csv")