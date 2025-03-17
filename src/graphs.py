import pandas as pd
from src.cncts.apis import *
from src.cncts.apis import ApiSolinftec
from queries import Queries
import flet as ft
import plotly.graph_objects as go
import plotly.io as pio
import io
import sys
from flet_webview import WebView
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import base64
matplotlib.use('Agg')
print(sys.executable)
print(sys.path)

class Graphs:
    def __init__(self):
        ...
    def alter_theme(self,column_graphs, event):
        json_elements = column_graphs.data
        normal_text = json_elements['grafico']['normal_text']
        hover_text = json_elements['grafico']['hover_text']

        if event:
            normal_text.color = ft.Colors.WHITE
        else:
            normal_text.color = ft.Colors.BLACK


    def informacoes_gerais_chart(self, column_graphs):
        normal_radius = 50
        hover_radius = 60
        normal_title_style = ft.TextStyle(
            size=9, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=11,
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK12),
        )
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 0)
        pd.set_option('display.max_rows', 500)

        # Conecta à API e obtém os dados
        data_oper = ApiSolinftec().conecta_solinftec()
        data_oper = json_normalize(data_oper)
        data_oper['cdOperacao'] = data_oper['cdOperacao'].astype(str)

        list_json, response = Api_Liberali().busca_sap_api_query(Queries().busca_rt_sap())
        list_json = json_normalize(list_json)

        opers_slft = ApiSolinftec().get_api_22(0)
        opers_slft = json_normalize(opers_slft)

        # Combina os dados
        opers_whith_rt = pd.merge(opers_slft, list_json, left_on='CD_ORDEM_SERVICO', right_on='DocEntry', how="left")
        opers_complet = pd.merge(opers_whith_rt, data_oper, left_on='CD_OPERACAO', right_on='cdOperacao', how="left")
        opers_complet['CD_TALHAO'] = opers_complet['CD_TALHAO'].astype(int)

        # Função para verificar o status das operações
        def verifica_status(df_original):
            df = df_original.copy()
            filtro_manobra = df['CD_OPERACAO'] != '143'
            df = df[filtro_manobra]

            OS_SLFT = df['CD_ORDEM_SERVICO'].notnull()
            OS_vs_RT = df['CD_ORDEM_SERVICO'] == df['DocEntry']
            df['StatusRT'] = OS_SLFT & OS_vs_RT

            OpSlft_vs_OpRT = df['CD_OPERACAO'] == df['U_CodOperaca']
            df['StatusOP'] = OpSlft_vs_OpRT

            TalhaoSlft_vs_TalhaoRT = df['CD_TALHAO'] == df['ID_talhao']
            df['StatusTalhao'] = TalhaoSlft_vs_TalhaoRT

            def definir_causa(row):
                if not row['StatusRT']:
                    return "NOK_RT"
                elif not row['StatusTalhao']:
                    return "NOK_Talhao"
                elif not row['StatusOP']:
                    return "NOK_OP"
                else:
                    return "OK"

            df['Class_Linha'] = df.apply(definir_causa, axis=1)
            return df

        # Funções para filtrar e processar os dados
        def filtra_opers_produtivas(df):
            filtro = df['FG_TIPO_OPERACAO'] == 'P'
            return df[filtro]

        def filtra_equipamentos_agricultura(df):
            eqpm = ['120014', '120015', '120027', '120028', '123001', '123002', '123004', '123005']
            filtro = df['CD_EQUIPAMENTO'].isin(eqpm)
            return df[filtro]

        def relat_status_area(df):
            return df.groupby('Class_Linha')['VL_AREA_HECTARES_EQUIPAMENTO'].sum().reset_index()

        def total_area_trabalhada(df):
            return df['VL_AREA_HECTARES_EQUIPAMENTO'].sum()

        def relat_operacoes_realizadas(df):
            return df.pivot_table(
                index='descOperacao',
                columns='Class_Linha',
                values='VL_AREA_HECTARES_EQUIPAMENTO',
                aggfunc='sum',
                fill_value=0
            )

        def relat_operacoes_realizadas_dia(df):
            df_filtrado = df[df['Class_Linha'] == 'OK']
            return df_filtrado.pivot_table(
                index='descOperacao',
                columns='DT_HR_INI_JORNADA',
                values='VL_AREA_HECTARES_EQUIPAMENTO',
                aggfunc='sum',
                fill_value=0
            )

        def generate_section(value, title, color):
            return ft.PieChartSection(
                value=value,
                title=title,
                title_style=normal_title_style,
                color=color,
                radius=normal_radius,
            )

        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()


        def tabela_operacoes_dia(df):
            colunas = df.columns.tolist()

            tam_col1 = 12*0.5
            if len(colunas)>0:
                tam_others_col = ((12-tam_col1)/len(colunas))
            else:
                tam_others_col = 1
            columns_header = ft.ResponsiveRow(controls=[
                                ft.Text("Operação", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE, col=tam_col1, size=11)
                            ])
            columns_body = ft.ResponsiveRow(controls=[
                ft.Text("Total ->", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK,
                        col=tam_col1, size=11)
            ])

            header = ft.Container(  # Usando ft.Container em vez de ft.Row
                            content=columns_header,
                    bgcolor=ft.colors.BLUE_900,  # Define a cor de fundo do ft.Row
                    padding=10,  # Adiciona um pequeno padding para melhor visualização
                    alignment=ft.alignment.center, #Alinha o Row dentro do container
                    )
            body = ft.Container(  # Usando ft.Container em vez de ft.Row
                            content=columns_body,
                    bgcolor=ft.colors.GREY_50,  # Define a cor de fundo do ft.Row
                    padding=10,  # Adiciona um pequeno padding para melhor visualização
                    alignment=ft.alignment.center, #Alinha o Row dentro do container
                    )
            rows = ft.Column(
                scroll=ft.ScrollMode.ADAPTIVE,
                height=150,
            )

            def create_columns(c, sum_area):
                columns_header.controls.append(
                    ft.Text(c, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, col=tam_others_col, size=11, text_align=ft.TextAlign.CENTER),
                )
                columns_body.controls.append(
                    ft.Text(f"{sum_area:.2f}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, col=tam_others_col, size=11,
                            text_align=ft.TextAlign.CENTER),
                )

            def create_rows(ind, ro):
                cells = ft.ResponsiveRow(controls=[ft.Text(ind, weight=ft.FontWeight.BOLD, col=tam_col1, size=11)])
                def create_cells(r):
                    cells.controls.append(
                        ft.Text(f"{r:.2f}", col=tam_others_col, size=11, text_align=ft.TextAlign.CENTER)
                    )
                for r in ro:
                    create_cells(r)
                rows.controls.append(cells)

            table = ft.Column(
                        controls=[
                            header,
                            rows,
                            body
                        ],
                expand=True,
                col=4,
                # Estilo do texto do cabeçalho
            )

            for index, row in df.iterrows():
                create_rows(index, row)
            for c in colunas:
                sum_area = df[c].sum()
                create_columns(c, sum_area)
            return table

        # Processamento dos dados
        equipamentosagricultura = filtra_equipamentos_agricultura(opers_complet)
        opersprodutivas = filtra_opers_produtivas(equipamentosagricultura)
        df_final_class = verifica_status(opersprodutivas)
        status_operacoes = relat_status_area(df_final_class)
        operacoes_realizadas = relat_operacoes_realizadas(df_final_class)
        operacoes_realizadas_dia = relat_operacoes_realizadas_dia(df_final_class)
        area_trabalhada = total_area_trabalhada(df_final_class)
        chart = ft.PieChart(
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event,
            expand=True,
            col=2.5
        )
        for i in range(len(status_operacoes['Class_Linha'])):
            area_grafico = (status_operacoes.loc[i, 'VL_AREA_HECTARES_EQUIPAMENTO']/area_trabalhada)*100
            title = f"{round(area_grafico, 2)}% - {round(status_operacoes.loc[i, 'VL_AREA_HECTARES_EQUIPAMENTO'], 2)}Ha - {status_operacoes.loc[i, 'Class_Linha']}"
            if status_operacoes.loc[i, 'Class_Linha'] == 'OK':
                cor = ft.Colors.GREEN
            elif status_operacoes.loc[i, 'Class_Linha'] == 'NOK_RT':
                cor = ft.Colors.RED
            elif status_operacoes.loc[i, 'Class_Linha'] == 'NOK_Talhao':
                cor = ft.Colors.GREY
            else:
                cor = ft.Colors.YELLOW
            chart.sections.append(generate_section(value=area_grafico, title=title, color=cor))

        tab_oper = tabela_operacoes_dia(operacoes_realizadas)
        linha_01 = ft.ResponsiveRow([
            chart,
            tab_oper
        ],
        height=250)
        linha_02 = ft.ResponsiveRow([
            ft.Container(bgcolor=ft.Colors.BLACK, height=200, content=ft.Text('Espaço Reservado'))
        ])

        column_graphs.controls = [
            linha_01,
            linha_02
        ]

        column_graphs.data = {
            'grafico': {
                'normal_text': normal_title_style,
                'hover_text': hover_title_style,
                'chart': chart
            },
            'tabela_operacoes': tab_oper
        }