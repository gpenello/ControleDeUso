import sqlite3
from sqlite3 import Error
import datetime
import csv
import urllib.request as urllib2

import os
dir_path = os.path.dirname(os.path.realpath(__file__))



class BancoDeDados():

    def __init__(self, arquivo):
        
        try:
            os.makedirs(os.path.join(dir_path, 'log'))
        except FileExistsError:
            # directory already exists
            pass

        self.conn = self.create_connection(arquivo)
            
        if self.rpi_online():
            self.hora_inicio = str(datetime.datetime.now())[:-7]
        else:
            self.hora_inicio = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]


    def rpi_online(self):
        try:
            urllib2.urlopen('http://www.google.com', timeout=1)
            return True
        except urllib2.URLError:
            return False
            

    def fechar_conn(self):
        self.conn.close()

    def create_table_admin(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY " +\
            "KEY, tag TEXT, login TEXT, nome TEXT UNIQUE, email TEXT, " +\
            "senha TEXT)"
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)        

    def create_table_variaveis(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS variaveis(id INTEGER PRIMARY " +\
            "KEY, variavel TEXT UNIQUE, valor TEXT UNIQUE)"
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)        

    def create_table_usuarios(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY " +\
            "KEY, tag TEXT UNIQUE, login TEXT UNIQUE, nome TEXT UNIQUE, email TEXT, adicionado_por TEXT, " +\
            "permissao TEXT, senha TEXT, grupo TEXT)"
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)


    def create_table_usuarios_antigos(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS usuarios_antigos(id INTEGER PRIMARY " +\
            "KEY, tag TEXT UNIQUE, login TEXT UNIQUE, nome TEXT UNIQUE, email TEXT, adicionado_por TEXT, " +\
            "permissao TEXT, senha TEXT, grupo TEXT)"
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)


    def create_table_autorizacao_equip(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS autorizacao_equip(id INTEGER
                PRIMARY KEY, equipamento TEXT, login TEXT, nome TEXT, super TEXT,
                UNIQUE(login, equipamento))'''
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_table_presenca(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS presenca(id INTEGER
                PRIMARY KEY, login TEXT, nome TEXT, tag TEXT, hora_entrada TEXT,
                 hora_saida TEXT)'''
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_table_uso_equip(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS uso_equip(id INTEGER PRIMARY
            KEY, login TEXT, nome TEXT, equipamento TEXT, hora_inicio TEXT, hora_fim TEXT,
            tempo_total TEXT, comentario TEXT, situacao Text)'''
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_connection(self, arquivo):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(arquivo)
            if self.conn is not None:
                self.create_table_usuarios()  # criando tabela usuarios
                self.create_table_usuarios_antigos()  # criando tabela usuarios antigos
                self.create_table_admin()
                self.create_table_variaveis()
                self.create_table_autorizacao_equip()  # tabela de autorizacoes
                # criando controle de uso de equip.
                self.create_table_uso_equip()
                self.create_table_presenca()
                self.create_csv_files()

                # password = cript.hash_password(password)
                # self.add_novo_admin("sem tag", "admin", "Administrador-Germano", "gpenello@gmail.com", password)

            else:
                print("Error! cannot create the database connection.")
            return self.conn
        except Error as e:
            print(e)
        return None

    def create_csv_files(self):
        try:
            open(os.path.join(dir_path, 'log/tabela_uso_equip.csv'), 'r')
        except IOError:
            with open(
                    os.path.join(dir_path, 'log/tabela_uso_equip.csv'),
                    'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow([
                    "id", "login", "nome", "equipamento", "hora_inicio", "hora_fim",
                    "tempo_total", "comentário", "situação"
                ])
        try:
            open(os.path.join(dir_path, 'log/tabela_presenca.csv'), 'r')
        except IOError:
            with open(os.path.join(dir_path, 'log/tabela_presenca.csv'),
                      'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow(
                    ["id", "login","nome", "tag", "hora_entrada", "hora_saida"])
        try:
            open(os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),'r')
        except IOError:
            with open(
                    os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),
                    'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow(["id", "equipamento", "login", "nome", "super"])
        try:
            open(os.path.join(dir_path, 'log/tabela_usuarios.csv'), 'r')
        except IOError:
            with open(os.path.join(dir_path, 'log/tabela_usuarios.csv'),
                      'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow([
                    "id", "tag", "login", "nome", "email", "adicionado_por",
                    "permissao", "senha", "grupo/orientador"
                ])
        try:
            open(os.path.join(dir_path, 'log/tabela_usuarios_antigos.csv'), 'r')
        except IOError:
            with open(os.path.join(dir_path, 'log/tabela_usuarios_antigos.csv'),
                      'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow([
                    "id", "tag", "login", "nome", "email", "adicionado_por",
                    "permissao", "senha", "grupo/orientador"
                ])

    def check_tabela_presenca(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM presenca")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)


    def check_tabela_variaveis(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM variaveis")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def check_tabela_usuarios(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM usuarios")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)


    def check_tabela_usuarios_antigos(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM usuarios_antigos")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

#    def check_lista_usuarios(self):
    def check_lista_nomes_usuarios(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM usuarios")
            rows = cur.fetchall()
            return [item[0] for item in rows]
        except Error as e:
            print(e)

    def check_lista_logins_usuarios(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT login FROM usuarios")
            rows = cur.fetchall()
            return [item[0] for item in rows]
        except Error as e:
            print(e)

    def check_tabela_autorizacao_equip(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM autorizacao_equip")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def check_tabela_uso_equip(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM uso_equip")
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def export_all_db_to_csv(self):
        tabela_uso_equip = self.check_tabela_uso_equip()
        tabela_autorizacao_equip = self.check_tabela_autorizacao_equip()
        tabela_usuarios = self.check_tabela_usuarios()
        tabela_usuarios_antigos = self.check_tabela_usuarios_antigos()
        tabela_presenca = self.check_tabela_presenca()

        with open(os.path.join(dir_path, 'log/tabela_uso_equip.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow([
                "id", "login", "nome", "equipamento", "hora_inicio", "hora_fim",
                "tempo_total", "comentario", "situacao"
            ])
            for row in tabela_uso_equip:
                spamwriter.writerow(row)

        with open(
                os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),
                'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow(["id", "equipamento", "login", "nome", "super"])
            for row in tabela_autorizacao_equip:
                spamwriter.writerow(row)

        with open(os.path.join(dir_path, 'log/tabela_usuarios.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow([
                "id", "tag", "login", "nome", "email", "adicionado_por", "permissao",
                "senha", "grupo/orientador"
            ])
            for row in tabela_usuarios:
                spamwriter.writerow(row)

        with open(os.path.join(dir_path, 'log/tabela_usuarios_antigos.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow([
                "id", "tag", "login", "nome", "email", "adicionado_por", "permissao",
                "senha", "grupo/orientador"
            ])
            for row in tabela_usuarios_antigos:
                spamwriter.writerow(row)


        with open(os.path.join(dir_path, 'log/tabela_presenca.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow(
                ["id", "login", "nome", "tag", "hora_entrada", "hora_saida"])
            for row in tabela_presenca:
                spamwriter.writerow(row)


    def add_novo_admin(self,nome,email,password):
        try:
            sql = "INSERT INTO admin(tag, login, nome, email, senha) VALUES(?,?,?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, ("sem tag", "admin", nome, email, password))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def add_variavel(self,variavel_txt, valor):
        try:
            sql = "INSERT INTO variaveis(variavel, valor) VALUES(?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (variavel_txt, valor))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False




    def add_novo_usuario(self,
                         tag_novo,
                         login,
                         nome,
                         email,
                         password,
                         tag_autorizacao,
                         grupo,
                         permissao='apenas uso'):
        try:
            sql = "INSERT INTO usuarios(tag, login, nome, email, senha ,adicionado_por, permissao, grupo) VALUES(?,?,?,?,?,?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (tag_novo, login, nome, email, password, tag_autorizacao,
                              permissao, grupo))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def usuario_aposentado(self,
                         tag_novo,
                         login,
                         nome,
                         email,
                         password,
                         tag_autorizacao,
                         grupo,
                         permissao):
        try:
            sql = "INSERT INTO usuarios_antigos(tag, login, nome, email, senha ,adicionado_por, permissao, grupo) VALUES(?,?,?,?,?,?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (tag_novo, login, nome, email, password, tag_autorizacao,
                              permissao, grupo))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def remove_usuario_para_recadastro(self, login):
        try:
            sql = 'DELETE FROM usuarios WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (login, ))
            sql = 'DELETE FROM autorizacao_equip WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (login, ))
            self.conn.commit()
        except Error as e:
            print(e)


    def remove_usuario_por_login(self, login):
                
        dados = self.check_usuario(login)
        idx, tag, login, nome, email, add_por, permissao, senha, grupo = dados
        
        try:
            self.usuario_aposentado(tag,login,nome,email,senha,add_por,grupo,permissao)
            sql = 'DELETE FROM usuarios WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (login, ))
            sql = 'DELETE FROM autorizacao_equip WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (login, ))
            self.conn.commit()
        except Error as e:
            print(e)

    #
    # def check_usuario(self, tag_ou_nome):
    #     try:
    #         cur = self.conn.cursor()
    #         cur.execute("SELECT * FROM usuarios WHERE nome=?", (tag_ou_nome, ))
    #         row = cur.fetchall()
    #         if row == []:
    #             cur = self.conn.cursor()
    #             cur.execute("SELECT * FROM usuarios WHERE tag=?",
    #                         (tag_ou_nome, ))
    #             row = cur.fetchall()
    #         return row
    #     except Error as e:
    #         print(e)

    def check_variavel(self, variavel_txt):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT valor FROM variaveis WHERE variavel=?", (variavel_txt, ))
            row = cur.fetchall()
            if row == []:
                return row
            return row[0][0]
        except Error as e:
            print(e)

    def check_admin(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM admin WHERE login='admin'")
            row = cur.fetchall()
            if row == []:
                return row
            return [item for item in row[0]]
        except Error as e:
            print(e)

    def check_usuario(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE login=?", (login, ))
            row = cur.fetchall()
            if row == []:
                return row
            return [item for item in row[0]]
        except Error as e:
            print(e)

    def check_senha(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT senha FROM usuarios WHERE login=?", (login, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows][0]
        except Error as e:
            print(e)

    def set_senha(self, login, senha):
        try:
            sql = "UPDATE usuarios SET senha = ? WHERE login = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (senha, login))
            self.conn.commit()
        except Error as e:
            print(e)

    def set_tag(self, login, tag):
        try:
            sql = "UPDATE usuarios SET tag = ? WHERE login = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (tag, login))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return e

    def remove_tag(self, login):
        try:
            sql = "UPDATE usuarios SET tag = ? WHERE login = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (None, login))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_permissao(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT permissao FROM usuarios WHERE login=?",
                        (login, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows][0]
        except Error as e:
            print(e)

    def set_permissao(self, login):
        try:
            sql = "UPDATE usuarios SET permissao = 'Registrar' WHERE login = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (login, ))
            self.conn.commit()
        except Error as e:
            print(e)

    # def check_todos_usuarios(self):
    #     try:
    #         cur = self.conn.cursor()
    #         cur.execute("SELECT DISTINCT nome FROM usuarios")
    #         rows = cur.fetchall()
    #         if rows:
    #             return [item[0] for item in rows]
    #         return []
    #     except Error as e:
    #         print(e)

    def get_nome_from_login_antigo(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM usuarios_antigos WHERE login=?", (login, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Login sem nome associado'
        except Error as e:
            print(e)
            return False

    def get_nome_from_login(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM usuarios WHERE login=?", (login, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Login sem nome associado'
        except Error as e:
            print(e)
            return False

    def get_nome_from_tag(self, tag):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM usuarios WHERE tag=?", (tag, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Tag sem nome associado'
        except Error as e:
            print(e)
            return False

    def get_login_from_tag(self, tag):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT login FROM usuarios WHERE tag=?", (tag, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Tag sem login associado'
        except Error as e:
            print(e)
            return False

    def get_email_from_login(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT email FROM usuarios WHERE login=?", (login, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Login sem email associado'
        except Error as e:
            print(e)
            return False

    def get_grupo_from_login(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT grupo FROM usuarios WHERE login=?", (login, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Login sem grupo associado'
        except Error as e:
            print(e)
            return False



    def add_autorizacao_equip(self, login, nome, equipamento, super="False"):
        try:
            sql = "INSERT INTO autorizacao_equip(login, nome, equipamento, super) VALUES(?,?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (login, nome, equipamento, super))
            self.conn.commit()
            print('adicionado na linha ' + str(cur.lastrowid))
            return True
        except Error as e:
            print(e)
            return False

    def add_autorizacao_nome_equip(self, nome, equipamento, super="False"):
        try:
            sql = "INSERT INTO autorizacao_equip(nome, equipamento, super) VALUES(?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (nome, equipamento, super))
            self.conn.commit()
            print('adicionado na linha ' + str(cur.lastrowid))
            return True
        except Error as e:
            print(e)
            return False

    def add_autorizacao_login_equip(self, login, equipamento, super="False"):
        try:
            sql = "INSERT INTO autorizacao_equip(login, equipamento, super) VALUES(?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (login, equipamento, super))
            self.conn.commit()
            print('adicionado na linha ' + str(cur.lastrowid))
            return True
        except Error as e:
            print(e)
            return False


    def check_superusuario(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT equipamento, super FROM autorizacao_equip WHERE login=?",
                (login, ))
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def set_superusuario(self, login, equipamento):
        try:
            sql = "UPDATE autorizacao_equip SET super = 'True' WHERE login = ? " +\
                "AND equipamento = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (login, equipamento))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_todos_usuarios_do_equip(self, equip):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT login FROM autorizacao_equip WHERE equipamento=?",
                (equip, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)


    def check_todos_grupos_do_equip(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT grupo FROM usuarios")
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)

    def check_todos_usuarios_do_grupo(self, grupo):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT login FROM usuarios WHERE grupo=?",
                (grupo, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)


    def check_todos_usuarios_antigos_do_grupo(self, grupo):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT login FROM usuarios_antigos WHERE grupo=?",
                (grupo, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)

    def check_todos_superusuarios_do_equip(self, equip):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT login FROM autorizacao_equip WHERE equipamento=? AND super='True'",
                (equip, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)

    def check_autorizacao_equip(self, login, equipamento):
        try:
            logins = self.check_todos_usuarios_do_equip(equipamento)
            if login in logins:
                return True
            else:
                return False
        except Error as e:
            print(e)

    def set_hora_inicio(self, login, equipamento):
        try:
            em_uso = self.check_equip_em_uso()
            if em_uso:
                login_em_uso = em_uso[0][1]
                if equipamento in [item[0] for item in em_uso]:
                    return False, login_em_uso

            if self.check_autorizacao_equip(login, equipamento) is True:
                if self.rpi_online():
                    self.hora_inicio = str(datetime.datetime.now())[:-7]
                else:
                    self.hora_inicio = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]
                nome = self.get_nome_from_login(login)    
                sql = "INSERT INTO uso_equip(login, nome, equipamento, hora_inicio) VALUES(?,?,?,?)"
                cur = self.conn.cursor()
                cur.execute(sql, (login, nome, equipamento, self.hora_inicio))
                self.conn.commit()
                print('Usuário: ' + login + '\tInicio: ' + self.hora_inicio)
                return True, "Uso liberado"
        except Error as e:
            print(e)

    def check_comentario(self, login, equipamento):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT comentario FROM uso_equip WHERE login=? AND equipamento=? AND hora_inicio=?",
                (login, equipamento, self.hora_inicio))
            row = cur.fetchall()
            if row[0][0] == None:
                return ""
            else:
                return str(row[0][0]) + '\n\n'
        except Error as e:
            print(e)

    def set_comentario(self, login, equipamento, comentario):
        try:
            comentario_antigo = self.check_comentario(login, equipamento)
            sql = "UPDATE uso_equip SET comentario = ? WHERE login = ? " +\
                "AND equipamento = ? AND hora_inicio = ?"
            novo_comentario = comentario_antigo + comentario
            cur = self.conn.cursor()
            cur.execute(sql,
                        (novo_comentario, login, equipamento, self.hora_inicio))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_id_inicio(self, login, equipamento):
        try:
            if self.check_autorizacao_equip(login, equipamento) is True:
                cur = self.conn.cursor()
                cur.execute(
                    "SELECT DISTINCT id, hora_inicio, hora_fim FROM uso_equip WHERE login=? AND equipamento=? AND hora_fim IS NULL",
                    (login, equipamento))
                rows = cur.fetchall()
                if rows:
                    # retorna a linha (id) do equip com hora_inicio e sem hora_fim
                    return str(
                        [item[0] for item in rows if item[2] is None][0])
                return rows
        except Error as e:
            print(e)

    def set_hora_fim(self, login, equipamento, tempo_total, situacao='OK'):
        try:
            if self.check_autorizacao_equip(login, equipamento) is True:
                # linha_id = self.check_id_inicio(login, equipamento)
                linha_id = self.ultima_linha_registrada(login, equipamento)

                if linha_id == []:
                    print("ERRO! " + login + ' não está usando o equipamento.')
                    return False

                if self.rpi_online():
                    hora = str(datetime.datetime.now())[:-7]
                else:
                    hora = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]
                
                sql = "UPDATE uso_equip SET hora_fim = ?, tempo_total = ?, situacao = ? WHERE id = ?"
                cur = self.conn.cursor()
                cur.execute(sql, (hora, tempo_total, situacao, linha_id))
                self.conn.commit()
                print('Usuário: ' + login + '\tFim: ' + hora)
        except Error as e:
            print(e)

    def force_hora_fim(self, login, equipamento):
        # funcinando por enquanto apenas para um equipamento
        try:
            em_uso = self.check_equip_em_uso()
            if equipamento in [item[0] for item in em_uso]:
                inicio = em_uso[0][2][-8:]
                fim_forcado = str(datetime.datetime.now())[:-7][-8:]
                tempo_forcado = self.subtrair_tempo(fim_forcado, inicio)
                self.set_hora_fim(em_uso[0][1], em_uso[0][0], tempo_forcado, situacao="Esqueceu logado! Saída forçada por " + login)
                                                                     
        except Error as e:
            print(e)

    def ultima_linha_registrada(self, login, equipamento):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM uso_equip WHERE login = ? and equipamento = ?",(login, equipamento))
            row = cur.fetchall()
            return row[-1][0]
        except Error as e:
            print(e)

    def set_hora_fim_seguranca(self, login, equipamento, tempo_total, situacao='ERRO! REGISTRO DE SEGURANÇA A CADA MINUTO ATIVADO!.'):
        try:
            id = self.ultima_linha_registrada(login, equipamento)
            if self.rpi_online():
                hora = str(datetime.datetime.now())[:-7]
            else:
                hora = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]            
            sql = "UPDATE uso_equip SET hora_fim = ?, tempo_total = ?, situacao = ? WHERE id = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (hora, tempo_total, situacao, id))
            self.conn.commit()
        except Error as e:
            print(e)



    def subtrair_tempo(self, tempo1, tempo2):
        t1_seg = int(tempo1[-2:])
        t1_min = int(tempo1[-5:-3])
        t1_hora = int(tempo1[-8:-6])
        t2_seg = int(tempo2[-2:])
        t2_min = int(tempo2[-5:-3])
        t2_hora = int(tempo2[-8:-6])

        t1 = t1_seg + 60*t1_min + 60*60*t1_hora
        t2 = t2_seg + 60*t2_min + 60*60*t2_hora

        dt = t1 - t2
        
        dt_hora = int(dt/3600)
        dt_min = int((dt%3600)/60)
        dt_seg = int((dt%3600)%60)

        if dt_seg < 10:
            s = '0' + str(dt_seg)
        else:
            s = str(dt_seg)               
        if dt_min < 10:
            m = '0' + str(dt_min)
        else:
            m = str(dt_min)
        if dt_hora < 10:
            h = '0' + str(dt_hora)
        else:
            h = str(dt_hora)      

        return h + ':' + m + ':' + s

    def check_equip_em_uso(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT equipamento, login, hora_inicio FROM uso_equip WHERE hora_fim IS NULL"
            )
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def set_entrada_ou_saida(self, tag):
        try:
            login = self.get_login_from_tag(tag)
            check_presenca = self.check_tag_presenca_em_aberto(tag)
            if check_presenca == "Usuário não identificado!":
                return "Usuário não identificado!"

            elif check_presenca == "Não esta presente":

                if self.rpi_online():
                    hora_entrada = str(datetime.datetime.now())[:-7]
                else:
                    hora_entrada = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]

                nome = self.get_nome_from_login(login)
                sql = "INSERT INTO presenca(login, nome, tag, hora_entrada, " +\
                    "hora_saida) VALUES(?,?,?,?,?)"
                cur = self.conn.cursor()
                cur.execute(sql, (login, nome, tag, hora_entrada, None))
                self.conn.commit()
                print('Usuário: ' + login + '\tEntrada: ' + hora_entrada)
                return "Entrada liberada! " + hora_entrada
            else:
                linha_db = check_presenca
                if self.rpi_online():
                    hora_saida = str(datetime.datetime.now())[:-7]
                else:
                    hora_saida = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]
                sql = "UPDATE presenca SET hora_saida=? WHERE id = ?"
                cur = self.conn.cursor()
                cur.execute(sql, (hora_saida, linha_db))
                self.conn.commit()
                print('Usuário: ' + login + '\tSaída: ' + hora_saida)
                return "Saída registrada! " + hora_saida

        except Error as e:
            print(e)

    def check_tag_presenca_em_aberto(self, tag):
        try:
            login = self.get_login_from_tag(tag)
            if login == 'Tag sem login associado':
                return "Usuário não identificado!"
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT id FROM presenca WHERE login = ? AND "
                        + "hora_saida IS NULL", (login, ))
            row = cur.fetchall()
            if row:
                return row[0][0]
            else:
                return "Não esta presente"
        except Error as e:
            print(e)

    def check_login_presenca_em_aberto(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT id FROM presenca WHERE login = ? AND "
                        + "hora_saida IS NULL", (login, ))
            row = cur.fetchall()
            if row:
                return True
            else:
                return False
        except Error as e:
            print(e)
            return False

    def check_lista_presentes(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT login FROM presenca WHERE hora_saida IS NULL")
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            else:
                return []
        except Error as e:
            print(e)
            return False

    def check_uso_equip(self, login):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT login, nome, hora_inicio, hora_fim, tempo_total, situacao, comentario FROM uso_equip WHERE login=?", (login, ))
            dados = cur.fetchall()
            if dados == []:
                return dados
            return dados
        except Error as e:
            print(e)

    def todas_linhas_de_uso(self, equipamento):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM uso_equip WHERE equipamento=?",(equipamento,))
            row = cur.fetchall()
            return row
        except Error as e:
            print(e)


    def get_nome_from_id(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM uso_equip WHERE id=?", (id, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Login sem nome associado'
        except Error as e:
            print(e)
            return False

    def check_uso_equip_id(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT login, nome, hora_inicio, hora_fim, tempo_total, situacao, comentario FROM uso_equip WHERE id=?", (id, ))
            dados = cur.fetchall()
            if dados == []:
                return dados
            return dados
        except Error as e:
            print(e)

    def check_tempo_total_de_uso_equip(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT tempo_total FROM uso_equip ")
            dados = cur.fetchall()
            if dados == []:
                return dados
            return dados
        except Error as e:
            print(e)


if __name__ == '__main__':
    db = BancoDeDados('arquivo.db') #exemplo de uso


# %%
