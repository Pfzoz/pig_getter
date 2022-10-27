import urllib.request
import ftplib
import os
import pandas as pd
import pigtreat
from zipfile import ZipFile
from datetime import date

# head

CNESFTP = "ftp://ftp.datasus.gov.br/cnes/"

# body

class PigGetter:
    
    # Health

    def get_cnes(yearspace=(2017, date.today().year + 1), keep_raw : bool = False, path : str = "", **kwargs) -> int:
        
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
                        csvName = "tbEstabelecimento"+str(year)+month+".csv"
                        cnesZip.extract(csvName, path)
                        pigtreat.treat_cnes(str(year), month, path + csvName)
                        if not keep_raw:
                            os.remove(path + fileName)
                        
            ftpConnection.close()
            return 0
        
# print(PigGetter.getCNES((2019, 2023), keep_raw=False, path="test/", _2019=(3, 8), _2022=(9, 10)))
PigGetter.get_cnes(yearspace=(2019, 2020), _2019=(9, 10))