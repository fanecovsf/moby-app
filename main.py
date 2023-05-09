import PySimpleGUI as sg
from backend import Insert, Select, Update, Delete
import pandas as pd

#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
DEVELOPER_MODE = True

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
    'Supervisor',
    'Gestor'
]

THEME = 'DarkTeal12'

VERSION = 'Versão 0.1'

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
        df = pd.DataFrame(Select.user_list(), columns=['E-mail','Senha','Cargo'])
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

            if event == 'Voltar ao menu':
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

                    if selected_data[0] != ADMIN_INFO['email']:

                        edit_layout = [
                            [sg.Text('E-mail:'), sg.InputText(selected_data[0], key='-EMAIL-', readonly=True)],
                            [sg.Text('Senha:'), sg.InputText(selected_data[1], key='-SENHA-')],
                            [sg.Text('Cargo:'), sg.InputCombo(CARGOS, selected_data[2], key='-CARGO-')],
                            [sg.Button('Salvar'), sg.Button('Cancelar')]
                        ]

                        edit_window = sg.Window(APP_NAME, edit_layout, icon=ICON)

                        while True:
                            edit_event, edit_values = edit_window.read()

                            if edit_event == sg.WIN_CLOSED or edit_event == 'Cancelar':
                                edit_window.close()
                                break
                            
                            #Ajustar
                            elif edit_event == 'Salvar':
                                df.iloc[row_index] = [edit_values['-EMAIL-'], edit_values['-SENHA-'], edit_values['-CARGO-']]

                                if selected_data[1] != edit_values['-SENHA-'] or selected_data[2] != edit_values['-CARGO-']:
                                    window['-TABLE-'].update(df.values.tolist())
                                    Update.user_update(edit_values['-EMAIL-'], edit_values['-SENHA-'], edit_values['-CARGO-'])
                                    sg.popup('Informações atualizadas com sucesso!', title='Edição de usuário', icon=ICON)
                                    edit_window.close()

                                else:
                                    edit_window.close() 

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
            [sg.Push(), sg.Text('Email:',pad=(10,10)), sg.Input(size=(30,0), key='email'), sg.Push()],
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

            if event == sg.WIN_CLOSED or event == 'Sair':
                break

            elif event == 'Registro de usuário':
                AdminLogin(['Gestor', 'Supervisor', 'Desenvolvedor'], Register)

            elif event == 'Login':
                if self.values['email'] == ADMIN_INFO['email'] and self.values['password'] == ADMIN_INFO['password']:
                    logged_password = ADMIN_INFO['password']
                    logged_email = ADMIN_INFO['email']
                    logged_role = ADMIN_INFO['role']
                    sg.popup('Login realizado como administrador!', title='Login ADM', icon=ICON)
                    window.close()
                    AdmMenu()
                elif Select.login_authentication(self.values['email'], self.values['password']) == True:
                    user_info = Select.user_information(self.values['email'], self.values['password'])
                    logged_email, logged_password, logged_role = user_info
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
        if Select.login_authentication(ADMIN_INFO['email'], ADMIN_INFO['password']) == True:
            Login()
        else:
            sg.popup('Ops! Parece que há divergências entre as informações de administrador no banco de dados, por favor corrija antes de iniciar o aplicativo.', title='Erro', icon=ICON)


Start()