import psycopg2 as ps
import datetime
import win32com.client as win32
import os


#Database info
#-------------------------------------------------------------------------------------------------------------------------------------------------
DATABASE = 'db_powerautomate'

HOST = '4.228.57.67'

USER = 'postgres'

PASSWORD = 'pRxI65oIubsdTlf'

INSTALLED_MODULES = [
    'Registro de turno',
]

#Classes
#-------------------------------------------------------------------------------------------------------------------------------------------------
class Insert:
    def __init__(self):
        pass

    def register(email, senha, cargo, project):
        email = ("'" + email + "'")
        senha = ("'" + senha + "'")
        cargo = ("'" + cargo + "'")
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''INSERT INTO sc_aplicativos.app_usuarios (email, senha, cargo, ultimo_login, modulos, projeto)
        VALUES ({email}, {senha}, {cargo}, NULL, NULL, {project})
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def add_project(project):
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''INSERT INTO sc_aplicativos.app_projetos (projetos)
        VALUES ({project})
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def add_tower(number, project, tower_code):
        tower_code = ("'" + tower_code + "'")
        chave = (f"'{number}-{project}'")
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        if tower_code == "'NULL'":
            command =f'''INSERT INTO sc_aplicativos.app_torres (chave, numero, projeto, codigo_torre)
            VALUES ({chave}, {number}, {project}, NULL)
            '''

        else:
            command =f'''INSERT INTO sc_aplicativos.app_torres (chave, numero, projeto, codigo_torre)
            VALUES ({chave}, {number}, {project}, {tower_code})
            '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def create_passage(data, torre, email, turno, frente, descricao, cod_torre):

        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''INSERT INTO sc_aplicativos.app_passagens (chave, torre, email, turno, frente, descricao, enviado, cod_torre, data_envio, data_criacao)
        VALUES ('{data}-{cod_torre}-{turno}', {torre}, '{email}', '{turno}', '{frente}', '{descricao}', false, '{cod_torre}', NULL, '{now}')
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

class Select:
    def __init__(self):
        pass
        
    def login_authentication(email, password):
        email = ("'" + email + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE email={email}
        AND senha={password}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result != None:
            return True
        else:
            return False
        
    def user_information(email, password):
        email = ("'" + email + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT email, senha, cargo, ultimo_login, projeto FROM sc_aplicativos.app_usuarios
        WHERE email={email}
        AND senha={password}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result != None:
            logged_email, logged_password, logged_role, last_login, logged_project = result
            return logged_email, logged_password, logged_role, last_login, logged_project
        else:
            logged_email, logged_password, logged_role, last_login, logged_project = '', '', '', '', ''
            return logged_email, logged_password, logged_role, last_login, logged_project
        
    def user_list():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT email, senha, cargo, ultimo_login, projeto FROM sc_aplicativos.app_usuarios
        ORDER BY email ASC
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        return result
    
    def role_authentication(email, password):
        email = ("'" + email + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE email = {email}
        AND senha = {password}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        role = result[2]

        return role
    
    def email_authentication(email):
        email = ("'" + email + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE email = {email}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result != None:
            return True
        else:
            return False
        
    def modules_information(email):
        email = ("'" + email + "'")
        
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT modulos
        FROM sc_aplicativos.app_usuarios
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        result = cur.fetchone()

        cur.close()
        con.close()
        
        try:
            lista = [str(item) for sublist in result for item in sublist]
            return lista
        except:
            return []
        
    def projects_list():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_projetos
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        return result
    
    def towers_list():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT numero, projeto, codigo_torre FROM sc_aplicativos.app_torres
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        return result
    
    def tower_authentication(chave):
        chave = ("'" + chave + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_torres
        WHERE chave={chave}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result != None:
            return True
        else:
            return False
        
    def search_tower_number(number):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT numero, projeto, codigo_torre FROM sc_aplicativos.app_torres
        WHERE CAST(numero as Text) LIKE '%{number}%'
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('','Sem resultados','')]
            return result
        else:
            return result
        
    def search_tower_code(code):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT numero, projeto, codigo_torre FROM sc_aplicativos.app_torres
        WHERE codigo_torre LIKE '%{code}%'
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('','Sem resultados','')]
            return result
        else:
            return result
        
    def search_tower_code_and_number(code, number):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT numero, projeto, codigo_torre FROM sc_aplicativos.app_torres
        WHERE codigo_torre LIKE '%{code}%' AND
        CAST(numero as Text) LIKE '%{number}%'
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('','Sem resultados','')]
            return result
        else:
            return result
        
    def passages_list(cod_torre):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT chave, email, turno, frente, enviado, data_envio, data_criacao FROM sc_aplicativos.app_passagens
        WHERE cod_torre = '{cod_torre}'
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('','','','Sem passagens','','','')]
            return result
        else:
            return result
        
    def edit_passage(chave):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_passagens
        WHERE chave = '{chave}'
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('')]
            return result
        else:
            return result
        
    def date_search(cod_torre, date, sent):
        date = (f"{date.split('/')[2]}-{date.split('/')[1]}-{date.split('/')[0]}")

        if sent == 'Não':
            sent = 'False'

            command =f'''SELECT chave, email, turno, frente, enviado, data_envio, data_criacao FROM sc_aplicativos.app_passagens
            WHERE cod_torre = '{cod_torre}' AND
            data_criacao BETWEEN '{date} 00:00:00' AND '{date} 23:59:59' AND
            enviado = '{sent}'
            '''
        elif sent == 'Sim':
            sent = 'True'

            command =f'''SELECT chave, email, turno, frente, enviado, data_envio, data_criacao FROM sc_aplicativos.app_passagens
            WHERE cod_torre = '{cod_torre}' AND
            data_criacao BETWEEN '{date} 00:00:00' AND '{date} 23:59:59' AND
            enviado = '{sent}'
            '''

        elif sent == 'Todos':
            command =f'''SELECT chave, email, turno, frente, enviado, data_envio, data_criacao FROM sc_aplicativos.app_passagens
            WHERE cod_torre = '{cod_torre}' AND
            data_criacao BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
            '''

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        if result == []:
            result = [('','','','Sem passagens','','','')]
            return result
        else:
            return result
        
class Update:
    def __init__(self):
        pass

    def user_update(email, password, role, project):
        email = ("'" + email + "'")
        password = ("'" + password + "'")
        role = ("'" + role + "'")
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET senha = {password}, cargo = {role}, projeto = {project}
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def last_login(email):
        email = ("'" + email + "'")

        hour = datetime.datetime.now()
        hour = str(hour)
        input_hour = hour.split('.')[0]
        input_hour = ("'" + input_hour + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET ultimo_login = {input_hour}
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def modules_update(email, modules_list):
        email = ("'" + email + "'")
        array = f"ARRAY{modules_list}"
        
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET modulos = {array}
        WHERE email = {email}
        '''

        command2 =f'''UPDATE sc_aplicativos.app_usuarios
        SET modulos = Null
        WHERE email = {email}
        '''

        if modules_list == []:
            cur.execute(command2)
        else:
            cur.execute(command)

        con.commit()

        cur.close()
        con.close()

    def role_project_update(email, role, project):
        email = ("'" + email + "'")
        role = ("'" + role + "'")
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET cargo = {role}, projeto = {project}
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def desc_update(chave, desc):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_passagens
        SET descricao = '{desc}'
        WHERE chave = '{chave}'
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def sent_update(chave):
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        data = datetime.datetime.today()
        data = str(data)
        data = data.split('.')[0]

        command =f'''UPDATE sc_aplicativos.app_passagens
        SET enviado = true, data_envio = '{data}'
        WHERE chave = '{chave}'
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

class TableColumns:
    def __init__(self):
        pass

    def columns_users():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'app_usuarios'
        ORDER BY ordinal_position;
        '''

        cur.execute(command)
        con.commit()

        result = cur.fetchall()

        column_names = [row[0] for row in result]

        cur.close()
        con.close()

        return column_names[0]

