import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PySimpleGUI as sg
from backend import Insert, Select, Update, Delete, INSTALLED_MODULES


#Configurações
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE_NAME = 'Passagem de turno'

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
        sg.theme(THEME)

        #Layout
        layout = [
            [sg.Text('Tela de passagem de turno')]
        ]

        #Janela
        window = sg.Window(APP_NAME, layout, icon=ICON)

        #Loop
        while True:
            event, self.values = window.read()

            if event == sg.WIN_CLOSED:
                break
        

#Start engine
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class StartPassagemTurno:
    def __init__(self):
        TowerList()
