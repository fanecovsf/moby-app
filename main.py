import PySimpleGUI as sg
from backend import Insert, Select, Update
import pandas as pd

#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
DEVELOPER_MODE = True

ADMIN_INFO = {
    'user': 'admin',
    'password': 'moby@bi',
    'email': 'powerbi_dev@mobyweb.com.br',
    'role': 'Administrador'
}

APP_NAME = 'Moby'

CARGOS = [
    'Assistente',
    'Analista',
    'Supervisor',
    'Gestor'
]

THEME = 'DarkTeal12'

#Parâmetros
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
if DEVELOPER_MODE == True:
    ICON = r'C:\Users\gustavo.faneco\OneDrive - MOBY\Documents\Projects\Python\Aplicativos\Demo\static\Símbolo.ico'
    LOGO = r'C:\Users\gustavo.faneco\OneDrive - MOBY\Documents\Projects\Python\Aplicativos\Demo\static\logo.png'
elif DEVELOPER_MODE == False:
    ICON = 'Símbolo.ico'
    LOGO = 'logo.png'

#Lista de usuários
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class UserList:
    def __init__(self):
        df = pd.DataFrame(Select.user_list(), columns=['E-mail','Usuário','Senha','Cargo'])
        data = df.values.tolist()
        header_list = list(df.columns)
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Table(data, headings=header_list, num_rows=20, auto_size_columns=True, enable_events=True, justification='center', key='-TABLE-', max_col_width=25)],
            [sg.Button('Editar',size=(20,0)),sg.Push(),sg.Button('Sair',size=(20,0))]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == 'Sair' or event == sg.WIN_CLOSED:
                break

            elif event == 'Editar':
                try:
                    row_index = self.values['-TABLE-'][0]

                    selected_data = list(df.iloc[row_index])

                    edit_layout = [
                        [sg.Text('E-mail:'), sg.InputText(selected_data[0], key='-EMAIL-')],
                        [sg.Text('Usuário:'), sg.InputText(selected_data[1], key='-USUÁRIO-')],
                        [sg.Text('Senha:'), sg.InputText(selected_data[2], key='-SENHA-')],
                        [sg.Text('Cargo:'), sg.InputCombo(CARGOS, selected_data[3], key='-CARGO-')],
                        [sg.Button('Salvar'), sg.Button('Cancelar')]
                    ]

                    edit_window = sg.Window(APP_NAME, edit_layout, icon=ICON)

                    while True:
                        edit_event, edit_values = edit_window.read()

                        if edit_event == sg.WIN_CLOSED or edit_event == 'Cancelar':
                            edit_window.close()
                            break

                        elif edit_event == 'Salvar':
                            df.iloc[row_index] = [edit_values['-EMAIL-'], edit_values['-USUÁRIO-'], edit_values['-SENHA-'], edit_values['-CARGO-']]

                            window['-TABLE-'].update(df.values.tolist())

                            Update.user_update(edit_values['-EMAIL-'], edit_values['-USUÁRIO-'], edit_values['-SENHA-'], edit_values['-CARGO-'])

                            edit_window.close()
                except:
                    pass

        window.close()

#Menu ADM
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AdmMenu:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Menu principal', pad=(10,10), font=('Arial', 18, 'bold')), sg.Push()],
            [sg.Push(), sg.Button('Lista de usuários', pad=(10,10)), sg.Push()],
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

        window.close()

#Menu
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PrincipalMenu:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Menu principal', pad=(10,10), font=('Arial', 18, 'bold')), sg.Push()],
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED:
                break

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
            [sg.Push(), sg.Text('Usuário:                  ',pad=(10,10)), sg.Input(size=(30,0), key='register_user'), sg.Push()],
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
                and self.values['register_user'] != '' \
                and self.values['register_password'] != '' \
                and self.values['register_cargo'] != '':
                    if self.values['register_password'] == self.values['confirm_password']:
                        if '@' in self.values['register_email'] and '.com' in self.values['register_email']:
                            if Select.user_verification(self.values['register_user']) == True:
                                try:
                                    Insert.register(self.values['register_email'],self.values['register_user'],self.values['register_password'],self.values['register_cargo'])
                                    sg.popup('Usuário registrado com sucesso!', title='Registro de usuário')
                                except:
                                    sg.popup('E-mail já registrado, tente outro endereço.')
                            else:
                                sg.popup('Usuário já registrado, tente outro nome de usuário.')
                        else:
                            sg.popup('O endereço de e-mail parece inválido, tente outro endereço.')
                    else:
                        sg.popup('As senhas devem ser iguais.', title=APP_NAME)
                else:
                    sg.popup('Preencha todos os campos.', title=APP_NAME)    

        window.close()

#Login de administrador
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AdminLogin:
    def __init__(self, screen):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Digite os dados de administrador:', pad=(10,10)), sg.Push()],
            [sg.Push(), sg.Text('Usuário:',pad=(10,10)), sg.Input(size=(30,0), key='admin_user'), sg.Push()],
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
                if self.values['admin_user'] == ADMIN_INFO['user'] and self.values['admin_password'] == ADMIN_INFO['password']:
                    window.close()
                    screen()
                    break
                else:
                    sg.popup('Dados incorretos.')

        window.close()

#Login de Usuário
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Login:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text('Bem vindo! Insira o usuário e senha abaixo para realizar o login', pad=(10,10)), sg.Push()],
            [sg.Push(), sg.Text('Usuário:',pad=(10,10)), sg.Input(size=(30,0), key='user'), sg.Push()],
            [sg.Push(), sg.Text('Senha:  ',pad=(10,10)), sg.Input(size=(30,0),key='password', password_char='*'), sg.Push()],
            [sg.Button('Registro de usuário', pad=(10,15), size=(15,0)), sg.Button('Login', pad=(10,10), size=(15,0)), sg.Button('Sair', pad=(10,10), size=(15,0))]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()
            global logged_user
            global logged_password
            global logged_email
            global logged_role

            if event == sg.WIN_CLOSED or event == 'Sair':
                break

            elif event == 'Registro de usuário':
                AdminLogin(Register)

            elif event == 'Login':
                if self.values['user'] == ADMIN_INFO['user'] and self.values['password'] == ADMIN_INFO['password']:
                    logged_user = ADMIN_INFO['user']
                    logged_password = ADMIN_INFO['password']
                    logged_email = ADMIN_INFO['email']
                    logged_role = ADMIN_INFO['role']
                    sg.popup('Login realizado como administrador!', title='Login ADM')
                    window.close()
                    AdmMenu()
                elif Select.user_authentication(self.values['user'], self.values['password']) == True:
                    user_info = Select.user_information(self.values['user'], self.values['password'])
                    logged_email, logged_user, logged_password, logged_role = user_info
                    sg.popup('Login realizado com sucesso!', title='Login')
                    window.close()
                    PrincipalMenu()
                else:
                    sg.popup('Usuário e/ou senha incorretos.',title='Erro')

        window.close()

#Logo popup
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Logo:
    def __init__(self):
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Image(LOGO)]
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
        Login()


AdmMenu()