# pig_getter

PigData web scraper script.

## Documentação

**src/main.py**

Script principal: possui a classe PigGetter com funções para retirar automáticamente os dados desejados.

**src/pigtreat.py**

Script secundário: possui as funções que tratam os dados minerados pelo *src/main.py*

## Main.py

**PigGetter - Funções**

* >.get_cnes(yearspace, keep_raw : bool, path : str, **kwargs) -> int  

    Pega dados do CNES, em um intervalo de anos específico, com intervalos de mêses específicos.

    * yearspace: intervalo de anos, recebe uma coleção no formato '(ano_inicial, ano_final)', com ano_final exclusivo.  
    *default* -> (2017, ano_atual + 1)
    * keep_raw: mantém o arquivo .zip se verdadeiro.  
    *default* -> False
    * path: caminho do .csv. Default é o caminho atual.  
    *default* -> ""
    * kwargs: recebe argumentos chaves para especificar os intervalos dos mêses de cada ano, no formato '_ano = (mes_inicial, mes_final)', com mes_final exclusivo.  
    *formato* -> _2017 = (2, 9), _2018 = (4, 13)  
    *default* -> _ano = (1, 13) *# pra cada ano não especificado*
