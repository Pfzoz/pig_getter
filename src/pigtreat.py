import pandas as pd
import os

## head

municipios = pd.read_excel("assets/municipios.xls")

## body

def treat_cnes(year : str, month : str, csv_path : str = ""):
    cnesFrame = pd.read_csv(csv_path, sep=';', encoding="latin")
    yearsFrame = pd.DataFrame({
        "Ano": [int(year) for i in range(len(cnesFrame.index))],
        "Mes": [month for i in range(len(cnesFrame.index))]
    })
    correct_columns = {
        "CO_ESTADO_GESTOR" : "ESTADO_UNIDADE_DE_SAUDE",
        "CO_DISTRITO_SANITARIO" : "CODIGO_DISTRITO_SANITARIO",
        "CO_MICRO_REGIAO" : "CODIGO_MICRO_REGIAO",
        "CO_MUNICIPIO_GESTOR" : "MUNICIPIO_UNIDADE_DE_SAUDE",
        "TP_UNIDADE" : "CODIGO_TIPO_UNIDADE",
        "CO_UNIDADE" : "CODIGO_UNIDADE_DE_SAUDE",
        "CO_CNES" : "CODIGO_CNES",
        "NU_CNPJ_MANTENEDORA" : "CNPJ_MANTENEDOR",
        "NO_RAZAO_SOCIAL" : "RAZAO_SOCIAL",
        "NO_FANTASIA" : "NOME_FANTASIA",
        "NO_BAIRRO" : "BAIRRO_UNIDADE_DE_SAUDE",
        "CO_CEP" : "CEP_UNIDADE_DE_SAUDE",
        "CO_REGIAO_SAUDE" : "CODIGO_REGIAO_SAUDE",
        "CO_DISTRITO_ADMINISTRATIVO" : "CODIGO_DISTRITO_ADMINISTRATIVO",
        "NU_TELEFONE" : "TELEFONE_UNIDADE_DE_SAUDE",
        "NO_EMAIL" : "EMAIL_UNIDADE_DE_SAUDE",
        "NU_CNPJ" : "CNPJ_UNIDADE_DE_SAUDE",
        "TO_CHAR(DT_ATUALIZACAO,'DD/MM/YYYY')" : "TO_CHAR(DATA_ATUALIZACAO,'DD/MM/YYYY')",
        "NO_URL" : "URL_UNIDADE_DE_SAUDE",
        "NU_LATITUDE" : "LATITUDE_UNIDADE_DE_SAUDE",
        "NU_LONGITUDE" : "LONGITUDE_UNIDADE_DE_SAUDE"
    }
    cnesFrame = cnesFrame[list(correct_columns.keys())]
    cnesFrame.rename(columns=correct_columns, inplace=True)
    cnesFrame = cnesFrame.join(yearsFrame)
    cnesFrame.to_csv(csv_path, sep=';')

def treat_PAM(excel_path : str = '', save_path : str = '') -> None:
    if save_path == '':
        save_path = save_path + excel_path.split(".xlsx")[0] + str("_treated.csv")
    pamFrame = pd.read_excel(excel_path, header=3)
    pamFrame.rename(columns={"Unnamed: 0": "COD", "Unnamed: 1": "NOME", "Unnamed: 2": "ANO"}, inplace=True)
    changer = pamFrame.at[0, "COD"]
    scatterer = 0
    for i, item in enumerate(pamFrame["COD"]):
        if pamFrame.at[i, "COD"] != changer and pd.notna(pamFrame.at[i, "COD"]) != False:
            break
        scatterer += 1
    for i, item in enumerate(pamFrame["COD"]):
        if i == 0 or i % scatterer == 0:
            changer = item
        else:
            pamFrame.at[i, "COD"] = changer
    for i, item in enumerate(pamFrame["NOME"]):
        if i == 0 or i % scatterer == 0:
            changer = item
        else:
            pamFrame.at[i, "NOME"] = changer
    pamFrame.drop(pamFrame.index[-1], inplace=True)
    pamFrame.to_csv(save_path, sep=';')

def treat_pop(excel_path : str = '', save_path : str = '') -> None:
    #PHASE1
    if save_path == '':
        save_path = save_path + excel_path.split(".xlsx")[0] + str("_treated.csv")
    pamFrame = pd.read_excel(excel_path, header=4)
    pamFrame.drop(0, inplace=True)
    mapper = {"Unnamed: 0": "COD", "Unnamed: 1": "NOME", "Unnamed: 2": "ANO"}
    pamFrame.rename(columns=mapper, inplace=True)
    mapper.pop("Unnamed: 2")
    changer = None
    for value in mapper.values():
        for index, item in zip(pamFrame.index, pamFrame[value]):
            if not changer:
                changer = item
            else:
                if pd.notna(pamFrame.at[index, value]) == False:
                    pamFrame.at[index, value] = changer
                else:
                    changer = pamFrame.at[index, value]
    pamFrame.drop(pamFrame.index[-1], inplace=True)
    pamFrame.to_csv(save_path, sep=';')

def treat_pop_dir(dir_path : str):
    for path in os.listdir(dir_path):
        fullPath = dir_path + path
        sex = path.split('_')[1]
        sit = path.split('_')[2]
        print(path)
        if (not "_80" in path) and (not "_81" in path) and (path.endswith("_treated.csv")):
            mainFrame = pd.read_csv(dir_path+path, sep=';', index_col=0)
            secondFrame = pd.read_csv(dir_path+f"POP_{sex}_{sit}_20102000_81_treated.csv", sep=';', index_col=0) # Faixas acima de 80 (2000, 2010)
            thirdFrame = pd.read_csv(dir_path+f"POP_{sex}_{sit}_19911970_80_treated.csv", sep=';', index_col=0) # 80+ (1991, 1980, 1970)
            mainFrame["80 anos ou mais"] = [None for i in range(len(mainFrame.index))]
            mainFrame["80 a 84 anos"] = [None for i in range(len(mainFrame.index))]
            mainFrame["85 a 89 anos"] = [None for i in range(len(mainFrame.index))]
            mainFrame["90 a 94 anos"] = [None for i in range(len(mainFrame.index))]
            mainFrame["95 a 99 anos"] = [None for i in range(len(mainFrame.index))]
            for row in thirdFrame.iterrows():
                changeI = mainFrame.loc[(mainFrame["ANO"] == row[1]["ANO"]) & (mainFrame["NOME"] == row[1]["NOME"])].index[0]
                mainFrame.at[changeI, "80 anos ou mais"] = row[1]["80 anos ou mais"]
            for row in secondFrame.iterrows():
                changeI = mainFrame.loc[(mainFrame["ANO"] == row[1]["ANO"]) & (mainFrame["NOME"] == row[1]["NOME"])].index[0]
                mainFrame.at[changeI, "80 a 84 anos"] = row[1]["80 a 84 anos"]
                mainFrame.at[changeI, "85 a 89 anos"] = row[1]["85 a 89 anos"]
                mainFrame.at[changeI, "90 a 94 anos"] = row[1]["90 a 94 anos"]
                mainFrame.at[changeI, "95 a 99 anos"] = row[1]["95 a 99 anos"]
            mainFrame.to_csv(fullPath, sep=';')

treat_pop_dir("Pop/")