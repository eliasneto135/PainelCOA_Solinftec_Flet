from ..cncts.apis import *
from ..cncts.crud_sql import gera_log
import datetime


class Verification:
    def __init__(self):
        pass

    def velocidade(self, a, velocidade, window, parametros):
        alert = False
        if (a['desctalhao'][:3] in ['FSF', 'FSP','FVS', 'SFR']
                and a['descestado'] == 'TRABALHANDO'
                and a['cdoperacao'] not in window.operacoes_apoio):
            if float(velocidade) > float(parametros["parametros"]['param_veloc']):
                if parametros["alertas"]['alrt_veloc'] == True:
                    msg_coa = f"O Pulverizador {a['cdequipamento']} está aplicando acima da velocidade máxima em {a['desctalhao']}"
                    msg_bordo = f'Alerta de Vel. Máx. Acima 18kmh'
                    window.msgAlertas.append(msg_coa)
                    status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                    alert = True
                    font_style = 'alert'
            else:
                font_style = 'normal'
        elif a['desctalhao'][:5] in ['Linha']:
            if float(velocidade) > float(parametros["parametros"]['param_veloc']):
                if parametros["alertas"]['alrt_veloc'] == True:
                    msg_coa = f"O Pulverizador {a['cdequipamento']} está aplicando acima da velocidade máxima em {a['desctalhao']}"
                    msg_bordo = f'Alerta de Vel. Máx. Acima 18kmh'
                    window.msgAlertas.append(msg_coa)
                    status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                    alert = True
        elif a['desctalhao'] in ['ESTRADAO PONTE ESTREITA', 'ESTRADAO VS', 'ESTRADAO SANTA LUCIA']:
            if float(velocidade) > float(40):
                if parametros["alertas"]['alrt_veloc'] == True:
                    msg_coa = f"Frota {a['cdequipamento']} está acima da velocidade em {a['desctalhao']}"
                    msg_bordo = f'Alerta de Vel. Máx.'
                    window.msgAlertas.append(msg_coa)
                    status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                    alert = True
                    font_style = 'alert'
            else:
                font_style = 'normal'
        elif a['desctalhao'] in ['GO-210', 'GO-164']:
            # print("REGRA a['desctalhao'] in ['GO-210', 'GO-164']:")
            if float(velocidade) > float(80):
                if parametros["alertas"]['alrt_veloc'] == True:
                    msg_coa = f"Frota  {a['cdequipamento']} está acima da velocidade em {a['desctalhao']}"
                    msg_bordo = f'Alerta de Vel. Máx.'
                    window.msgAlertas.append(msg_coa)
                    status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                    alert = True
                    font_style = 'alert'
            else:
                font_style = 'normal'
        elif float(velocidade) > float(80):
            if parametros["alertas"]['alrt_veloc'] == True:
                msg_coa = f"Frota  {a['cdequipamento']} está acima da velocidade em {a['descfazenda']}"
                msg_bordo = f'Alerta de Vel. Máx.'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'
        status_alert = alert
        return status_alert

    def rpm(self, a, rpm, window, parametros):
        alert = False
        if int(rpm) > int(parametros["parametros"]['param_rpm']):
            if parametros["alertas"]['alrt_rpm'] == True:
                msg_coa = f"Frota  {a['cdequipamento']} está com o RPM acima do limite em {a['descfazenda']}"
                msg_bordo = f'Alerta de RPM máximo'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert

        return status_alert

    def temperatura_motor(self, a, temp_motor, window, parametros):
        alert = False
        if int(temp_motor) >int(parametros["parametros"]['param_temp']):
            if parametros["alertas"]['alrt_temp'] == True:
                msg_coa = f"Alerta de alta temperatura para frota {a['cdequipamento']} em {a['descfazenda']}"
                msg_bordo = f'Alerta de alta temperatura.'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert
        return status_alert

    def operador(self, a, window, parametros):
        alert = False
        font_style = ''

        if a['cdoperador'] in ['9999', None] and a['cdequipamento'] not in window.equip_sem_tela:
            if parametros["alertas"]['alrt_oper'] == True:
                msg_coa = f"O equipamento {a['cdequipamento']} está operando com o código de operador inválido."
                msg_bordo = f'Alerta de código de operador'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert
        return status_alert

    def implemento(self, a, window, parametros):
        alert = False
        font_style = ''

        if a['cdimplemento'] == None:  ##VERIFICA SE O IMPLEMENTO FOI COLOCADO
            if parametros["alertas"]['alrt_implem'] == True:
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert
        return status_alert

    def rt(self, a, window, parametros):
        alert = False
        font_style = ''

        if str(a['cdordemservico']) not in window.rts_sap:  ##SE RT ESTIVERVER INCORRETA
            if parametros["alertas"]['alrt_rt'] == True:
                msg_coa = f"Frota {a['cdequipamento']} está com RT incorreta"
                msg_bordo = f'Alerta de RT incorreta'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'

        status_alert = alert
        return status_alert

    def operacao(self, a, l, window, parametros):
        alert = False
        font_style = ''

        if (int(l['U_CodOperaca']) != int(a['cdoperacao'])):  ##VERIFICA STATUS DA OPERAÇÃO
            if parametros["alertas"]['alrt_op'] == True:
                msg_coa = "Frota  {a['cdequipamento']} está com operação incorreta"
                msg_bordo = f'Alerta de operação incorreta'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert
        return status_alert

    def talhao(self, a, l, window, parametros):
        alert = False
        font_style = ''
        if int(l['ID_talhao']) != int(a['cdtalhao']):  ##VERIFICA STATUS DO TALHÃO
            if parametros["alertas"]['alrt_talhao'] == True:
                msg_coa = f"Frota  {a['cdequipamento']} está em talhão diferente da RT"
                msg_bordo = f'Talhão diferente da RT'
                window.msgAlertas.append(msg_coa)
                status_log = ApiSolinftec().call_msg(window.get_contador_alert(), a['cdequipamento'], msg_bordo)
                alert = True
                font_style = 'alert'
        else:
            font_style = 'normal'

        status_alert = alert
        return status_alert

    def example(self, a, param, window, parametros):
        alert = False
        font_style = ''

        ##code here

        status_alert = alert
        return status_alert