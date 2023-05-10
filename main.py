import PySimpleGUI as sg
from backend import Insert, Select, Update, Delete, INSTALLED_MODULES
from Modules.passagem_turno import StartPassagemTurno
import pandas as pd
import os

#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
DEVELOPER_MODE = True

STATIC_PATH = os.path.dirname(os.path.abspath(__file__)) + '\Static'

ICON = STATIC_PATH + '\Símbolo.ico'

LOGO = STATIC_PATH + '\logo.png'

ADMIN_PASSWORD = 'moby@bi'

ADMIN_INFO = {
    'password': ADMIN_PASSWORD,
    'email': Select.user_information('powerbi_dev@mobyweb.com.br', ADMIN_PASSWORD)[0],
    'role': Select.user_information('powerbi_dev@mobyweb.com.br', ADMIN_PASSWORD)[2]
}

APP_NAME = 'Moby'

CARGOS = [
    'Assistente',
    'Analista',
    'Líder',
    'Gestor'
]

THEME = 'DarkTeal12'

VERSION = 'Versão 0.12'

#Telas
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Troca de senha
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class ChangePassword:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Senha antiga:              ',pad=(10,10)), sg.Input(size=(30,0),key='old_password', password_char='*'), sg.Push()],
            [sg.Push(), sg.Text('Nova senha:                ',pad=(10,10)), sg.Input(size=(30,0),key='new_password', password_char='*'), sg.Push()],
            [sg.Push(), sg.Text('Confirme a nova senha:',pad=(10,10)), sg.Input(size=(30,0),key='new_password2', password_char='*'), sg.Push()],
            [sg.Button('Cancelar', pad=(10,15), size=(15,0)), sg.Push(), sg.Button('Confirmar mudança', pad=(10,0), size=(15,0))]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.value = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancelar':
                break

            elif event == 'Confirmar mudança':

                if self.value['old_password'] == '' or \
                self.value['new_password'] == '' or \
                self.value['new_password2'] == '':
                    sg.popup('Preencha todos os campos.', title='Erro', icon=ICON)

                else:
                    if self.value['new_password'] != self.value['new_password2']:
                        sg.popup('As senhas devem ser iguais.', title='Erro', icon=ICON)

                    else:
                        if self.value['old_password'] == self.value['new_password']:
                            sg.popup('A nova senha digitada é igual a sua senha antiga, tente outra.', title='Erro', icon=ICON)

                        else:
                            if self.value['old_password'] != logged_password:
                                sg.popup('A senha antiga digitada não confere.', title='Erro', icon=ICON)
                            
                            else:
                                Update.user_update(logged_email, self.value['new_password'], logged_role)
                                sg.popup('Senha alterada com sucesso!', title='Sucesso', icon=ICON)
                                window.close()
                                sg.Exit()

