import urllib.request
import ftplib
import os
from datetime import date

# head

CNESFTP = "ftp://ftp.datasus.gov.br/cnes/"

# body

class PigGetter:
    
    # Health

    def getCNES(yearspace=(2017, date.today().year + 1), keep=False, path="") -> int:
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
                for month in range(1, 12):
                    if month <= 9:
                        month = "0"+str(month)
                    fileName = f"BASE_DE_DADOS_CNES_{year}{month}.ZIP"
                    try:
                        f = open(path + fileName, "wb")
                        ftpConnection.retrbinary(f"RETR "+fileName, f.write)
                    except ftplib.error_perm:
                        print("Missed CNES:", year, month)
                    else:
                        print("Retrieved CNES:", year, month)
                    finally:
                        f.close()
                        if not keep:
                            os.remove(fileName)
            ftpConnection.close()
            return 0
            
print(PigGetter.getCNES((2017, 2018), keep=True, path="assets/Health/CNES/raw/"))