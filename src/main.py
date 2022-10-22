import urllib.request
import ftplib
import os
from zipfile import ZipFile
from datetime import date

# head

CNESFTP = "ftp://ftp.datasus.gov.br/cnes/"

# body

class PigGetter:
    
    # Health

    def getCNES(yearspace=(2017, date.today().year + 1), keep_raw : bool = False, path : str = "") -> int:
        if not os.path.exists(path):
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
                for month in range(1, 13):
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
                        print(path + fileName)
                        cnesZip = ZipFile(path + fileName)
                        csvName = "tbEstabelecimento"+str(year)+month+".csv"
                        print(csvName)
                        cnesZip.extract(csvName, path)
                        if not keep_raw:
                            os.remove(path + fileName)
                        
            ftpConnection.close()
            
            return 0
            
print(PigGetter.getCNES((2019, 2023), keep_raw=False, path="test/"))