import datetime
import json
from time import sleep

from sqlalchemy import column

from design.create_elements import *
from cncts.crud_sql import CrudSqlite
from queries import Queries
import flet as ft
from design.edit_elements import *

def create_container(gridview,
        window
        ,page):
    response = CrudSqlite().select(Queries().busca_dados_frota_sqlite())
    v = []

    for a in response:
        if a['cdequipamento'] not in ['1003', '1002', '1000', '1004', '1001']:
            v.append(int(a['cdequipamento']))
            rpm = 0
            temp_motor = 0
            estado_motor = 0
            estado_operacao = 0
            UltmaComunicacao = datetime.datetime(*eval(a['datahora']))
            dias_sem_comunicacao = abs((datetime.datetime.today() - UltmaComunicacao)).days
            info = json.loads(a['return_json_eqpm_popup'])

            for i in info['popupMonitoramentoList']:
                if i['fieldName'] == 'RPM do Motor' or (
                        i['fieldName'] == 'VL_PARAMETRO_4' and i['fieldDescription'] == 'RPM do Motor'):
                    rpm = i['fieldValue']
                else:
                    pass
                if i['fieldName'] == 'Temperatura Motor' or (
                        i['fieldName'] == 'VL_PARAMETRO_20' and i['fieldDescription'] == 'Temperatura Motor'):
                    temp_motor = i['fieldValue']
                else:
                    pass
                if i['fieldName'] == 'VL_ED_1' and i['fieldDescription'] == 'Motor Ligado':
                    estado_motor = i['fieldValue']
                else:
                    pass
                if i['fieldName'] == 'DESC_GRUPO_OPERACAO':
                    estado_operacao = i['fieldValue']
            if rpm == None:
                rpm = 0
            if temp_motor == None:
                temp_motor = 0
            if a['vlvelocidade'] == None:
                velocidade = 0
            else:
                velocidade = a['vlvelocidade']

            if window.first_loop:
                container_gbx = create_gbx(
                                    frt=a['cdequipamento'] ,
                                    frota=f"{a['cdequipamento']} - {a['descequipamento']}",
                                    talhao=a['desctalhao'],
                                    veloc=velocidade,
                                    rpm=rpm,
                                    temp=temp_motor,
                                    rt=a['cdordemservico'],
                                    oper=a['cdoperacao'],
                                    implem=a['cdimplemento'],
                                    op=a['cdoperador'],
                                    last_com=UltmaComunicacao,
                                    days_com_off=dias_sem_comunicacao,
                                    other_details={"info_popupMonitoramentoList": info['popupMonitoramentoList'],
                                     "estado_motor": estado_motor,
                                     "estado_operacao": estado_operacao,
                                     "velocidade": velocidade,
                                     "rpm": rpm,
                                     "temp_motor": temp_motor,
                                     "operacao": a['cdoperacao'],
                                     "diassemcomun": dias_sem_comunicacao,
                                     "ultimacom": UltmaComunicacao,
                                     "dados_frota": a
                                     }
                                    )
                gridview.controls.append(container_gbx)
            else:
                for f in gridview.controls:
                    if f.data['frota'] == a['cdequipamento']:
                        for el in f.data['elements']:
                            if isinstance(el, ft.TextField) and el.label == "Velocidade":
                                el.value = velocidade
                            elif isinstance(el, ft.TextField) and el.label == "RPM":
                                el.value = rpm
                            elif isinstance(el, ft.TextField) and el.label == "Temperatura":
                                el.value = temp_motor
                            elif isinstance(el, ft.TextField) and el.label == "Operador":
                                el.value = a['cdoperador']
                            elif isinstance(el, ft.TextField) and el.label == "Talhão":
                                el.value = a['desctalhao']
                            elif isinstance(el, ft.TextField) and el.label == "Rec. Tecnica.":
                                el.value = a['cdordemservico']
                            elif isinstance(el, ft.TextField) and el.label == "Operação":
                                el.value = a['cdoperacao']
                            elif isinstance(el, ft.TextField) and el.label == "Implemento":
                                el.value = a['cdimplemento']
                            elif isinstance(el, ft.ElevatedButton):
                                resprow_bt = el.content
                                resprow_bt.data[1].value = f"{UltmaComunicacao} - {dias_sem_comunicacao} S/C"
                                el.value = a['cdimplemento']
                            f.data['json_data'] = {"info_popupMonitoramentoList": info['popupMonitoramentoList'],
                                     "estado_motor": estado_motor,
                                     "estado_operacao": estado_operacao,
                                     "velocidade": velocidade,
                                     "rpm": rpm,
                                     "temp_motor": temp_motor,
                                     "operacao": a['cdoperacao'],
                                     "diassemcomun": dias_sem_comunicacao,
                                     "ultimacom": UltmaComunicacao,
                                     "dados_frota": a
                                     }
                        operations_analyzer(f, window, page)
    return gridview

