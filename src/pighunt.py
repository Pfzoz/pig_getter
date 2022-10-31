import urllib.request
import ftplib
import os
import shutil
import pigtreat
from zipfile import ZipFile
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import threading
import time

## head

CNESFTP = "ftp://ftp.datasus.gov.br/cnes/"

## body

class Pighunt:
    def __init__(self, sidra_login : tuple, sidra_driver : str = "assets/geckodriver"):
        self.sidraCredentials = sidra_login
        self.sidraDriver = sidra_driver

    # Macros

    def get_pop(self, save_path : str="Pop/", treat : bool = True):
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        name, where = None, None
        for i in range(1, 3):
            threads = []
            for ia in range(1, 3):
                if i == 1: name="HOMENS"
                else: name="MULHERES"
                if ia == 1: where="URBANO"
                else: where="RURAL"
                threads.append(self.sidra_thread(table_code="200", variables=[0], panels={"C2":[i], "C1":[ia], "C58":[1, 8, 14, 20, 26, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]}, file_name=f"POP_{name}_{where}_20101970", save_path=save_path, years=(1970, 1980, 1991, 2000, 2010), naLinha=["Grupo de idade"], naColuna=["Ano"]))
                threads.append(self.sidra_thread(table_code="200", variables=[0], panels={"C2":[i], "C1":[ia], "C58":[43]}, file_name=f"POP_{name}_{where}_19911970_80", save_path=save_path, years=(1970, 1980, 1991), naLinha=["Grupo de idade"], naColuna=["Ano"]))
                threads.append(self.sidra_thread(table_code="200", variables=[0], panels={"C2":[i], "C1":[ia], "C58":[44, 45, 46, 47]}, file_name=f"POP_{name}_{where}_20102000_81", save_path=save_path, years=(2000,2010), naLinha=["Grupo de idade"], naColuna=["Ano"]))
            for t in threads:
                if t:
                    t.join()
            while threading.active_count() > 1:
                pass
        for path in os.listdir(save_path):
            if path.startswith("POP"):
                pigtreat.treat_pop(excel_path=save_path+path)
        pigtreat.treat_pop_dir(save_path)

    def get_pam(self, save_path : str= "Agro/", treat : bool = True, yearspace=(1974, date.today().year + 6), y_interval : int = 6, aqui_yspace=(2013, date.today().year + 1)):
        threads = []
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        for y in range(*yearspace, y_interval):
            threads = []
            year = y
            #Lavouras
            threads.append(self.sidra_thread(table_code="5457", variables=[0], panels={"C782":["all"]}, file_name=f"PAM_LAVOURAS_{year}{year+y_interval}_PLANTIO", save_path=save_path, years=range(year, year+y_interval+1)))
            threads.append(self.sidra_thread(table_code="5457", variables=[2], panels={"C782":["all"]}, file_name=f"PAM_LAVOURAS_{year}{year+y_interval}_COLHEITA", save_path=save_path, years=range(year, year+y_interval+1)))
            threads.append(self.sidra_thread(table_code="5457", variables=[4], panels={"C782":["all"]}, file_name=f"PAM_LAVOURAS_{year}{year+y_interval}_QTD", save_path=save_path, years=range(year, year+y_interval+1)))
            threads.append(self.sidra_thread(table_code="5457", variables=[6], panels={"C782":["all"]}, file_name=f"PAM_LAVOURAS_{year}{year+y_interval}_VALOR", save_path=save_path, years=range(year, year+y_interval+1)))
            #OrigemAnimal
            threads.append(self.sidra_thread(table_code="74", variables=[0], panels={"C80":["all"]}, file_name=f"PAM_ORIGEMANIMAL_{year}{year+y_interval}_PROD", save_path=save_path, years=range(year, year+y_interval+1)))
            threads.append(self.sidra_thread(table_code="74", variables=[1], panels={"C80":["all"]}, file_name=f"PAM_ORIGEMANIMAL_{year}{year+y_interval}_VALOR", save_path=save_path, years=range(year, year+y_interval+1)))
            #Pecuaria
            threads.append(self.sidra_thread(table_code="3939", variables=[0], panels={"C79":["all"]}, file_name=f"PAM_PECUARIA_{year}{year+y_interval}_EFETIVO", save_path=save_path, years=range(year, year+y_interval+1)))
            for t in threads:
                if t:
                    t.join()
            while threading.active_count() > 1:
                pass
        if aqui_yspace:
            for y in range(*aqui_yspace, y_interval):
                threads = []
                year = y
                threads.append(self.sidra_thread(table_code="3940", variables=[0], panels={"C654":["all"]}, file_name=f"PAM_AQUICULTURA_{year}{year+y_interval}_PROD", save_path=save_path, years=range(year, year+y_interval+1)))
                threads.append(self.sidra_thread(table_code="3940", variables=[1], panels={"C654":["all"]}, file_name=f"PAM_AQUICULTURA_{year}{year+y_interval}_VALOR", save_path=save_path, years=range(year, year+y_interval+1)))
                while threading.active_count() > 1:
                    pass
                for t in threads:
                    if t:
                        t.join()
                while threading.active_count() > 1:
                    pass
        if treat:
            for path in os.listdir(save_path):
                if path.startswith("PAM_") and path.endswith("_treated.csv") == False:
                    pigtreat.treat_PAM(save_path + path)


    # Sidra

    def sidra_thread(self, **kwargs):
        thread = threading.Thread(target=self.sidra_req, kwargs=kwargs)
        thread.start()
        return thread

    def sidra_get(self, file_name : str, mail : str = None, password : str = None, download_path : str = str(os.path.expanduser('~'))+"/Downloads/", save_path : str = ""):
        if not mail or not password:
            mail, password = self.sidraCredentials
        # Driver
        driver = webdriver.Firefox()
        driver.get("https://sidra.ibge.gov.br/Posteriori/Gravacoes")
        driver.find_element_by_class_name("areausuario-li").click()
        formControls = driver.find_elements_by_class_name("form-control")
        for formControl in formControls:
            if formControl.get_attribute("name") == "Email":
                formControl.send_keys(mail)
            elif formControl.get_attribute("name") == "Senha":
                formControl.send_keys(password)
                break
        btns = driver.find_elements_by_class_name("btn")
        for btn in btns:
            if btn.get_attribute("value") == "Entrar":
                btn.click()
                break
        time.sleep(1)
        driver.get("https://sidra.ibge.gov.br/Posteriori/Gravacoes")
        time.sleep(2)
        downloaded = False
        while not downloaded:
            driver.refresh()
            time.sleep(2)
            solis = driver.find_elements_by_class_name("item-solicitacao")
            for soli in solis:
                lsLeft = soli.find_element_by_class_name("ls-left")
                if soli.get_attribute("class").split(" ")[-1] == "pendente":
                    break
                if lsLeft.text.split('.')[0] == file_name:
                    a = lsLeft.find_element_by_tag_name("a")
                    reffer = str(a.get_attribute("href"))
                    time.sleep(1)
                    #driver.get(reffer)
                    lsLeft.click()
                    a.click()
                    downloaded = True
                    print("Downloading")
                    break
        downloading = True
        time.sleep(0.5)
        while downloading:
            downloading = False
            for path in os.listdir(download_path):
                if path.endswith(".crdownload") or path.endswith(".part"):
                    downloading = True
        print("Download finished.")
        driver.close()
        shutil.copyfile(download_path+file_name+".xlsx", save_path+file_name+".xlsx")
        os.remove(download_path+file_name+".xlsx")
        
    def sidra_req(self, table_code, variables, panels : dict, file_name : str, save_path : str = '', years=(), mail : str = None, password : str = None, autoget : bool = True, **kwargs) -> None:
        if not mail or not password:
            mail, password = self.sidraCredentials
        # Driver
        driver = webdriver.Firefox()
        driver.get("https://sidra.ibge.gov.br/tabela/"+str(table_code))
        while True:
            time.sleep(0.5)
            if driver.find_elements_by_class_name("loading-logo") and driver.find_element_by_class_name("loading-logo").get_attribute("class").split(' ')[-1] == "carregado":
                time.sleep(1.5)
                break
        print("Resquesting... "+file_name)
        # Layout
        if kwargs.get("naColuna"):
            draggers = kwargs.get("naColuna")
            for item in draggers:
                trs = driver.find_elements_by_class_name("na-coluna")
                if trs:
                    for tr in trs:
                        if item in tr.text:
                            ActionChains(driver).drag_and_drop(tr, driver.find_elements_by_class_name("na-linha")[0]).perform()
                            time.sleep(0.2)
                            break    
        if kwargs.get("naLinha"):
            draggers = kwargs.get("naLinha")
            for item in draggers:
                trs = driver.find_elements_by_class_name("na-linha")
                if trs:
                    for tr in trs:
                        if item in tr.text:
                            ActionChains(driver).drag_and_drop(tr, driver.find_elements_by_class_name("na-coluna")[0]).perform()
                            time.sleep(0.2)
                            break    
        # Variables
        varPanel = driver.find_element_by_id("panel-V")
        for i, e in enumerate(varPanel.find_elements_by_class_name("lv-row")):
            if e.text != '' and i in variables:
                sidraToggle = e.find_element_by_class_name("sidra-toggle")
                if sidraToggle.get_attribute("aria-selected") == "false":
                    sidraToggle.click()
            elif e.text != '':
                sidraToggle = e.find_element_by_class_name("sidra-toggle")
                if sidraToggle.get_attribute("aria-selected") == "true":
                    sidraToggle.click()
        # Classifications
        for key in panels.keys():
            specificPanel = driver.find_element_by_id("panel-"+key)
            rows = specificPanel.find_elements_by_class_name("lv-row")
            if "all" in panels[key]:
                for btn in specificPanel.find_elements_by_class_name("cmd-lista"):
                    if btn.get_attribute("data-cmd") == "marcarTudo":
                        btn.click()
            else:
                for row in rows:
                    if not row.find_elements_by_class_name("item-lista"):
                        continue
                    itemList = row.find_element_by_class_name("item-lista")
                    if row.text != '' and int(itemList.get_attribute("data-indice")) in panels[key]:
                        sidraToggle = row.find_element_by_class_name("sidra-toggle")
                        if sidraToggle.get_attribute("aria-selected") == "false":
                            sidraToggle.click()
                    elif row.text != '':
                        sidraToggle = row.find_element_by_class_name("sidra-toggle")
                        if sidraToggle.get_attribute("aria-selected") == "true":
                            sidraToggle.click()
        # Period
        yearPanel = driver.find_element_by_id("panel-P")
        rows = yearPanel.find_elements_by_class_name("lv-row")
        for row in rows:
            if row.text != '' and int(row.text[:4]) in years:
                sidraToggle = row.find_element_by_class_name("sidra-toggle")
                if sidraToggle.get_attribute("aria-selected") == "false":
                    sidraToggle.click()
            else:
                try:
                    sidraToggle = row.find_element_by_class_name("sidra-toggle")
                    if sidraToggle.get_attribute("aria-selected") == "true":
                        sidraToggle.click()
                except Exception as e:
                    pass
        # Territorial Level
        terrPanel = driver.find_element_by_id("panel-T")
        for i, r in enumerate(terrPanel.find_elements_by_class_name("sidra-check")):
            if r.text[:9] == "Município":
                r.find_element_by_class_name("sidra-toggle").click()
        # Download Request
        driver.find_element_by_id("botao-downloads").click()
        time.sleep(0.5)
        modDownloads = driver.find_element_by_id("modal-downloads")
        modDownloads.find_elements_by_class_name("checkbox-inline")[3].click()
        modDownloads.find_elements_by_class_name("checkbox-inline")[7].click()
        driver.find_element_by_id("posteriori-email").send_keys(mail)
        fControls = modDownloads.find_elements_by_class_name("form-control")
        for f in fControls:
            if f.get_attribute("name") == "nome-arquivo":
                f.send_keys(file_name)
        modDownloads.find_element_by_id("opcao-downloads").click()
        timeouter = 0
        while True:
            time.sleep(0.1)
            timeouter += 1
            if timeouter > 100000:
                break
            if driver.find_elements_by_class_name("sucesso"):
                time.sleep(1.5)
                break
        driver.close()
        print(f"Request {file_name} made.")
        if autoget:
            self.sidra_get(file_name, mail, password, save_path=save_path)
        
    # CNES

    def get_cnes(self, yearspace=(2017, date.today().year + 1), keep_raw : bool = False, path : str = "", **kwargs) -> int:
        
        if path != "" and not os.path.exists(path):
            os.mkdir(path)
        try:        
            newRequest = urllib.request.Request(CNESFTP)
            ftpConnection = ftplib.FTP()
            ftpConnection.connect(newRequest.host)
            ftpConnection.login()
            ftpConnection.cwd("cnes")
        except Exception as connectException:
            print("Failed connection to FTP server:\n"+str(connectException))
            return 1
        else:
            if kwargs.get("toExtract"):
                print(kwargs.get("toExtract").keys())
                for key in kwargs.get("toExtract").keys():
                    print(key)
                    if kwargs.get("toExtract")[key] == "latest":
                        for i in range(date.today().year, 2016, -1):
                            year = i
                            gotten = False
                            for ia in range(12, 0, -1):
                                month = ia
                                if month <= 9:
                                    month = "0"+str(month)
                                print(i, ia)
                                fName = f"BASE_DE_DADOS_CNES_{year}{month}.ZIP"
                                print(fName)
                                try:
                                    f = open(path + fName, "wb")
                                    ftpConnection.retrbinary(f"RETR "+fName, f.write)
                                except ftplib.error_perm:
                                    f.close()
                                    os.remove(path + fName)
                                else:
                                    print("Retrieved CNES:", i, ia)
                                    gotten = True
                                    if f:
                                        f.close()
                                    cnesZip = ZipFile(path + fName)
                                    csvName = str(key)+str(year)+str(month)+".csv"
                                    cnesZip.extract(csvName, path)
                                    if not keep_raw:
                                        os.remove(path + fName)
                                    break
                            if gotten:
                                break
            for year in range(*yearspace):
                monthspace = (1, 13)
                if kwargs.get("_"+str(year)):
                    monthspace = kwargs.get("_"+str(year))
                for month in range(*monthspace):
                    if month <= 9:
                        month = "0"+str(month)
                    fileName = f"BASE_DE_DADOS_CNES_{year}{month}.ZIP"
                    try:
                        f = open(path + fileName, "wb")
                        ftpConnection.retrbinary(f"RETR "+fileName, f.write)
                    except ftplib.error_perm:
                        print("Missed CNES:", year, month)
                        f.close()
                        os.remove(path + fileName)
                    else:
                        print("Retrieved CNES:", year, month)
                        if f:
                            f.close()
                        cnesZip = ZipFile(path + fileName)            
                        csvName = "tbEstabelecimento"+str(year)+str(month)+".csv"
                        cnesZip.extract(csvName, path)
                        pigtreat.treat_cnes(str(year), month, path + csvName)
                        if not keep_raw:
                            os.remove(path + fileName)
                        
            ftpConnection.close()
            return 0

## footer

pigHunt = Pighunt(sidra_login=("pedrozoz.qwerty@gmail.com", "oLOSISTOTAL7!"))

#pigHunt.get_cnes(toExtract={"tbNaturezaJuridica":"latest", "tbTipoUnidade":"latest"})
#pigHunt.get_pam(yearspace=(1981, date.today().year + 6), aqui_yspace=(2020, 2022))
pigHunt.get_pop()
