import psycopg2 as ps
import pandas as pd

#Database info
#-------------------------------------------------------------------------------------------------------------------------------------------------
DATABASE = 'db_powerautomate'

HOST = '4.228.57.67'

USER = 'postgres'

PASSWORD = 'pRxI65oIubsdTlf'

#Classes
#-------------------------------------------------------------------------------------------------------------------------------------------------
class Insert:
    def __init__(self):
        pass

    def register(email, usuario, senha, cargo):
        email = ("'" + email + "'")
        usuario = ("'" + usuario + "'")
        senha = ("'" + senha + "'")
        cargo = ("'" + cargo + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''INSERT INTO sc_aplicativos.app_usuarios (email, usuario, senha, cargo)
        VALUES ({email}, {usuario}, {senha}, {cargo})
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

class Select:
    def __init__(self):
        pass

    def user_verification(user):
        user = ("'" + user + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE usuario={user}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result == None:
            return True
        else:
            return False
        
    def user_authentication(user, password):
        user = ("'" + user + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE usuario={user}
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
        
    def user_information(user, password):
        user = ("'" + user + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE usuario={user}
        AND senha={password}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        if result != None:
            logged_email, logged_user, logged_password, logged_role = result
            return logged_email, logged_user, logged_password, logged_role
        else:
            logged_email, logged_user, logged_password, logged_role = '', '', '', ''
            return logged_email, logged_user, logged_password, logged_role
        
    def user_list():
        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        '''

        cur.execute(command)
        result = cur.fetchall()
        con.commit()

        cur.close()
        con.close()

        return result
    
    def role_authentication(user, password):
        user = ("'" + user + "'")
        password = ("'" + password + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''SELECT * FROM sc_aplicativos.app_usuarios
        WHERE usuario = {user}
        AND senha = {password}
        '''

        cur.execute(command)
        result = cur.fetchone()
        con.commit()

        cur.close()
        con.close()

        role = result[3]

        return role

class Update:
    def __init__(self):
        pass

    def user_update(email, user, password, role):
        email = ("'" + email + "'")
        user = ("'" + user + "'")
        password = ("'" + password + "'")
        role = ("'" + role + "'")

        con = ps.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cur = con.cursor()

        command =f'''UPDATE sc_aplicativos.app_usuarios
        SET email = {email}, usuario = {user}, senha = {password}, cargo = {role}
        WHERE email = {email}
        '''

        cur.execute(command)
        con.commit()

        cur.close()
        con.close()

class TableColumns:
    def __init__(self):
        pass

    def table_users():
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
    
