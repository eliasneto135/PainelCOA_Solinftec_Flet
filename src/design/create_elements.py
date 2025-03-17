import json
import flet as ft
import requests
from src.cncts.getenv import URL_PROJECT_FIREBASE


def create_row_info(frt, frota, talhao, veloc, rpm, temp, rt, oper, implem, op,last_com,days_com_off,other_details):

    params = {
        'orderBy': '"frota"',  # Precisa estar entre aspas duplas no Firebase
        'equalTo': f'"{frt}"'  # Também precisa de aspas duplas
    }
    param_frota = requests.get(f'{URL_PROJECT_FIREBASE}/parametros.json', params=params)
    if param_frota.json() == {}:
        data = {'frota': frt,
                'alrt_frota': True,
                'alrt_talhao': True,
                'alrt_veloc': True,
                'alrt_rpm': True,
                'alrt_temp': True,
                'alrt_rt': True,
                'alrt_oper': True,
                'alrt_implem': True,
                'alrt_op': True,
                'param_veloc': 3,
                'param_rpm': 2100,
                'param_temp': 103
        }
        requests.post(f'{URL_PROJECT_FIREBASE}/parametros.json', data=json.dumps(data))
    else:
        param = param_frota.json()
        for id, dados in param.items():
            json_param_frota = {
                "frota": dados['frota'],
                "id_firebase": id,
                "alertas": {
                    'alrt_frota': dados['alrt_frota'],
                    'alrt_talhao': dados['alrt_talhao'],
                    'alrt_veloc': dados['alrt_veloc'],
                    'alrt_rpm': dados['alrt_rpm'],
                    'alrt_temp': dados['alrt_temp'],
                    'alrt_rt': dados['alrt_rt'],
                    'alrt_oper': dados['alrt_oper'],
                    'alrt_implem': dados['alrt_implem'],
                    'alrt_op': dados['alrt_op']
                },
                "parametros": {
                    'param_veloc':  dados['param_veloc'],
                    'param_rpm':  dados['param_rpm'],
                    'param_temp':  dados['param_temp']
                }
            }

    
    icone = ft.Icon(ft.icons.SETTINGS, col=1)
    nome_frota = ft.Text(f"{frota}", size=11)
    dias_sem_com = ft.Text(f"{last_com} - {days_com_off} S/C", size=9)
    cbx_frota = ft.ElevatedButton(
        content=ft.ResponsiveRow(
            data=[nome_frota, dias_sem_com],
            controls=[
            icone,
            ft.Column(controls=[
                nome_frota,
                dias_sem_com
                ]
                ,col=11
                ,spacing=0
                ,horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ])
        ,style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.BOLD
            )
            ,shape=ft.RoundedRectangleBorder(radius=2)
        )
    )
    tx_talhao = ft.TextField(label="Talhão", read_only=True, value=f"{talhao}", col=6, text_size=12, height=40, data=frt)
    tx_veloc = ft.TextField(label="Velocidade", read_only=True, value=f"{veloc}", col=6, text_size=12, height=40, data=frt)

    rw_talhao_vel = ft.ResponsiveRow([
        tx_talhao,
        tx_veloc
    ])

    tx_rpm = ft.TextField(label="RPM", read_only=True, value=f"{rpm}", col=6, text_size=12, height=40, data=frt)
    tx_temp = ft.TextField(label="Temperatura", read_only=True, value=f"{temp}", col=6, text_size=12, height=40, data=frt)

    rw_rpm_temp = ft.ResponsiveRow([
        tx_rpm,
        tx_temp
    ])

    tx_rt = ft.TextField(label="Rec. Tecnica.", read_only=True, value=f"{rt}", col=6, text_size=12, height=40, data=frt)
    tx_oper = ft.TextField(label="Operação", read_only=True, value=f"{oper}", col=6, text_size=12, height=40, data=frt)

    rw_rt_oper = ft.ResponsiveRow([
        tx_rt,
        tx_oper
    ])

    tx_implem = ft.TextField(label="Implemento", read_only=True, value=f"{implem}", col=6, text_size=12, height=40, data=frt)
    tx_op = ft.TextField(label="Operador", read_only=True, value=f"{op}", col=6, text_size=12, height=40, data=frt)

    rw_implem_op = ft.ResponsiveRow([
        tx_implem,
        tx_op
    ])

    header_cbx = ft.ResponsiveRow([
        cbx_frota
    ])

    group_box = ft.Container(
            content=ft.Column([
            header_cbx,
            rw_talhao_vel,
            rw_rpm_temp,
            rw_rt_oper,
            rw_implem_op
        ]),
        border=ft.border.all(1, ft.colors.GREY),  # Adiciona uma borda cinza
        border_radius=ft.border_radius.all(5),  # Arredonda os cantos
        padding=10,  # Adiciona um espaçamento interno
        data={
            "frota": frt,
            "elements": [
                tx_talhao,
                tx_veloc,
                tx_rpm,
                tx_temp,
                tx_rt,
                tx_oper,
                tx_implem,
                tx_op,
                cbx_frota
            ],
            "json_data": other_details,
            "json_param": json_param_frota

        }
    )
    return group_box

def create_gbx(frt, frota, talhao, veloc, rpm, temp, rt, oper, implem, op,last_com,days_com_off,other_details):
    return create_row_info(frt, frota, talhao, veloc, rpm, temp, rt, oper, implem, op,last_com,days_com_off,other_details)