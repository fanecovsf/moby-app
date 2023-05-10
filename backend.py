import psycopg2 as ps
import datetime

#Database info
#-------------------------------------------------------------------------------------------------------------------------------------------------
DATABASE = 'db_powerautomate'

HOST = '4.228.57.67'

USER = 'postgres'

PASSWORD = 'pRxI65oIubsdTlf'

INSTALLED_MODULES = [
    'Passagem de turno',
]

#Classes
#-------------------------------------------------------------------------------------------------------------------------------------------------
class Insert:
    def __init__(self):
        pass

    def register(email, senha, cargo):
        email = ("'" + email + "'")
        senha = ("'" + senha + "'")
        cargo = ("'" + cargo + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''INSERT INTO sc_aplicativos.app_usuarios (email, senha, cargo)
        VALUES ({email}, {senha}, {cargo})
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
            logged_email, logged_password, logged_role, last_login = result[:4]
            return logged_email, logged_password, logged_role, last_login
        else:
            logged_email, logged_password, logged_role, last_login = '', '', '', ''
            return logged_email, logged_password, logged_role, last_login
        
    def user_list():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT email, senha, cargo, ultimo_login FROM sc_aplicativos.app_usuarios
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
        
class Update:
    def __init__(self):
        pass

    def user_update(email, password, role):
        email = ("'" + email + "'")
        password = ("'" + password + "'")
        role = ("'" + role + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET senha = {password}, cargo = {role}
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
