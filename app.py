import pandas as pd

def filtra_chunk(df):
    lista_chunks = []
    for i in df:
        filtrado = i.query('CO_UF == 25')
        lista_chunks.append(filtrado)
    resultado = pd.concat(lista_chunks, ignore_index=True)
    return resultado

def prepara_json(dataframe_a, dataframe_b):
    colunas_em_comum = [
        'NU_ANO_CENSO', 'NO_REGIAO', 'CO_REGIAO', 'NO_UF', 'SG_UF', 'CO_UF',
        'NO_MUNICIPIO', 'CO_MUNICIPIO', 'NO_REGIAO_GEOG_INTERM', 'CO_REGIAO_GEOG_INTERM',
        'NO_REGIAO_GEOG_IMED', 'CO_REGIAO_GEOG_IMED', 'NO_DISTRITO', 'CO_DISTRITO',
        'NO_SUBDISTRITO', 'CO_SUBDISTRITO', 'NO_ENTIDADE', 'CO_ENTIDADE', 'CO_REDE',
        'TP_DEPENDENCIA', 'TP_CATEGORIA_ESCOLA_PRIVADA', 'TP_LOCALIZACAO',
        'TP_LOCALIZACAO_DIFERENCIADA', 'IN_PODER_PUBLICO_PARCERIA', 'TP_PODER_PUBLICO_PARCERIA'
    ]

    tabelao = pd.merge(dataframe_a, dataframe_b, on=colunas_em_comum, how='left')

    colunas_desejadas = [
        'NO_ENTIDADE', 'CO_ENTIDADE', 'NO_UF', 'SG_UF', 'CO_UF',
        'NO_MUNICIPIO', 'CO_MUNICIPIO', 'NO_REGIAO_GEOG_INTERM', 
        'CO_REGIAO_GEOG_INTERM',  'NO_REGIAO_GEOG_IMED', 'CO_REGIAO_GEOG_IMED',      
        'NU_ANO_CENSO', 'NO_REGIAO', 'CO_REGIAO', 'QT_MAT_BAS', 'QT_MAT_INF', 
        'QT_MAT_FUND', 'QT_MAT_MED', 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP'
    ]

    dataframe_filtrado = tabelao[colunas_desejadas].copy()
    dataframe_filtrado.fillna(0.0, inplace=True)
    dataframe_filtrado.to_json("CensoEscolar.json", orient='records', compression='infer')

escolas = pd.read_csv("TabelaEscola.csv", chunksize=500, sep=";", encoding='latin-1')
matriculas = pd.read_csv("TabelaMatricula.csv", chunksize=500, sep=";", encoding='latin-1')

escolas_paraiba = filtra_chunk(escolas)
matriculas_paraiba = filtra_chunk(matriculas)

prepara_json(escolas_paraiba, matriculas_paraiba)