# pighunt

Web scraper script for socio-economy data.

## Documentação

**src/pighunt.py**

Script principal: possui os métodos da classe Pighunt capazes de extrair automáticamente dados por meios online.

**src/pigtreat.py**

Script secundário: possui as funções que tratam os dados minerados pelo *src/pighunt.py*

## Pighunt.py

>Pighunt(sidra_credentials=(mail,password), sidra_driver="path_to_driver")

**Métodos**

*   >.get_cnes(yearspace, keep_raw : bool, path : str, **kwargs) -> int  

    Pega dados do CNES, em um intervalo de anos específico, com intervalos de mêses específicos.

    * yearspace: intervalo de anos, recebe uma coleção no formato '(ano_inicial, ano_final)', com ano_final exclusivo.  
    *default* -> (2017, ano_atual + 1)
    * keep_raw: mantém o arquivo .zip se verdadeiro.  
    *default* -> False
    * path: caminho dos .csv. Default é o caminho atual. Deve ser um diretório.   
    *default* -> ""
    * kwargs: recebe argumentos chaves para especificar os intervalos dos mêses de cada ano, no formato '_ano = (mes_inicial, mes_final)', com mes_final exclusivo.  
    Também pode receber o argumento chave 'toExtract' para especificar outros arquivos a serem extraídos, recebendo um dict no formato '{"nomeArquivoSemExtensão":"latest"}.  
    *formato* -> _2017 = (2, 9), _2018 = (4, 13)  
    *formato* -> toExtract = {"tbNaturezaJuridica":"latest"}  
    *default* -> _ano = (1, 13) *# pra cada ano não especificado*

*   >.sidra_req(table_code, variables, panels : dict, file_name : str,   save_path : str, years, mail : str, password : str, autoget : bool) -> None

    Pega dados das tabelas provindas pelo site Sidra, de maneira automática e generalizada por meio de um webdriver.

    * table_code: código da tabela sidra.
    * variables: variáveis da tabela, recebe um iterável.
    * panels: recebe um dicionário para selecionar uma classificação, no formato '{"nome_classificação":[iterável_com_categorias]}', pode-se adicionar um "all" no iterável para selecionar todas categorias.
    * file_name: nome do arquivo para ser requisitado no site (sem extensão, sempre xlsx)
    * save_path: caminho para se salvar o arquivo. Default é o caminho atual.  
    *default* -> ""
    * mail: e-mail para se requisitar a tabela no sidra. Default é o e-mail inserido na construção do objeto Pighunt.  
    *default* -> self.sidraCredentials[0]
    * password: senha para se requisitar a tabela no sidra. Default é a senha inserida na construção do objeto Pighunt.  
    *default* -> self.sidraCredentials[1]
    * autoget: define se baixa o arquivo ou somente o requisita.  
    *default* -> True

*   >.sidra_thread(**kwargs)

    Age igualmente ao sidra_req, mas cria uma nova thread para se executar.
    * kwargs: argumentos chave do sidra_req.  

*   >.get_pam(save_path : str, treat : bool, yearspace, y_interval : int, aqui_yspace)

    'Macro' para as funções sidra, com intuito de adquirir todo repositório PAM (Produção Agrícola Municipal).

    * save_path: destino dos arquivos a serem salvos, deve ser um diretório.  
    *default* -> "Agro/"
    * treat: define se os arquivos vão ser tratados por pigtreat.treat_PAM ou não.  
    *default* -> True
    * yearspace: recebe uma coleção especificando o intervalo de anos a serem extraídos, no formato '(ano_inicial, ano_final)', com ano_final exclusivo.   
    *default* -> (1974, date.today().year + 6)
    * y_interval: define o período a ser colocado em cada arquivo. Sidra não tende a aguentar mais que 6 anos.   
    *default* -> 6
    * aqui_yspace: recebe uma coleção especificando o intervalo de anos a serem extraídos para aquicultura, no formato '(ano_inicial, ano_final)', com ano_final exclusivo.
