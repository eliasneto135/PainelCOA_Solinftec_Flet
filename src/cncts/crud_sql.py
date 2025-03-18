import sqlite3 as sql
import time

from pandas import json_normalize
from sqlalchemy import create_engine
from .getenv import *

class CrudSqlite:
    def __init__(self):
        self.database = URL_DB_SQLITE

    def select(self, query):
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                con = sql.connect(self.database)
                con.row_factory = sql.Row
                cur = con.cursor()  # Obtém um cursor usando con.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                con.close()
                return rows
            except sql.Error as e:  # Captura exceções específicas do SQLite
                print(f"Erro ao executar consulta SQL (Tentativa {tentativas + 1}): {e}")
                tentativas += 1
                if tentativas < max_tentativas:
                    time.sleep(intervalo)
                else:
                    print("Número máximo de tentativas excedido. Consulta SQL falhou.")
                    return None  # Retorna None caso todas as tentativas falhem.
            finally:
                if 'con' in locals() and con:  # Verifica se a variavel con existe, e se a conexão ainda está aberta.
                    con.close()


    def insert(self, df, table: str, if_exists: str):
        engine = create_engine(f'sqlite:///{self.database}')
        df.to_sql(f'{table}', con=engine, if_exists=f'{if_exists}')


def gera_log(data_hora, causa_evento, parametro_controle, frota, valor_alerta, desc_alerta_bordo, desc_alerta_coa
             , log_bordo):
    dicio = {}
    dicio['data_hora'] = data_hora
    dicio['tipo_msg'] = 'coa'
    dicio['causa_evento'] = causa_evento
    dicio['parametro_controle'] = parametro_controle
    dicio['frota'] = frota
    dicio['valor_alerta'] = valor_alerta
    dicio['desc_alerta'] = desc_alerta_coa
    log = json_normalize(dicio)
    # CrudSqlite().insert(df=log, table='logs_alertas_natasha', if_exists='append')
    if log_bordo:
        dicio['tipo_msg'] = 'bordo'
        dicio['desc_alerta'] = desc_alerta_bordo
        log = json_normalize(dicio)
        # CrudSqlite().insert(df=log, table='logs_alertas_natasha', if_exists='append')
        # print('Log Gerado | BORDO')