#Lista de usuários
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class UserList:
    def __init__(self):
        df = pd.DataFrame(Select.user_list(), columns=['E-mail','Senha','Cargo','Último login'])
        data = df.values.tolist()
        header_list = list(df.columns)
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Table(data, headings=header_list, num_rows=20, auto_size_columns=True, enable_events=True, justification='center', key='-TABLE-', max_col_width=25)],
            [sg.Push(),sg.Button('Voltar ao menu',size=(15,0)),sg.Button('Editar',size=(15,0)),sg.Button('Excluir usuário',size=(15,0)),sg.Push()]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == 'Voltar ao menu' or event == sg.WIN_CLOSED:
                break

            elif event == 'Excluir usuário':
                try:
                    row_index = self.values['-TABLE-'][0]

                    selected_data = list(df.iloc[row_index])

                    if selected_data[0] != ADMIN_INFO['email']:

                        exclude_layout = [
                            [sg.Push(),sg.Text('Digite a palavra EXCLUIR abaixo para confirmar a exclusão do usuário'),sg.Push()],
                            [sg.Push(), sg.Input(size=(30,0), key='exclude'), sg.Push()],
                            [sg.Push(), sg.Button('Cancelar',size=(15,0)), sg.Button('Excluir',size=(15,0)), sg.Push()]
                        ]

                        exclude_window = sg.Window(APP_NAME, exclude_layout, icon=ICON)

                        while True:
                            exclude_event, exclude_values = exclude_window.read()

                            if exclude_event == 'Excluir':
                                if exclude_values['exclude'] == 'EXCLUIR':
                                    Delete.delete_user(selected_data[0])
                                    sg.popup('Usuário excluído com sucesso', title='Exclusão de usuário', icon=ICON)
                                    exclude_window.close()
                                    break
                                else:
                                    sg.popup('Incorreto. Verifique a ortografia e se todas as letras estão maiúsculas.')

                            elif exclude_event == sg.WIN_CLOSED or exclude_event == 'Cancelar':
                                exclude_window.close()
                                break

                    else:
                        sg.popup('O usuário de administrador não pode ser excluído.', title='Erro', icon=ICON)

                except:
                    pass

            elif event == 'Editar':
                try:
                    row_index = self.values['-TABLE-'][0]

                    selected_data = list(df.iloc[row_index])

                    checkboxes = []

                    actual_modules = Select.modules_information(selected_data[0])

                    for modulo in INSTALLED_MODULES:

                        if modulo in actual_modules:
                            checkboxes.append([sg.Checkbox(modulo, key=modulo, default=True)],)

                        else:
                            checkboxes.append([sg.Checkbox(modulo, key=modulo, default=False)],)


                    if selected_data[0] != ADMIN_INFO['email']:

                        edit_tab1_layout = [
                            [sg.Text('E-mail:'), sg.Text(selected_data[0], key='email')],
                            [sg.Text('Senha:'), sg.InputText(selected_data[1], key='senha')],
                            [sg.Text('Cargo:'), sg.InputCombo(CARGOS, selected_data[2], key='cargo')],
                            [sg.Text('Último login:'), sg.Text(selected_data[3], key='ultimo_login', size=(20,0))]
                        ]

                        edit_tab2_layout = [
                            [
                                sg.Frame('Módulos', [
                                    [sg.Column(
                                            checkboxes,
                                            scrollable=True, vertical_scroll_only=True, size=(350,150)
                                        )
                                    ]
                                ])
                            ]
                        ]

                        edit_layout = [
                            [sg.TabGroup([[sg.Tab('Informações', edit_tab1_layout), sg.Tab('Módulos', edit_tab2_layout)]])],
                            [sg.Button('Salvar'), sg.Button('Cancelar')]
                        ]

                        edit_window = sg.Window(APP_NAME, edit_layout, icon=ICON)

                        while True:
                            edit_event, edit_values = edit_window.read()

                            if edit_event == sg.WIN_CLOSED or edit_event == 'Cancelar':
                                edit_window.close()
                                break
                            
                            elif edit_event == 'Salvar':
                                try:
                                    modules_list = []

                                    for i in INSTALLED_MODULES:
                                        if edit_values[i] == True:
                                            modules_list.append(i)

                                    
                                    Update.modules_update(selected_data[0], modules_list)
                                    Update.user_update(selected_data[0], selected_data[1], selected_data[2])

                                    #df.iloc[row_index] = [edit_values['-EMAIL-'], edit_values['-SENHA-'], edit_values['-CARGO-'], edit_values['-LASTL-']]
                                    window['-TABLE-'].update(df.values.tolist())
        
                                    sg.popup('Informações atualizadas com sucesso!', title='Edição de usuário', icon=ICON)
                                    edit_window.close()

                                except:
                                    pass                       

                    elif selected_data[0] == ADMIN_INFO['email']:
                        sg.popup('O usuário de administrador não pode ser editado.', title='Erro', icon=ICON)
                except:
                    pass

        window.close()

