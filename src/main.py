import threading
import time
import flet as ft
from functions import *
from src.cncts.apis import *
from graphs import Graphs
from src.cncts.auth_firebase import autenticar_usuario, registrar_usuario, alterar_senha, registrar_log


class DadosWindow:
    def __init__(self):
        self.operacoes_apoio = ['143', '305', '48', '190', '221', '69', '4', '224']
        self.veiculos_apoio = []
        self.equip_sem_tela = ['120020', '120023']
        self.msgAlertas = []
        self.contador_alert = []
        self.contador_alert2 = 0
        self.first_loop = True
        self.list_json = ''
        self.rts_sap = []
        self.username = ''

    def set_username(self, user):
        self.username = user

    def get_username(self):
        return self.username

    def set_contador_alert(self, caler):
        self.contador_alert.append(caler)

    def get_contador_alert(self):
        # print(self.contador_alert)
        return self.contador_alert

    def set_contador_alert2(self, calert):
        self.contador_alert2 += calert

    def get_contador_alert2(self):
        return self.contador_alert2


def tela_login(page: ft.Page):
    page.window.maximized = True
    window = DadosWindow()
    logo_login = ft.ResponsiveRow([
        ft.Container(col=4),
        ft.Image(
            src="assets\icon.png",
            col=4
        ),
        ft.Container(col=4),
    ]
    )

    def autenticar(e):
        lb_user = txt_usuario.value.strip()
        lb_password = txt_senha.value.strip()
        if lb_user == '' or lb_password == '':
            page.open(ft.AlertDialog(title=ft.Text("Campo de usuário ou senha em branco.")))
        else:
            try:
                if autenticar_usuario(nome_usuario=lb_user, senha=lb_password):
                    # log = {'usuario': lb_user, 'datahora': f'{datetime.today()}'}
                    registrar_log(lb_user, f'{datetime.today()}')
                    window.set_username(lb_user)
                    page.clean()  # Limpa a tela de login
                    app(page, window)  # Inicia a aplicação principal
                else:
                    page.open(ft.AlertDialog(title=ft.Text("Credenciais Inválidas.")))
                    page.update()
            except requests.exceptions.HTTPError as http_err:
                print(f"❌ HTTP Error: {http_err}")

    txt_usuario = ft.TextField(label="Nome de usuário")
    txt_senha = ft.TextField(label="Senha", password=True)
    btn_login = ft.ResponsiveRow([ft.ElevatedButton(text="Login", on_click=autenticar)])
    lbl_mensagem = ft.Text("", color=ft.Colors.BLACK87)

    page.add(ft.ResponsiveRow([
        ft.Column([

        ], col=4),
        ft.Column([
            logo_login,
            txt_usuario,
            txt_senha,
            btn_login,
            lbl_mensagem
        ], col=4),
        ft.Column([
        ], col=4)
    ])
    )


