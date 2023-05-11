import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PySimpleGUI as sg
from backend import Insert, Select, Update, Delete, INSTALLED_MODULES


#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE_NAME = 'Registro de turno'

APP_NAME = 'Moby'

THEME = 'DarkTeal12'

STATIC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\Static'

ICON = STATIC_PATH + '\Símbolo.ico'

LOGO = STATIC_PATH + '\logo.png'

#Telas
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Lista de torres
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class TowerList:
    def __init__(self):
        df = pd.DataFrame(Select.towers_list(), columns=['Número', 'Projeto', 'Código da torre'])
        df = df.loc[df['Projeto'] == logged_project]

        data = df.values.tolist()
        header_list = list(df.columns)

        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Table(data, headings=header_list, num_rows=20, auto_size_columns=False, enable_events=True, justification='center', key='-TABLE-', max_col_width=45, def_col_width=20)],
            [sg.Push(),sg.Button('Voltar ao menu',size=(15,0)),sg.Button('Lista de passagens',size=(15,0)),sg.Push()]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON, resizable=True)

        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED or event == 'Voltar ao menu':
                window.close()
                break
        

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
