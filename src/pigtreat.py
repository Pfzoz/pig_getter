import pandas as pd

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
    print(cnesFrame)
    cnesFrame.to_csv(csv_path)

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
    pamFrame.to_csv(save_path)