#Menu ADM
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AdmMenu:
    def __init__(self):
        sg.theme(THEME)

        #Menu
        menu_def = [
            ['&Módulos', ['&Passagem de turno']],
            ['&Usuário', ['&Lista de usuários']]
        ]

        #Layout
        layout = [
            [sg.Menu(menu_def, key='-MENUBAR-')],
            [sg.Push(), sg.Text('Menu principal', pad=(10,10), font=('Arial', 18, 'bold')), sg.Push()],
            [sg.Push(), sg.Button('Lista de usuários', pad=(10,10), size=(30,0)), sg.Push()],
            [sg.Push(), sg.Button('Passagem de turno', pad=(10,10), size=(30,0)), sg.Push()],
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON, size=(400,200))

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'Lista de usuários':
                UserList()

            elif event == 'Passagem de turno':
                StartPassagemTurno()

        window.close()

#Menu
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PrincipalMenu:
    def __init__(self):
        sg.theme(THEME)

        #Menu
        menu_def = [
            ['&Módulos', ['&Passagem de turno']],
        ]

        #Layout
        layout = [
            [sg.Menu(menu_def, key='-MENUBAR-')],
            [sg.Push(), sg.Text('Menu principal', pad=(10,10), font=('Arial', 18, 'bold')), sg.Push()],
            [sg.Push(), sg.Button('Passagem de turno', pad=(10,10), size=(30,0)), sg.Push()],
            [sg.Button('Alterar senha', pad=(20,40), font=('Arial', 9)), sg.Push()],
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == 'Passagem de turno':
                if event in Select.modules_information(logged_email):
                    StartPassagemTurno()

                else:
                    sg.popup('Você não tem acesso a este módulo, solicite acesso ao supervisor ou ao administrador da área.', title='Erro', icon=ICON)

            elif event == 'Alterar senha':
                ChangePassword()

        window.close()

#Tela de registro
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Register:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Registro de usuário',pad=(10,10)), sg.Push()],
            [sg.Push(), sg.Text('E-mail:                   ',pad=(10,10)), sg.Input(size=(30,0), key='register_email'), sg.Push()],
            [sg.Push(), sg.Text('Senha:                    ',pad=(10,10)), sg.Input(size=(30,0), key='register_password', password_char='*'), sg.Push()],
            [sg.Push(), sg.Text('Confirme sua senha:',pad=(10,10)), sg.Input(size=(30,0), key='confirm_password', password_char='*'), sg.Push()],
            [sg.Push(), sg.Text('Cargo:                    ',pad=(10,10)), sg.Combo(CARGOS, size=(28,0), key='register_cargo', readonly=True), sg.Push()],
            [sg.Button('Voltar', pad=(10,15), size=(15,0)), sg.Push(), sg.Button('Registrar', pad=(10,0), size=(15,0))]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, resizable=True, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Voltar':
                break
            
            elif event == 'Registrar':
                if self.values['register_email'] != '' \
                or self.values['register_password'] != '' \
                or self.values['register_cargo'] != '':
                    if self.values['register_password'] == self.values['confirm_password']:
                        if '@' in self.values['register_email'] and '.com' in self.values['register_email']:
                            try:
                                Insert.register(self.values['register_email'],self.values['register_user'],self.values['register_password'],self.values['register_cargo'])
                                sg.popup('Usuário registrado com sucesso!', title='Registro de usuário', icon=ICON)
                            except:
                                sg.popup('E-mail já registrado, tente outro endereço.', title='Erro', icon=ICON)
                        else:
                            sg.popup('O endereço de e-mail parece inválido, tente outro endereço.', title='Erro', icon=ICON)
                    else:
                        sg.popup('As senhas devem ser iguais.', title=APP_NAME, icon=ICON)
                else:
                    sg.popup('Preencha todos os campos.', title=APP_NAME, icon=ICON)    

        window.close()

#Login de administrador
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AdminLogin:
    def __init__(self, roles, screen):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Autenticação', pad=(10,10)), sg.Push()],
            [sg.Push(), sg.Text('E-mail:',pad=(10,10)), sg.Input(size=(30,0), key='admin_email'), sg.Push()],
            [sg.Push(), sg.Text('Senha:  ',pad=(10,10)), sg.Input(size=(30,0), key='admin_password', password_char='*'), sg.Push()],
            [sg.Button('Voltar', pad=(10,15), size=(15,0)), sg.Button('Login', pad=(10,0), size=(15,0))]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Voltar':
                break
            elif event == 'Login':
                if Select.login_authentication(self.values['admin_email'], self.values['admin_password']) == True:
                    if Select.role_authentication(self.values['admin_email'], self.values['admin_password']) in roles:
                        window.close()
                        screen()
                        break
                    else:
                        sg.popup('Esse usuário não tem permissão.', title='Erro', icon=ICON)
                else:
                    sg.popup('Usuário inexistente.', title='Erro', icon=ICON)

        window.close()

#Login de Usuário
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Login:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Bem vindo! Insira o email e senha abaixo para realizar o login', pad=(10,10)), sg.Push()],
            [sg.Push(), sg.Text('Email:   ',pad=(10,10)), sg.Input(size=(30,0), key='email'), sg.Push()],
            [sg.Push(), sg.Text('Senha:  ',pad=(10,10)), sg.Input(size=(30,0),key='password', password_char='*'), sg.Push()],
            [sg.Button('Registro de usuário', pad=(10,15), size=(15,0)), sg.Button('Login', pad=(10,10), size=(15,0)), sg.Button('Sair', pad=(10,10), size=(15,0))],
            [sg.Text(VERSION)]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()
            global logged_password
            global logged_email
            global logged_role
            global last_login

            if event == sg.WIN_CLOSED or event == 'Sair':
                break

            elif event == 'Registro de usuário':
                AdminLogin(['Gestor', 'Líder', 'Desenvolvedor'], Register)

            elif event == 'Login':
                if '@' not in self.values['email']:
                    login_email = self.values['email'] + '@mobyweb.com.br'
                    if login_email == ADMIN_INFO['email'] and self.values['password'] == ADMIN_INFO['password']:
                        logged_password = ADMIN_INFO['password']
                        logged_email = ADMIN_INFO['email']
                        logged_role = ADMIN_INFO['role']
                        Update.last_login(logged_email)
                        sg.popup('Login realizado como administrador!', title='Login ADM', icon=ICON)
                        window.close()
                        AdmMenu()
                    elif Select.login_authentication(login_email, self.values['password']) == True:
                        user_info = Select.user_information(login_email, self.values['password'])
                        logged_email, logged_password, logged_role, last_login = user_info
                        Update.last_login(logged_email)
                        sg.popup('Login realizado com sucesso!', title='Login', icon=ICON)
                        window.close()
                        PrincipalMenu()
                    else:
                        sg.popup('Email e/ou senha incorretos.',title='Erro', icon=ICON)

                else:
                    if self.values['email'] == ADMIN_INFO['email'] and self.values['password'] == ADMIN_INFO['password']:
                        logged_password = ADMIN_INFO['password']
                        logged_email = ADMIN_INFO['email']
                        logged_role = ADMIN_INFO['role']
                        Update.last_login(logged_email)
                        sg.popup('Login realizado como administrador!', title='Login ADM', icon=ICON)
                        window.close()
                        AdmMenu()
                    elif Select.login_authentication(self.values['email'], self.values['password']) == True:
                        user_info = Select.user_information(self.values['email'], self.values['password'])
                        logged_email, logged_password, logged_role, last_login = user_info
                        Update.last_login(logged_email)
                        sg.popup('Login realizado com sucesso!', title='Login', icon=ICON)
                        window.close()
                        PrincipalMenu()
                    else:
                        sg.popup('Email e/ou senha incorretos.',title='Erro', icon=ICON)

        window.close()

#Logo popup
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Logo:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Image(LOGO)],
            [sg.Text(VERSION)]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, no_titlebar=True)
        window.SetIcon(icon=ICON)

        window.read(timeout=3000)

        window.close()

#Start engine
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Start:
    def __init__(self):
        Logo()
        Update.modules_update(ADMIN_INFO['email'], INSTALLED_MODULES)
        if Select.login_authentication(ADMIN_INFO['email'], ADMIN_INFO['password']) == True:
            Login()
        else:
            sg.popup('Ops! Parece que há divergências entre as informações de administrador no banco de dados, por favor corrija antes de iniciar o aplicativo.', title='Erro', icon=ICON)


Start()