def app(page: ft.Page, window):
    page.window.maximized = True
    page.title = "Natasha - Centro de Operações Agricolas - Fazenda Santa Fé"
    page.theme_mode = ft.ThemeMode.LIGHT

    def alter_theme(e):
        if e.control.value:
            page.theme_mode = ft.ThemeMode.DARK
            logodark = logo.content
            logodark.src = "assets\\logo_dark.png"
            create_container(
                gridview,
                window,
                page
            )
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            logolight = logo.content
            logolight.src = "assets\\logo.png"
            create_container(
                gridview,
                window,
                page
            )
        Graphs().alter_theme(graphs, event=e.control.value)
        page.update()

    bt_switch_theme = ft.Switch(
            adaptive=True,
            label="Dark Mode",
            value=False,
            col=1,
            on_change=alter_theme
        )
    logo = ft.Container(
        ft.Image(
            # src=".\src\\assets\logo.png",
            src="assets\\logo.png",
            width=250,
            height=40
        ),
        # padding=ft.padding.symmetric(vertical=25)
    )
    gridview = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=260,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        padding=ft.Padding(left=40, right=40, top=0, bottom=0)
    )

    def show_settings_frota(e):
        # print(type(e.control.data))
        lb_frota.value = f"{e.control.data['frota']}"
        cbx_alrt_talhao.value = e.control.data['alertas']['alrt_talhao']
        cbx_alrt_talhao.data = {"chave_dict": 'alrt_talhao', "json_param": e.control.data}
        cbx_alrt_veloc.value = e.control.data['alertas']['alrt_veloc']
        cbx_alrt_veloc.data = {"chave_dict": 'alrt_veloc', "json_param": e.control.data}
        cbx_alrt_rpm.value = e.control.data['alertas']['alrt_rpm']
        cbx_alrt_rpm.data = {"chave_dict": 'alrt_rpm', "json_param": e.control.data}
        cbx_alrt_temp.value = e.control.data['alertas']['alrt_temp']
        cbx_alrt_temp.data = {"chave_dict": 'alrt_temp', "json_param": e.control.data}
        cbx_alrt_rt.value = e.control.data['alertas']['alrt_rt']
        cbx_alrt_rt.data = {"chave_dict": 'alrt_rt', "json_param": e.control.data}
        cbx_alrt_oper.value = e.control.data['alertas']['alrt_oper']
        cbx_alrt_oper.data = {"chave_dict": 'alrt_oper', "json_param": e.control.data}
        cbx_alrt_implem.value = e.control.data['alertas']['alrt_implem']
        cbx_alrt_implem.data = {"chave_dict": 'alrt_implem', "json_param": e.control.data}
        cbx_alrt_op.value = e.control.data['alertas']['alrt_op']
        cbx_alrt_op.data = {"chave_dict": 'alrt_op', "json_param": e.control.data}
        tx_param_temp.value =  e.control.data['parametros']['param_temp']
        tx_param_temp.data = {"chave_dict": 'param_temp', "json_param": e.control.data}
        tx_param_rpm.value =  e.control.data['parametros']['param_rpm']
        tx_param_rpm.data = {"chave_dict": 'param_rpm', "json_param": e.control.data}
        tx_param_veloc.value =  e.control.data['parametros']['param_veloc']
        tx_param_veloc.data = {"chave_dict": 'param_veloc', "json_param": e.control.data}
        btn_salva_param.data =  e.control.data['id_firebase']

        # print("firebase", e.control.data['id_firebase'], btn_salva_param.data)

        bs_param.open = True
        page.update()

    def edit_param_frota(e):
        json_param = e.control.data['json_param']
        chave = e.control.data['chave_dict']
        valor = e.control.value
        if valor == '' or valor is None:  # Verificação de string vazia ou None
            json_param['parametros'][chave] = 0
        else:
            json_param['parametros'][chave] = int(valor)

    def edit_alert_frota(e):
        json_param = e.control.data['json_param']
        chave = e.control.data['chave_dict']
        json_param['alertas'][chave] = e.control.value

    def salva_param_firebase(e):
        key_id = e.control.data
        dados = {'frota': key_id,
                 'alrt_frota': cbx_alrt_talhao.value,
                 'alrt_implem': cbx_alrt_veloc.value,
                 'alrt_op': cbx_alrt_rpm.value,
                 'alrt_oper': cbx_alrt_oper.value,
                 'alrt_rpm': cbx_alrt_rpm.value,
                 'alrt_rt': cbx_alrt_rt.value,
                 'alrt_talhao': cbx_alrt_talhao.value,
                 'alrt_temp': cbx_alrt_temp.value,
                 'alrt_veloc': cbx_alrt_veloc.value,
                 'param_rpm': int(tx_param_rpm.value),
                 'param_temp': int(tx_param_temp.value),
                 'param_veloc': int(tx_param_veloc.value)
        }
        edit_param(key_id, dados)
        bs_param.open = False
        page.update()

    lb_frota = ft.Text()
    cbx_alrt_talhao= ft.Checkbox(label="Alertar Talhão", on_change=edit_alert_frota, col=6)
    cbx_alrt_veloc= ft.Checkbox(label="Alertar Velocidade", on_change=edit_alert_frota, col=6)
    cbx_alrt_rpm= ft.Checkbox(label="Alertar RPM", on_change=edit_alert_frota, col=6)
    cbx_alrt_temp= ft.Checkbox(label="Alertar Temperatura", on_change=edit_alert_frota, col=6)
    cbx_alrt_rt= ft.Checkbox(label="Alertar Rec. Tecn.", on_change=edit_alert_frota, col=6)
    cbx_alrt_oper= ft.Checkbox(label="Alertar Operação", on_change=edit_alert_frota, col=6)
    cbx_alrt_implem= ft.Checkbox(label="Alertar Implemento", on_change=edit_alert_frota, col=6)
    cbx_alrt_op= ft.Checkbox(label="Alertar Operador", on_change=edit_alert_frota, col=6)

    tx_param_veloc = ft.TextField(label="Velocidade", col=6, text_size=12, height=40, on_change=edit_param_frota)
    tx_param_rpm = ft.TextField(label="RPM", col=6, text_size=12, height=40, on_change=edit_param_frota)
    tx_param_temp = ft.TextField(label="Temperatura", col=6, text_size=12, height=40, on_change=edit_param_frota)
    btn_salva_param = ft.TextButton(text="Salvar Parâmetros", on_click=salva_param_firebase)

    coluna_param = ft.Column([
        ft.ResponsiveRow([lb_frota]),
        ft.ResponsiveRow([
        cbx_alrt_talhao,
        cbx_alrt_veloc,]),
        ft.ResponsiveRow([
        cbx_alrt_rpm,
        cbx_alrt_temp,]),
        ft.ResponsiveRow([
        cbx_alrt_rt,
        cbx_alrt_oper,]),
        ft.ResponsiveRow([
        cbx_alrt_implem,
        cbx_alrt_op,]),
        tx_param_veloc,
        tx_param_rpm,
        tx_param_temp,
        ft.ResponsiveRow([btn_salva_param])
    ], tight=True, alignment=ft.alignment.center_right)

    bs_param = ft.BottomSheet(
        ft.Container(
            content=coluna_param,
            padding=20,
            height=720,
            width=500
        ),
        open=False,
    )

    def menu_usuario(e):
        bs_menu.open = True
        page.update()

    def modify_user(e):
        if e.control.value:
            txt_user.disabled = False
            txt_user.visible = True
            txt_type_modify.value = 'Crie abaixo o novo usuário'
        else:
            txt_user.disabled = True
            txt_user.visible = False
            txt_type_modify.value = 'Altere sua senha'
        page.update()

    def btn_confirm(e):
        if cbx_type_modify_user.value:
            lb_user = txt_user.value.strip()
            lb_password = txt_pass1.value.strip()
            lb_re_password = txt_pass2.value.strip()

            if lb_user == '' or lb_password == '':
                page.open(ft.AlertDialog(title=ft.Text("Campo de usuário ou senha em branco.")))
            else:
                try:
                    if lb_re_password == lb_password:
                        registrar_usuario(nome_usuario=lb_user, senha=lb_password)
                        txt_user.value = ''
                        txt_pass1.value = ''
                        txt_pass2.value = ''
                        page.open(ft.AlertDialog(title=ft.Text("Usuário Criado com Sucesso!!!")))
                    else:
                        page.open(ft.AlertDialog(title=ft.Text("As senhas digitadas não conferem.")))
                        page.update()
                except requests.exceptions.HTTPError as http_err:
                    print(f"❌ HTTP Error: {http_err}")
        else:
            lb_password = txt_pass1.value.strip()
            lb_re_password = txt_pass2.value.strip()
            try:
                if lb_re_password == lb_password:
                    alterar_senha(nome_usuario=window.get_username(), senha=lb_password)
                    txt_pass1.value = ''
                    txt_pass2.value = ''
                    page.open(ft.AlertDialog(title=ft.Text("Senha Alterada com Sucesso!!!")))
                else:
                    page.open(ft.AlertDialog(title=ft.Text("As senhas digitadas não conferem.")))
                    page.update()
            except requests.exceptions.HTTPError as http_err:
                print(f"❌ HTTP Error: {http_err}")

    cbx_type_modify_user = ft.Checkbox(label="Criar novo usuário?", value=False, on_change=modify_user)
    txt_user = ft.TextField(label="Username", disabled=True, visible=False)
    txt_pass1 = ft.TextField(label="Password", password=True)
    txt_pass2 = ft.TextField(label="Re-Password", password=True)
    btn_confirm = ft.ElevatedButton(text="Confirm", on_click=btn_confirm)
    txt_type_modify = ft.Text("Altere sua senha",
                               size=14,
                               text_align=ft.TextAlign.CENTER,
                               color=ft.Colors.BLACK
                           )
    coluna_menu = ft.Column([
        ft.ResponsiveRow([ft.Container(content=ft.Text("Menu de Usuário",
                                                   size=14,
                                                   text_align=ft.TextAlign.CENTER,
                                                   color=ft.Colors.WHITE
                                               ),
                                       bgcolor=ft.Colors.BLUE_900)]),
        ft.ResponsiveRow([txt_type_modify]),
        ft.ResponsiveRow([cbx_type_modify_user]),
        ft.ResponsiveRow([txt_user]),
        ft.ResponsiveRow([txt_pass1]),
        ft.ResponsiveRow([txt_pass2]),
        ft.ResponsiveRow([btn_confirm])
    ], tight=True, alignment=ft.alignment.center_right)

    bs_menu = ft.BottomSheet(
        ft.Container(
            content=coluna_menu,
            padding=20,
            height=720,
            width=500
        ),
        open=False,
    )

    bt_menu = ft.ElevatedButton(
        "Menu",
        icon="menu",
        col=1,
        on_click=menu_usuario
    )
    page.overlay.append(bs_menu)
    page.overlay.append(bs_param)
    graphs = ft.Column()
    header = ft.ResponsiveRow(controls=[
                bt_menu,
                ft.Container(content=logo,alignment=ft.alignment.center, col=10),
                bt_switch_theme
            ],
    )

    body_column = ft.Column(
        controls=[
            header,
            gridview,
            graphs
        ]
    )

    def init():
        create_container(
            gridview,
            window,
            page
        )

        if window.first_loop:
            for f in gridview.controls:
                for el in f.data['elements']:
                    if isinstance(el, ft.ElevatedButton):
                        el.on_click = show_settings_frota
                        el.data = f.data["json_param"]
                operations_analyzer(f, window, page)
        window.first_loop = False
        page.update()
        threading.Timer(10, init).start()

    def update_rt():
        window.list_json, response = Api_Liberali().busca_sap_api_query(Queries().busca_rt_sap())
        for l in window.list_json:
            window.rts_sap.append(str(l['DocEntry']))
        threading.Timer(60, update_rt).start()

    def update_charts():
        Graphs().informacoes_gerais_chart(graphs)
        page.update()
        threading.Timer(60, update_charts).start()

    page.add(
        body_column
    )

    update_rt()
    init()
    update_charts()

def main(page: ft.Page):
    page.title = "Aprovações e Pagamentos"
    tela_login(page)  # Exibe a tela de login inicialmente
ft.app(target=main)
