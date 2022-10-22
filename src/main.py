import shutil
import urllib.request
from contextlib import closing

class PigGetter:
    
    def getCNES():
        with closing(urllib.request.urlopen('ftp://ftp.datasus.gov.br/cnes/BASE_DE_DADOS_CNES_201805.ZIP')) as r:
            with open('BASE_DE_DADOS_CNES_201805.ZIP', 'wb') as f:
                shutil.copyfileobj(r, f)        

        

PigGetter.getCNES()