import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.webelement import FirefoxWebElement
#FirefoxWebElement.get_attribute()
import time

municipios = pd.read_excel("assets/municipios.xls")

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

def sidraKiller(table_code, variables, mail : str, panels : dict, file_name : str, years=()):
    # Driver
    driver = webdriver.Firefox()
    driver.get("https://sidra.ibge.gov.br/tabela/"+str(table_code))
    driver.maximize_window()
    time.sleep(10)
    # Layout
    for tr in driver.find_elements_by_class_name("na-coluna"):
        if "Ano" in tr.text:
            ActionChains(driver).drag_and_drop(tr, driver.find_elements_by_class_name("na-linha")[0]).perform()
            break
    # Variables
    varPanel = driver.find_element_by_id("panel-V")
    for i, e in enumerate(varPanel.find_elements_by_class_name("lv-row")):
        if i in variables:
            e.find_element_by_class_name("sidra-toggle").click()
    # Classifications
    for key in panels.keys():
        specificPanel = driver.find_element_by_id("panel-"+key)
        if "all" in panels[key]:
            for btn in specificPanel.find_elements_by_class_name("cmd-lista"):
                if btn.get_attribute("data-cmd") == "marcarTudo":
                    btn.click()
        else:
            pass
    # Period
    yearPanel = driver.find_element_by_id("panel-P")
    correctBox = yearPanel.find_elements_by_class_name("lv-block")[-1]
    for i, e in enumerate(correctBox.find_elements_by_class_name("lv-row")):
        if int(e.find_element_by_class_name("sidra-check").text) in years:
            e.find_element_by_class_name("sidra-toggle").click()
    # Territorial Level
    terrPanel = driver.find_element_by_id("panel-T")
    for i, r in enumerate(terrPanel.find_elements_by_class_name("sidra-check")):
        if r.text[:9] == "Município":
            r.find_element_by_class_name("sidra-toggle").click()
    driver.find_element_by_id("botao-downloads").click()
    time.sleep(1)
    modDownloads = driver.find_element_by_id("modal-downloads")
    modDownloads.find_elements_by_class_name("checkbox-inline")[3].click()
    modDownloads.find_elements_by_class_name("checkbox-inline")[7].click()
    driver.find_element_by_id("posteriori-email").send_keys(mail)
    fControls = modDownloads.find_elements_by_class_name("form-control")
    for f in fControls:
        if f.get_attribute("name") == "nome-arquivo":
            f.send_keys(file_name)
    modDownloads.find_element_by_id("opcao-downloads").click()
    
def treatPAM(csv_path : str = ""):
    pamFrame = pd.read_csv("")



sidraKiller("5457", mail="pedrozoz.sizaan@gmail.com", years=(2020, 2019, 2018, 2017, 2016, 2015),variables=[0, 4], panels={"C782":["all"]}, file_name="PAM_20202015_TN")
