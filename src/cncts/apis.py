import time
import requests
import json
from pandas import json_normalize
from datetime import datetime, timedelta
from src.cncts.getenv import *


class ApiSolinftec:
    def __init__(self):
        pass

    def solinftec_get_token_legado(self):
        url_auth = URL_AUTH_SOLINFTEC
        data = {'cliente': f'{USER_API_SOLINFTEC}', 'password': f'{PW_API_SOLINFTEC}'}
        headers = {'Content-type': 'application/json'}
        try:
            resposta = requests.post(url_auth, json=data, headers=headers)
            token = resposta.json()['token']
        except:
            token = None
        # print('resptoken', resposta,  resposta.json())
        return token

    def call_msg(self, contador, frota, msg):
        # print('Chamada de CAll MSG')
        cod_equip = frota
        url = URL_COMANDO_ONLINE_SOLINFTEC
        payload = json.dumps({"cdEquipamentos": [f"{cod_equip}"],
                              "cdTipoComando": 1,
                              "valoresDosParametros": {"1": f'{msg}'},
                              "valoresDosParametrosList": {}
                              })
        headers = {
            'authority': f'{URL_AUTHORITY_SOLINFTEC}',
            'method': 'POST',
            'path': '/slf10/comandoOnline',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '693',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': f'{ORIN_REF1}',
            'Referer': f'{ORIN_REF1}/',
            'scheme': 'https',
            'X-Auth-Token': f'{self.solinftec_get_token()}'
        }

        for al in contador:
            log_bordo = False
            # print('Inicio da Iteração LOG BORDO', al['eqpm'] == cod_equip, al['eqpm'], cod_equip)
            if al['eqpm'] == cod_equip:
                if al['count'] == 0:
                    # response = requests.request("POST", url, headers=headers, data=payload)
                    # print('Response:', (response.status_code))
                    # if response.status_code == 200:
                    #     log_bordo = True
                    # print(response, response.json())
                    al['count'] += 1
                elif al['count'] < 2:
                    al['count'] += 1
                elif al['count'] == 2:
                    al['count'] = 0
            else:
                continue
            return log_bordo

    def info_equipamento(self, vehicle):
        url = f"{URL_INFO_EQPM}={vehicle}"
        ca = "{"
        cf = "}"
        payload = f'''equipamentoId={vehicle}'''
        headers = {
            'authority': f'{URL_AUTHORITY_SOLINFTEC}',
            'method': 'GET',
            'path': f'/slf10/campoTipoEquipamento/equipamento/popup?equipamentoId={vehicle}',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '693',
            'Content-Type': 'application/json',
            'Origin': f'{ORIN_REF_2}',
            'Referer': f'{ORIN_REF_2}/',
            'scheme': 'https',
            'X-Auth-Token': f'{self.solinftec_get_token()}'
        }
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                response = requests.get(url, headers=headers, data=payload)
                response.raise_for_status()  # Garante que o status code seja 200.
                response = response.json()
                # print("Dados da api info equipamento obtidos com sucesso")
                return response  # Retorna o token se obtido com sucesso
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Erro ao obter dados da API do Site da Solinftec (Info Equipamentos) {tentativas + 1}): {e}")
                tentativas += 1
                time.sleep(intervalo)  # Aguarda antes da próxima tentativa

        print("Número máximo de tentativas excedido. Falha ao obter dados da API do Site da Solinftec (Info Equipamentos).")
        return None  # Retorna None se todas as tentativas falharem

    def sync_operaces_slft_legado(self, token, data_pesquisa, data_fim, page):
        url_busca = f'{URL_INT_SOLINFTEC}/v2/pull/paged'
        headers2 = {'X-Auth-Token': token, 'Content-type': 'application/json'}
        body = {"id": 22, "page": page,
                "parameters": {"dataini": data_pesquisa, "datafim": data_fim, "unidade": "", "equipamento": "",
                               "operacao": "", "operador": "", "talhao": "", "ordemservico": ""}}
        operacoes = requests.post(url_busca, json=body, headers=headers2)
        return operacoes

    def solinftec_get_token(self):
        url_auth = f'{NEW_URL_AUTH_SOLINFTEC}'
        data = {'cliente': f'{USER_API_SOLINFTEC}', 'password': f'{PW_API_SOLINFTEC}'}
        headers = {'Content-type': 'application/json'}
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                resposta = requests.post(url_auth, json=data, headers=headers)
                resposta.raise_for_status()  # Garante que o status code seja 200.
                token = resposta.json()['token']
                print("Token obtido com sucesso!!!")
                return token  # Retorna o token se obtido com sucesso
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Erro ao obter o token (tentativa {tentativas + 1}): {e}")
                tentativas += 1
                time.sleep(intervalo)  # Aguarda antes da próxima tentativa

        print("Número máximo de tentativas excedido. Falha ao obter o token.")
        return None  # Retorna None se todas as tentativas falharem


    def sync_operaces_slft(self, token, data_ini, data_fim, page, dt_movimentacao):
        url_busca = f'{NEW_URL_INT_SOLINFTEC}/pull/'
        headers2 = {'X-Auth-Token': token, 'Content-type': 'application/json'}
        body = {"identifier": "22",
                "filters": {"page": f'{page}', "dtmovimentacao": data_ini[:10], "dataini": data_ini, "datafim": data_fim,
                            "unidade": "", "equipamento": "", "operacao": "", "operador": "", "talhao": "",
                            "ordemservico": ""}}
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                operacoes = requests.post(url_busca, json=body, headers=headers2)
                operacoes.raise_for_status()  # Garante que o status code seja 200.
                totalpages = operacoes.json()['total_pages']
                return operacoes, totalpages  # Retorna o token se obtido com sucesso
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Erro ao se comunicar com API 22 da Solinftec (tentativa {tentativas + 1}): {e}")
                tentativas += 1
                time.sleep(intervalo)  # Aguarda antes da próxima tentativa

        print("Número máximo de tentativas excedido. Falha ao obter dados da API 22 da Solinftec")
        return None, None  # Retorna None se todas as tentativas falharem

    def get_api_22(self, dias):
        token = self.solinftec_get_token()
        data_atual = datetime.today() - timedelta(days=int(dias))
        data_input = datetime.today().strftime('%d/%m/20%y %H:%M:%S')
        tab = []
        while data_atual <= datetime.today():
            c = 0
            qtd = 0
            page = 1
            while qtd == 1000 or c == 0:
                data_ini = data_atual.strftime('%d/%m/20%y 00:00:00')
                data_fim = data_atual.strftime('%d/%m/20%y 23:59:59')
                operacoes, totalpages = self.sync_operaces_slft(token=token, data_ini=data_ini, data_fim=data_fim, page=page,
                                                           dt_movimentacao=data_atual.strftime('%d/%m/20%y'))
                tabela = operacoes.json()['data']
                page += 1
                qtd = len(tabela)
                c += 1
                for t in tabela:
                    tab.append(t)
            data_atual = data_atual + timedelta(days=1)
        return tab


    def conecta_solinftec(self):
        url = f'https://{URL_AUTHORITY_SOLINFTEC}/slf10/operacao'
        metod = 'GET'
        token = self.solinftec_get_token()
        url = f'{url}'
        ca = "{"
        cf = "}"
        payload = f'''Teste:Teste'''
        headers = {
            'authority': f'{URL_AUTHORITY_SOLINFTEC}',
            'method': f'{metod}',
            'path': f'/slf10/monitoramento/equipamento',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '693',
            'Locale': '1',
            'Content-Type': 'application/json',
            'Origin': f'{ORIN_REF1}',
            'Referer': f'{ORIN_REF1}/',
            'scheme': 'https',
            'X-Auth-Token': f'{token}'
        }
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                response = requests.get(url, headers=headers, data=payload)
                response.raise_for_status()  # Garante que o status code seja 200.
                response = response.json()
                return response  # Retorna o token se obtido com sucesso
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Erro ao se comunicar com API do Site da Solinftec (tentativa {tentativas + 1}): {e}")
                tentativas += 1
                time.sleep(intervalo)  # Aguarda antes da próxima tentativa

        print("Número máximo de tentativas excedido. Falha ao obter dados do site da Solinftec")
        return None  # Retorna None se todas as tentativas falharem


class Api_Liberali:
    def __init__(self):
        ...
    def cnct_api_liberali(self, requisicao, api):
        address = URL_API_LIBERALI
        url = f"{address}{api}"
        # print(url)
        headers = {
            'Authorization': f'{AUTH_API_LIBERALI}',
            'Content-Type': 'application/json'
        }
        # print(headers)
        tentativas = 0
        max_tentativas = 10  # Número máximo de tentativas
        intervalo = 3  # Intervalo em segundos entre as tentativas

        while tentativas < max_tentativas:
            try:
                response = requests.post(url, headers=headers, data=requisicao)
                response.raise_for_status()  # Garante que o status code seja 200.
                retorno = response.json()
                # print(retorno)
                return retorno, response  # Retorna o token se obtido com sucesso
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Erro ao se comunicar com API da Liberali (tentativa {tentativas + 1}): {e}")
                tentativas += 1
                time.sleep(intervalo)  # Aguarda antes da próxima tentativa

        print("Número máximo de tentativas excedido. Falha ao obter dados da Liberali.")
        return None, None  # Retorna None se todas as tentativas falharem

    def busca_sap_api_query(self, q):
        query = json.dumps(q)
        list_json, response = self.cnct_api_liberali(query, "query")
        return list_json, response
