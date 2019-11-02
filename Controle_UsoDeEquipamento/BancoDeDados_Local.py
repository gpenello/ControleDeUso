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
        except urllib2.URLError as err:
            print(err)
            return False
            

    def fechar_conn(self):
        self.conn.close()

    def create_table_usuarios(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY " +\
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
            tempo_total TEXT, comentario TEXT)'''
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
                self.create_table_autorizacao_equip()  # tabela de autorizacoes
                # criando controle de uso de equip.
                self.create_table_uso_equip()
                self.create_table_presenca()
                self.create_csv_files()

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
                    "tempo_total", "comentario"
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

    def check_tabela_presenca(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM presenca")
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
        tabela_presenca = self.check_tabela_presenca()

        with open(os.path.join(dir_path, 'log/tabela_uso_equip.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow([
                "id", "login", "nome", "equipamento", "hora_inicio", "hora_fim",
                "tempo_total", "comentario"
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

        with open(os.path.join(dir_path, 'log/tabela_presenca.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow(
                ["id", "login", "nome", "tag", "hora_entrada", "hora_saida"])
            for row in tabela_presenca:
                spamwriter.writerow(row)

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

    def remove_usuario(self, tag_ou_nome_ou_login):
        try:
            sql = 'DELETE FROM usuarios WHERE tag=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
            sql = 'DELETE FROM usuarios WHERE nome=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
            sql = 'DELETE FROM usuarios WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
            sql = 'DELETE FROM autorizacao_equip WHERE login=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
            sql = 'DELETE FROM autorizacao_equip WHERE tag=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
            sql = 'DELETE FROM autorizacao_equip WHERE nome=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome_ou_login, ))
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

    def set_hora_fim(self, login, equipamento, tempo_total):
        try:
            if self.check_autorizacao_equip(login, equipamento) is True:
                linha_id = self.check_id_inicio(login, equipamento)
                if linha_id == []:
                    print("ERRO! " + login + ' não está usando o equipamento.')
                    return False

                if self.rpi_online():
                    hora = str(datetime.datetime.now())[:-7]
                else:
                    hora = '[RPI OFFLINE]' + str(datetime.datetime.now())[:-7]
                
                sql = "UPDATE uso_equip SET hora_fim = ?, tempo_total = ? WHERE id = ?"
                cur = self.conn.cursor()
                cur.execute(sql, (hora, tempo_total, linha_id))
                self.conn.commit()
                print('Usuário: ' + login + '\tFim: ' + hora)
        except Error as e:
            print(e)

    def force_hora_fim(self, login, equipamento):
        # funcinando por enquanto apenas para um equipamento
        try:
            em_uso = self.check_equip_em_uso()
            if equipamento in [item[0] for item in em_uso]:
                self.set_hora_fim(em_uso[0][1], em_uso[0][0],
                                  "SAÍDA FORÇADA POR " + login)
        except Error as e:
            print(e)

    def check_equip_em_uso(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT equipamento, login FROM uso_equip WHERE hora_fim IS NULL"
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
            cur.execute("SELECT login, nome, hora_inicio, hora_fim, tempo_total FROM uso_equip WHERE login=?", (login, ))
            dados = cur.fetchall()
            if dados == []:
                return dados
            return dados
        except Error as e:
            print(e)


if __name__ == '__main__':
    db = BancoDeDados('arquivo.db')