def operations_analyzer(container_gbx, window, page):
    frota = container_gbx.data["frota"]
    elements = container_gbx.data["elements"]
    a = container_gbx.data["json_data"]["dados_frota"]
    estado_motor = container_gbx.data["json_data"]["estado_motor"]
    velocidade = container_gbx.data["json_data"]["velocidade"]
    rpm = container_gbx.data["json_data"]["rpm"]
    temp_motor = container_gbx.data["json_data"]["temp_motor"]
    parametros = container_gbx.data["json_param"]
    days_off_com = container_gbx.data["json_data"]["diassemcomun"]
    for el in elements:
        if isinstance(el, ft.TextField) and el.label == "Velocidade":
            tx_veloc = el
        elif isinstance(el, ft.TextField) and el.label == "RPM":
            tx_rpm = el
        elif isinstance(el, ft.TextField) and el.label == "Temperatura":
            tx_temp = el
        elif isinstance(el, ft.TextField) and el.label == "Operador":
            tx_op = el
        elif isinstance(el, ft.TextField) and el.label == "Implemento":
            tx_implem = el
        elif isinstance(el, ft.TextField) and el.label == "Rec. Tecnica.":
            tx_rt = el
        elif isinstance(el, ft.TextField) and el.label == "Operação":
            tx_oper = el
        elif isinstance(el, ft.TextField) and el.label == "Talhão":
            tx_talhao = el
        elif isinstance(el, ft.ElevatedButton):
            if days_off_com > 0:
                el.bgcolor = ft.Colors.RED
                resprow = el.content
                for er in resprow.controls:
                    if isinstance(er, ft.Column):
                        # print(er.controls)
                        for text in er.controls:
                            text.color=ft.Colors.WHITE




    monitoramento = False
    if a['fgmonitoramentoativo'] == 'T':
        font_style = 'normal_bold'
        container_gbx.border = ft.border.all(1.5, ft.Colors.BLACK)
        for e in container_gbx.data['elements']:
            e.disabled = False
            e.label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)

            ##==== AJUSTA PARAMETROS DE LAYOUT DA BORDA DE ACORDO COM O STATUS DE OPERAÇÃO DA MAQUINA ====##
        if int(estado_motor) == 1:
            if a['descestado'] == 'PARADA':
                if float(a['vltemposec']) / 60 > 5:
                    msg_coa = f"Alerta de motor ocioso para frota {a['cdequipamento']}."
                    msg_bordo = "alerta motor ocioso"
                container_gbx.border = ft.border.all(3, ft.Colors.RED)
                for e in container_gbx.data['elements']:
                    if isinstance(e, ft.ElevatedButton):
                        continue
                    else:
                        if page.theme_mode == ft.ThemeMode.DARK:
                            e.border_color = ft.Colors.GREY_50
                        else:
                            e.border_color = ft.Colors.SHADOW
                        e.border_width = 1
                        e.bgcolor = ft.Colors.TRANSPARENT
                        e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)
                # print("Alterou borda para vermelho", a['cdequipamento'])
            elif a['descestado'] == 'DESLOCAMENTO':
                container_gbx.border = ft.border.all(3, ft.Colors.YELLOW)
                for e in container_gbx.data['elements']:
                    if isinstance(e, ft.ElevatedButton):
                        continue
                    else:
                        if page.theme_mode == ft.ThemeMode.DARK:
                            e.border_color = ft.Colors.GREY_50
                        else:
                            e.border_color = ft.Colors.SHADOW
                        e.border_width = 1
                        e.bgcolor = ft.Colors.TRANSPARENT
                        e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)
            elif a['descestado'] == 'TRABALHANDO':
                container_gbx.border = ft.border.all(3, ft.Colors.GREEN)
                for e in container_gbx.data['elements']:
                    if isinstance(e, ft.ElevatedButton):
                        continue
                    else:
                        if page.theme_mode == ft.ThemeMode.DARK:
                            e.border_color = ft.Colors.GREY_50
                        else:
                            e.border_color = ft.Colors.SHADOW
                        e.border_width = 1
                        e.bgcolor = ft.Colors.TRANSPARENT
                        e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)
            else:
                container_gbx.border = ft.border.all(3, ft.Colors.BLUE)
                for e in container_gbx.data['elements']:
                    if isinstance(e, ft.ElevatedButton):
                        continue
                    else:
                        if page.theme_mode == ft.ThemeMode.DARK:
                            e.border_color = ft.Colors.GREY_50
                        else:
                            e.border_color = ft.Colors.SHADOW
                        e.border_width = 1
                        e.bgcolor = ft.Colors.TRANSPARENT
                        e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

            ##===AJUSTA VARIAVEL DE ALERTA PARA VALOR PADRÃO "FALSE"===##
            alert = False

            # #====PARAMETROS DE ALERTA E LAYOUT DE ACORDO COM A VELOCIDADE DA MAQUINA====##
            status_alert = Verification().velocidade(a, velocidade, window, parametros)
            if status_alert == True:
                alert = True
                tx_veloc.border_color = ft.Colors.RED
                tx_veloc.border_width = 3
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_veloc.bgcolor = ft.Colors.TRANSPARENT
                    tx_veloc.text_style =ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                else:
                    tx_veloc.bgcolor = ft.Colors.RED_50
                    tx_veloc.text_style =ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
            else:
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_veloc.border_color = ft.Colors.GREY
                else:
                    tx_veloc.border_color = ft.Colors.BLACK

                tx_veloc.border_width = 1
                tx_veloc.bgcolor = ft.Colors.TRANSPARENT
                tx_veloc.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

            ##====PARAMETROS DE ALERTA E LAYOUT DE ACORDO COM A RPM DA MAQUINA====##
            status_alert = Verification().rpm(a, rpm, window, parametros)
            if status_alert == True:
                alert = True
                tx_rpm.border_color = ft.Colors.RED
                tx_rpm.border_width = 3
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_rpm.bgcolor = ft.Colors.TRANSPARENT
                    tx_rpm.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                else:
                    tx_rpm.bgcolor = ft.Colors.RED_50
                    tx_rpm.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
            else:
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_rpm.border_color = ft.Colors.GREY
                else:
                    tx_rpm.border_color = ft.Colors.BLACK

                tx_rpm.border_width = 1
                tx_rpm.bgcolor = ft.Colors.TRANSPARENT
                tx_rpm.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

            ##====PARAMETROS DE ALERTA E LAYOUT DE ACORDO COM A TEMPERATURA DA MAQUINA====##
            status_alert = Verification().temperatura_motor(a, temp_motor, window, parametros)
            if status_alert:
                alert = True
                tx_temp.border_color = ft.Colors.RED
                tx_temp.border_width = 3
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_temp.bgcolor = ft.Colors.TRANSPARENT
                    tx_temp.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                else:
                    tx_temp.bgcolor = ft.Colors.RED_50
                    tx_temp.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
            else:
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_temp.border_color = ft.Colors.GREY
                else:
                    tx_temp.border_color = ft.Colors.BLACK

                tx_temp.border_width = 1
                tx_temp.bgcolor = ft.Colors.TRANSPARENT
                tx_temp.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

            ##====PARAMETROS DE ALERTA E LAYOUT DE ACORDO COM PREENCHIMENTO DA MATRICULA DO OPERADOR NO BORDO DA MAQUINA====##
            status_alert = Verification().operador(a, window, parametros)
            if status_alert == True:
                alert = True
                tx_op.border_color = ft.Colors.RED
                tx_op.border_width = 3
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_op.bgcolor = ft.Colors.TRANSPARENT
                    tx_op.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                else:
                    tx_op.bgcolor = ft.Colors.RED_50
                    tx_op.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
            else:
                if page.theme_mode == ft.ThemeMode.DARK:
                    tx_op.border_color = ft.Colors.GREY
                else:
                    tx_op.border_color = ft.Colors.BLACK

                tx_op.border_width = 1
                tx_op.bgcolor = ft.Colors.TRANSPARENT
                tx_op.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

            ##====PARAMETROS DE ALERTA E LAYOUT PARA RT, TALHÃO E OPERACAO DA MAQUINA====##
            if a['descestado'] == 'TRABALHANDO':  ##SEGUE APENAS SE A OPERAÇÃO FOR PRODUTIVA

                ##VERIFICA SE O IMPLEMENTO FOI COLOCADO

                if a['cdequipamento'] not in window.veiculos_apoio:  ##SEGUE APENAS SE O EQUIPAMENTO NÃO CONSTAR NA LISTA DE APOIO
                    if a['cdoperacao'] not in window.operacoes_apoio:  ##SEGUE APENAS SE A OPERAÇÃO PRODUTIVA DO MESMO NÃO CONSTAR NAS OPERAÇÕES DE APOIO
                        status_alert = Verification().implemento(a, window, parametros)
                        if status_alert == True:
                            alert = True
                            tx_implem.border_color = ft.Colors.RED
                            tx_implem.border_width = 3
                            if page.theme_mode == ft.ThemeMode.DARK:
                                tx_implem.bgcolor = ft.Colors.TRANSPARENT
                                tx_implem.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                            else:
                                tx_implem.bgcolor = ft.Colors.RED_50
                                tx_implem.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
                        else:
                            if page.theme_mode == ft.ThemeMode.DARK:
                                tx_implem.border_color = ft.Colors.GREY
                            else:
                                tx_implem.border_color = ft.Colors.BLACK

                            tx_implem.border_width = 1
                            tx_implem.bgcolor = ft.Colors.TRANSPARENT
                            tx_implem.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)
                        ##=====PARAMETRO DE ALERTA E LAYOUT PARA RT

                        status_alert = Verification().rt(a, window, parametros)
                        if status_alert == True:
                            alert = True
                            tx_rt.border_color = ft.Colors.RED
                            tx_rt.border_width = 3
                            if page.theme_mode == ft.ThemeMode.DARK:
                                tx_rt.bgcolor = ft.Colors.TRANSPARENT
                                tx_rt.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.RED)
                            else:
                                tx_rt.bgcolor = ft.Colors.RED_50
                                tx_rt.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
                        else:  ##SE RT ESTIVER CORRETA, O LAYOUT É AJUSTADO E OS PARAMETROS DE OPERAÇÃO E TALHÃO SÃO VERIFICADOS
                            if page.theme_mode == ft.ThemeMode.DARK:
                                tx_rt.border_color = ft.Colors.GREY
                            else:
                                tx_rt.border_color = ft.Colors.BLACK

                            tx_rt.border_width = 1
                            tx_rt.bgcolor = ft.Colors.TRANSPARENT
                            tx_rt.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

                            for l in window.list_json:  ## INICIA LOOP PARA ENCONTRAR O JSON DA RT DA MAQUINA NO SAP
                                if str(l['DocEntry']) == str(a['cdordemservico']):  ## CLAUSULA PARA IDENTIFICAR O JSON DA RT
                                    ##VERIFICA STATUS DA OPERAÇÃO
                                    status_alert = Verification().operacao(a, l, window, parametros)
                                    if status_alert == True:
                                        alert = True
                                        tx_oper.border_color = ft.Colors.RED
                                        tx_oper.border_width = 3
                                        if page.theme_mode == ft.ThemeMode.DARK:
                                            tx_oper.bgcolor = ft.Colors.TRANSPARENT
                                            tx_oper.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12,
                                                                            color=ft.Colors.RED)
                                        else:
                                            tx_oper.bgcolor = ft.Colors.RED_50
                                            tx_oper.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
                                    else:
                                        if page.theme_mode == ft.ThemeMode.DARK:
                                            tx_oper.border_color = ft.Colors.GREY
                                        else:
                                            tx_oper.border_color = ft.Colors.BLACK

                                        tx_oper.border_width = 1
                                        tx_oper.bgcolor = ft.Colors.TRANSPARENT

                                    ##VERIFICA STATUS DO TALHÃO
                                    status_alert = Verification().talhao(a, l, window, parametros)
                                    if status_alert == True:
                                        alert = True
                                        tx_talhao.border_color = ft.Colors.RED
                                        tx_talhao.border_width = 3
                                        if page.theme_mode == ft.ThemeMode.DARK:
                                            tx_talhao.bgcolor = ft.Colors.TRANSPARENT
                                            tx_talhao.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12,
                                                                            color=ft.Colors.RED)
                                        else:
                                            tx_talhao.bgcolor = ft.Colors.RED_50
                                            tx_talhao.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=12)
                                    else:
                                        if page.theme_mode == ft.ThemeMode.DARK:
                                            tx_talhao.border_color = ft.Colors.GREY
                                        else:
                                            tx_talhao.border_color = ft.Colors.BLACK

                                        tx_talhao.border_width = 1
                                        tx_talhao.bgcolor = ft.Colors.TRANSPARENT
                                    break  ## INTERROMPE O LOOP DE PESQUISA DE RT QUANDO A MESMA É ENCONTRADA
        else:
            container_gbx.border = ft.border.all(1.5, ft.Colors.GREY)
            for e in container_gbx.data['elements']:
                if isinstance(e, ft.ElevatedButton):
                    continue
                else:
                    if page.theme_mode == ft.ThemeMode.DARK:
                        e.border_color = ft.Colors.GREY_50
                    else:
                        e.border_color = ft.Colors.SHADOW
                    e.border_width = 1
                    e.bgcolor = ft.Colors.TRANSPARENT
                    e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)
    else:
        container_gbx.border = ft.border.all(1.5, ft.Colors.GREY)
        for e in container_gbx.data['elements']:
            e.disabled = True
            if isinstance(e, ft.ElevatedButton):
                continue
            else:
                if page.theme_mode == ft.ThemeMode.DARK:
                    e.border_color = ft.Colors.GREY_50
                else:
                    e.border_color = ft.Colors.SHADOW
                e.border_width = 1
                e.bgcolor = ft.Colors.TRANSPARENT
                e.text_style = ft.TextStyle(weight=ft.FontWeight.NORMAL, size=12)