class Delete:
    def __init__(self):
        pass

    def delete_user(email):
        email = ("'" + email + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''DELETE FROM sc_aplicativos.app_usuarios
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def delete_project(project):
        project = ("'" + project + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''DELETE FROM sc_aplicativos.app_projetos
        WHERE projetos = {project}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

    def delete_tower(tower, project):
        chave = f"'{tower}-{project}'"

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''DELETE FROM sc_aplicativos.app_torres
        WHERE chave = {chave}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

class Functions:
    def check_date_format(date):
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            return True
            
        except ValueError:
            return False

class Email:
    def email_passage(receivers, desc_passage, file_path, turn, project, user_email, tower):
        today = datetime.date.today()
        today = str(today)
        today = (f"{today.split('-')[2]}/{today.split('-')[1]}/{today.split('-')[0]}")

        # construct Outlook application instance
        olApp = win32.Dispatch('Outlook.Application')
        olNS = olApp.GetNameSpace('MAPI')

        # construct the email item object
        mailItem = olApp.CreateItem(0)
        mailItem.Subject = f'Passagem de turno {turn} - Projeto {project} - Torre {tower} - {today}'
        mailItem.BodyFormat = 1
        mailItem.Body = f'''\n{desc_passage}

Responsável pela passagem de turno: {user_email}
        '''
        mailItem.To = ', '.join(receivers)

        for attachment in file_path:
            if file_path == '':
                pass
            else:
                mailItem.Attachments.Add(os.path.join(os.getcwd(), attachment))

        mailItem.Display()

        mailItem.Save()
        mailItem.Send()

