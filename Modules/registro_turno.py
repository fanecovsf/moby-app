import os
import sys
import pandas as pd
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PySimpleGUI as sg
from backend import Insert, Select, Update, Delete, Functions, Email


#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE_NAME = 'Registro de turno'

APP_NAME = 'Moby'

THEME = 'DarkTeal12'

STATIC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\Static'

ICON = STATIC_PATH + '\Símbolo.ico'

LOGO = STATIC_PATH + '\logo.png'

FRONTS = [
    'Safety',
    'Inbound',
    'Outbound'
]

TURNS = [
    'A',
    'B',
    'C',
    'ADM'
]

#Telas
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Criação de passagem
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PassageCreate:
    def __init__(self, torre):
        num_torre = torre.split('-')[0]

        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Text('Torre:', size=(20,0)), sg.Text(num_torre, size=(30,0),key='-TOWER-')],
            [sg.Text('Responsável:', size=(20,0)), sg.Text(logged_email,size=(30,0),key='-EMAIL-')],
            [sg.Text('Turno:', size=(20,0)), sg.Combo(TURNS,readonly=True,size=(30,0),key='-TURNO-')],
            [sg.Text('Frente:', size=(20,0)), sg.Combo(FRONTS, readonly=True, size=(30,0), key='-FRONT-')],
            [sg.Text('Descrição:', size=(20,0))],
            [sg.Multiline(size=(70,30), key='-DESC-')],
            [sg.Push() ,sg.Button('Cancelar', size=(15,0)), sg.Button('Salvar', size=(15,0)), sg.Push()]
        ]

        #Janela
        window = sg.Window(MODULE_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancelar':
                window.close()
                break

            elif event == 'Salvar':
                if self.values['-TURNO-'] == '' \
                or self.values['-FRONT-'] == '' \
                or self.values['-DESC-'] == '':
                    sg.popup('Preencha todos os campos.', title='Erro', icon=ICON)

                else:
                    try:
                        data = datetime.date.today()
                        data = str(data)
                        data = f"{data.split('-')[2]}-{data.split('-')[1]}-{data.split('-')[0]}"

                        Insert.create_passage(data, num_torre, logged_email, self.values['-TURNO-'], self.values['-FRONT-'], self.values['-DESC-'], torre)

                        sg.popup('Registro de turno criado!', title='Ciração', icon=ICON)

                        window.close()
                        break

                    except:
                        sg.popup('Já existe um registro de turno dessa torre para hoje no mesmo turno.', title='Erro', icon=ICON)

#Descrição da passagem
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Edit:
    def __init__(self, chave):
        torre = Select.edit_passage(chave)[1]
        email = Select.edit_passage(chave)[2]
        turno = Select.edit_passage(chave)[3]
        frente = Select.edit_passage(chave)[4]
        descricao = Select.edit_passage(chave)[5]
        data_envio = Select.edit_passage(chave)[8]
        enviado = Select.edit_passage(chave)[6]

        if enviado == False:
            enviado = 'Não'
        else:
            enviado = 'Sim'

        sg.theme(THEME)

        #Layout
        layout_view = [
            [sg.Text('Torre:', size=(20,0)), sg.Text(torre, size=(30,0),key='-TOWER-')],
            [sg.Text('Responsável:', size=(20,0)), sg.Text(email,size=(30,0),key='-EMAIL-')],
            [sg.Text('Turno:', size=(20,0)), sg.Text(turno,size=(30,0),key='-TURNO-')],
            [sg.Text('Frente:', size=(20,0)), sg.Text(frente, size=(30,0), key='-FRONT-')],
            [sg.Text('Data de envio:', size=(20,0)), sg.Text(data_envio, size=(30,0), key='-FRONT-')],
            [sg.Text('Enviado:', size=(20,0)), sg.Text(enviado, size=(30,0), key='-FRONT-')],
            [sg.Text('Descrição:')],
            [sg.Text(descricao, key='-DESC-')],   
            [sg.Push() ,sg.Button('Sair', size=(15,0)), sg.Push()]
        ]

        layout_edit = [
            [sg.Text('Torre:', size=(20,0)), sg.Text(torre, size=(30,0),key='-TOWER-')],
            [sg.Text('Responsável:', size=(20,0)), sg.Text(email,size=(30,0),key='-EMAIL-')],
            [sg.Text('Turno:', size=(20,0)), sg.Text(turno,size=(30,0),key='-TURNO-')],
            [sg.Text('Frente:', size=(20,0)), sg.Text(frente, size=(30,0), key='-FRONT-')],
            [sg.Text('Data de envio:', size=(20,0)), sg.Text(data_envio, size=(30,0), key='-FRONT-')],
            [sg.Text('Enviado:', size=(20,0)), sg.Text(enviado, size=(30,0), key='-FRONT-')],
            [sg.Text('Descrição:', size=(20,0))],
            [sg.Multiline(descricao,size=(70,30), key='-DESC-')],
            [sg.Text('Lista de emails para envio da passagem:', pad=(10,10))],
            [sg.Text('Email 1:'), sg.Input(size=(40,0), key='-EMAIL1-'),sg.Push(), sg.FileBrowse('Anexar arquivo ao email',target='-PATH1-')],
            [sg.Text('Email 2:'), sg.Input(size=(40,0), key='-EMAIL2-'),sg.Push(), sg.Input(key='-PATH1-', readonly=True, size=(10,0))],
            [sg.Text('Email 3:'), sg.Input(size=(40,0), key='-EMAIL3-'),sg.Push(), sg.FileBrowse('Anexar arquivo ao email',target='-PATH2-')],
            [sg.Text('Email 4:'), sg.Input(size=(40,0), key='-EMAIL4-'),sg.Push(), sg.Input(key='-PATH2-', readonly=True, size=(10,0))],
            [sg.Text('Email 5:'), sg.Input(size=(40,0), key='-EMAIL5-'),sg.Push(), sg.FileBrowse('Anexar arquivo ao email',target='-PATH3-')],
            [sg.Text('Email 6:'), sg.Input(size=(40,0), key='-EMAIL6-'),sg.Push(), sg.Input(key='-PATH3-', readonly=True, size=(10,0))],
            [sg.Push() ,sg.Button('Sair', size=(15,0)), sg.Button('Salvar', size=(15,0)),sg.Button('Enviar', size=(15,0)), sg.Push()]
        ]

        #Janela
        if enviado == 'Sim':
            window = sg.Window(MODULE_NAME, layout_view, icon=ICON)

        elif enviado == 'Não':
            if logged_email != email:
                if logged_role == 'Gestor' or logged_role == 'Líder' or logged_role == 'Desenvolvedor':
                    window = sg.Window(MODULE_NAME, layout_edit, icon=ICON)
                else:
                    sg.popup('Registros não enviados só podem ser abertos pelos seus responsáveis, aguarde o envio do mesmo.', title='Erro', icon=ICON)
            else:
                window = sg.Window(MODULE_NAME, layout_edit, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Sair':
                window.close()
                break

            elif event == 'Salvar':
                Update.desc_update(chave, self.values['-DESC-'])
                sg.popup('Informações salvas com sucesso!', title='Salvo', icon=ICON)
                window.close()
                break

            elif event == 'Enviar':
                ch = sg.popup_ok_cancel('Deseja realmente enviar o registro? O mesmo não poderá ser editado após o envio.', title='Confirmação', icon=ICON)

                if ch == 'OK':
                    try:
                        Update.sent_update(chave)

                        receivers = []
                        attach = []

                        for i in range(1, 7):
                            email_key = f'-EMAIL{i}-'
                            if self.values[email_key]:
                                receivers.append(self.values[email_key])

                        for i in range(1, 4):
                            path_key = f'-PATH{i}-'
                            if self.values[path_key]:
                                attach.append(self.values[path_key])

                        if receivers:
                            Email.email_passage(receivers, descricao, attach, turno, logged_project, logged_email, torre)

                        window.close()
                        break
                    except Exception as e:
                        print(e)

                elif ch == 'Cancel':
                    pass

#Passagens
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Passages:
    def __init__(self, cod_torre):
        num_torre = cod_torre.split('-')[0]
        df = pd.DataFrame(Select.passages_list(cod_torre), columns=['Chave', 'Responsável', 'Turno', 'Frente', 'Enviado', 'Data de envio'])
        df['Enviado'] = df['Enviado'].apply(lambda x: '' if x == '' else 'Não' if x == False else 'Sim')
        df['Data de envio'] = df['Data de envio'].apply(lambda x: '' if x == None else x)
        df = df.sort_values('Data de envio', ascending=False)
        data = df.values.tolist()
        header_list = list(df.columns)

        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text(f'Registros - Torre {num_torre}', font=('Arial', 18, 'bold')), sg.Push()],
            [sg.Input(key='-IN-', size=(10,0), pad=(10,0)),sg.CalendarButton('📆', target='-IN-', format='%d/%m/%Y',default_date_m_d_y=(1,None,2023), key='calendar', font=('Arial', 16)),sg.Button('Pesquisar 🔍')],
            [sg.Table(data, headings=header_list, num_rows=40, auto_size_columns=False, enable_events=True, justification='center', key='-TABLE-', max_col_width=40, def_col_width=20)],
            [sg.Push(),sg.Button('Sair',size=(15,0)),sg.Button('Abrir',size=(15,0)),sg.Button('Criar registro',size=(15,0)),sg.Push()]
        ]

        #Janela
        window = sg.Window(MODULE_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Sair':
                window.close()
                break

            elif event == 'Abrir':
                try:
                    row_index = self.values['-TABLE-'][0]
                    selected_data = list(df.iloc[row_index])
                    Edit(selected_data[0])
                    df = pd.DataFrame(Select.passages_list(cod_torre), columns=['Chave', 'Responsável', 'Turno', 'Frente', 'Enviado', 'Data de envio'])
                    df['Enviado'] = df['Enviado'].apply(lambda x: '' if x == '' else 'Não' if x == False else 'Sim')
                    df['Data de envio'] = df['Data de envio'].apply(lambda x: '' if x == None else x)
                    df = df.sort_values('Data de envio', ascending=False)
                    window['-TABLE-'].update(df.values.tolist())
                except:
                    pass

            elif event == 'Pesquisar 🔍':
                if Functions.check_date_format(self.values['-IN-']) == False:
                    sg.popup('Digite ou selecione uma data válida.', title='Erro', icon=ICON)

                else:
                    try:
                        df = pd.DataFrame(Select.date_search(cod_torre, self.values['-IN-']), columns=['Chave', 'Responsável', 'Turno', 'Frente', 'Enviado', 'Data de envio'])
                        df['Enviado'] = df['Enviado'].apply(lambda x: '' if x == '' else 'Não' if x == False else 'Sim')
                        df['Data de envio'] = df['Data de envio'].apply(lambda x: '' if x == None else x)
                        df = df.sort_values('Data de envio', ascending=False)
                        window['-TABLE-'].update(df.values.tolist())

                    except:
                        sg.popup('Erro', title='Erro', icon=ICON)

            elif event == 'Criar registro':
                PassageCreate(cod_torre)
                df = pd.DataFrame(Select.passages_list(cod_torre), columns=['Chave', 'Responsável', 'Turno', 'Frente', 'Enviado', 'Data de envio'])
                df['Enviado'] = df['Enviado'].apply(lambda x: '' if x == '' else 'Não' if x == False else 'Sim')
                df['Data de envio'] = df['Data de envio'].apply(lambda x: '' if x == None else x)
                df = df.sort_values('Data de envio', ascending=False)
                window['-TABLE-'].update(df.values.tolist())

#Lista de torres
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class TowerList:
    def __init__(self):
        if logged_role == 'Desenvolvedor':
            df = pd.DataFrame(Select.towers_list(), columns=['Número', 'Projeto', 'Código da torre'])
        else:
            df = pd.DataFrame(Select.towers_list(), columns=['Número', 'Projeto', 'Código da torre'])
            df = df.loc[df['Projeto'] == logged_project]

        data = df.values.tolist()
        header_list = list(df.columns)

        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Push(), sg.Text(f'Torres - Projeto {logged_project}', font=('Arial', 18, 'bold')), sg.Push()],
            [sg.Text('Pesquisa por número:'),sg.Input(size=(10,0), key='search_number'),sg.Push(),sg.Text('Pesquisa por código da torre:'),sg.Input(size=(17,0), pad=(0,20),key='search_code')],
            [sg.Table(data, headings=header_list, num_rows=20, auto_size_columns=False, enable_events=True, justification='center', key='-TABLE-', max_col_width=45, def_col_width=20)],
            [sg.Push(),sg.Button('Voltar ao menu',size=(15,0)),sg.Button('Lista de passagens',size=(15,0)),sg.Push(),sg.Button('Pesquisar 🔍')]
        ]

        #Janela
        window = sg.Window(MODULE_NAME, layout, icon=ICON, resizable=True)

        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Voltar ao menu':
                window.close()
                break

            elif event == 'Lista de passagens':
                try:
                    row_index = self.values['-TABLE-'][0]
                    selected_data = list(df.iloc[row_index])
                    cod_torre = f'{selected_data[0]}-{selected_data[1]}'
                    Passages(cod_torre)
                except Exception as e:
                    pass

            elif event == 'Pesquisar 🔍':
                code = self.values['search_code']
                number = self.values['search_number']

                if code == '' and number == '':
                    df = pd.DataFrame(Select.towers_list(), columns=['Número', 'Projeto', 'Código da torre'])
                    df = df.loc[df['Projeto'] == logged_project]
                    window['-TABLE-'].update(df.values.tolist())
                    pass

                elif code != '' and number == '':
                    df = pd.DataFrame(Select.search_tower_code(code), columns=['Número', 'Projeto', 'Código da torre'])
                    df = df.loc[df['Projeto'] == logged_project]
                    window['-TABLE-'].update(df.values.tolist())

                elif code == '' and number != '':
                    df = pd.DataFrame(Select.search_tower_number(number), columns=['Número', 'Projeto', 'Código da torre'])
                    df = df.loc[df['Projeto'] == logged_project]
                    window['-TABLE-'].update(df.values.tolist())

                elif code != '' and number != '':
                    df = pd.DataFrame(Select.search_tower_code_and_number(code, number), columns=['Número', 'Projeto', 'Código da torre'])
                    df = df.loc[df['Projeto'] == logged_project]
                    window['-TABLE-'].update(df.values.tolist())

#Start engine
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class StartPassagemTurno:
    def __init__(self, email, password):
        global logged_email
        global logged_password
        global logged_role
        global last_login
        global logged_project

        logged_email, logged_password, logged_role, last_login, logged_project = Select.user_information(email, password)
        TowerList()
