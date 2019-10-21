import sqlite3
from sqlite3 import Error
import datetime
import csv

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class BancoDeDados():

    def __init__(self, arquivo):

        self.conn = self.create_connection(arquivo)
        self.hora_inicio = str(datetime.datetime.now())[:-7]

    def create_table_usuarios(self):
        nova_tabela = "CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY " +\
            "KEY, tag TEXT UNIQUE, nome TEXT UNIQUE, email TEXT, adicionado_por TEXT, " +\
            "permissao TEXT, senha TEXT)"
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_table_autorizacao_equip(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS autorizacao_equip(id INTEGER
                PRIMARY KEY, equipamento TEXT, nome TEXT, super TEXT,
                UNIQUE(nome, equipamento))'''
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_table_presenca(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS presenca(id INTEGER
                PRIMARY KEY, nome TEXT, tag TEXT, hora_entrada TEXT,
                 hora_saida TEXT)'''
        try:
            c = self.conn.cursor()
            c.execute(nova_tabela)
        except Error as e:
            print(e)

    def create_table_uso_equip(self):
        nova_tabela = '''CREATE TABLE IF NOT EXISTS uso_equip(id INTEGER PRIMARY
            KEY, nome TEXT, equipamento TEXT, hora_inicio TEXT, hora_fim TEXT,
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
            file = open(
                os.path.join(dir_path, 'log/tabela_uso_equip.csv'), 'r')
        except IOError:
            with open(
                    os.path.join(dir_path, 'log/tabela_uso_equip.csv'),
                    'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow([
                    "id", "nome", "equipamento", "hora_inicio", "hora_fim",
                    "tempo_total", "comentario"
                ])
        try:
            file = open(os.path.join(dir_path, 'log/tabela_presenca.csv'), 'r')
        except IOError:
            with open(os.path.join(dir_path, 'log/tabela_presenca.csv'),
                      'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow(
                    ["id", "nome", "tag", "hora_entrada", "hora_saida"])
        try:
            file = open(
                os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),
                'r')
        except IOError:
            with open(
                    os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),
                    'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow(["id", "equipamento", "nome", "super"])
        try:
            file = open(os.path.join(dir_path, 'log/tabela_usuarios.csv'), 'r')
        except IOError:
            with open(os.path.join(dir_path, 'log/tabela_usuarios.csv'),
                      'w+') as csv_file:
                spamwriter = csv.writer(csv_file, delimiter=';')
                spamwriter.writerow([
                    "id", "tag", "nome", "email", "adicionado_por",
                    "permissao", "senha"
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

    def check_lista_usuarios(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nome FROM usuarios")
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
                "id", "nome", "equipamento", "hora_inicio", "hora_fim",
                "tempo_total", "comentario"
            ])
            for row in tabela_uso_equip:
                spamwriter.writerow(row)

        with open(
                os.path.join(dir_path, 'log/tabela_autorizacao_equip.csv'),
                'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow(["id", "equipamento", "nome", "super"])
            for row in tabela_autorizacao_equip:
                spamwriter.writerow(row)

        with open(os.path.join(dir_path, 'log/tabela_usuarios.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow([
                "id", "tag", "nome", "email", "adicionado_por", "permissao",
                "senha"
            ])
            for row in tabela_usuarios:
                spamwriter.writerow(row)

        with open(os.path.join(dir_path, 'log/tabela_presenca.csv'),
                  'w+') as csv_file:
            spamwriter = csv.writer(csv_file, delimiter=';')
            spamwriter.writerow(
                ["id", "nome", "tag", "hora_entrada", "hora_saida"])
            for row in tabela_presenca:
                spamwriter.writerow(row)

    def add_novo_usuario(self,
                         tag_novo,
                         nome,
                         email,
                         password,
                         tag_autorizacao,
                         permissao='apenas uso'):
        try:
            sql = "INSERT INTO usuarios(tag, nome, email, senha ,adicionado_por, permissao) VALUES(?,?,?,?,?,?)"
            cur = self.conn.cursor()
            cur.execute(sql, (tag_novo, nome, email, password, tag_autorizacao,
                              permissao))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def remove_usuario(self, tag_ou_nome):
        try:
            sql = 'DELETE FROM usuarios WHERE tag=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome, ))
            sql = 'DELETE FROM usuarios WHERE nome=?'
            cur = self.conn.cursor()
            cur.execute(sql, (tag_ou_nome, ))
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

    def check_usuario(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE nome=?", (nome, ))
            row = cur.fetchall()
            if row == []:
                return row
            return [item for item in row[0]]
        except Error as e:
            print(e)

    def check_senha(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT senha FROM usuarios WHERE nome=?", (nome, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows][0]
        except Error as e:
            print(e)

    def set_senha(self, nome, senha):
        try:
            sql = "UPDATE usuarios SET senha = ? WHERE nome = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (senha, nome))
            self.conn.commit()
        except Error as e:
            print(e)

    def set_tag(self, nome, tag):
        try:
            sql = "UPDATE usuarios SET tag = ? WHERE nome = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (tag, nome))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return e

    def remove_tag(self, nome):
        try:
            sql = "UPDATE usuarios SET tag = ? WHERE nome = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (None, nome))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_permissao(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT permissao FROM usuarios WHERE nome=?",
                        (nome, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows][0]
        except Error as e:
            print(e)

    def set_permissao(self, nome):
        try:
            sql = "UPDATE usuarios SET permissao = 'Registrar' WHERE nome = ? "
            cur = self.conn.cursor()
            cur.execute(sql, (nome, ))
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

    def get_email(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT email FROM usuarios WHERE nome=?", (nome, ))
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return 'Tag sem nome associado'
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

    def check_superusuario(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT equipamento, super FROM autorizacao_equip WHERE nome=?",
                (nome, ))
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def set_superusuario(self, nome, equipamento):
        try:
            sql = "UPDATE autorizacao_equip SET super = 'True' WHERE nome = ? " +\
                "AND equipamento = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (nome, equipamento))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_todos_usuarios_do_equip(self, equip):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT nome FROM autorizacao_equip WHERE equipamento=?",
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
                "SELECT DISTINCT nome FROM autorizacao_equip WHERE equipamento=? AND super='True'",
                (equip, ))
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            return []
        except Error as e:
            print(e)

    def check_autorizacao_equip(self, nome, equipamento):
        try:
            nomes = self.check_todos_usuarios_do_equip(equipamento)
            if nome in nomes:
                return True
            else:
                return False
        except Error as e:
            print(e)

    def set_hora_inicio(self, nome, equipamento):
        try:
            em_uso = self.check_equip_em_uso()
            if em_uso:
                nome_em_uso = em_uso[0][1]
                if equipamento in [item[0] for item in em_uso]:
                    return False, nome_em_uso

            if self.check_autorizacao_equip(nome, equipamento) is True:
                self.hora_inicio = str(datetime.datetime.now())[:-7]
                sql = "INSERT INTO uso_equip(nome, equipamento, hora_inicio) VALUES(?,?,?)"
                cur = self.conn.cursor()
                cur.execute(sql, (nome, equipamento, self.hora_inicio))
                self.conn.commit()
                print('Usuário: ' + nome + '\tInicio: ' + self.hora_inicio)
                return True, "Uso liberado"
        except Error as e:
            print(e)

    def check_comentario(self, nome, equipamento):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT comentario FROM uso_equip WHERE nome=? AND equipamento=? AND hora_inicio=?",
                (nome, equipamento, self.hora_inicio))
            row = cur.fetchall()
            if row[0][0] == None:
                return ""
            else:
                return str(row[0][0]) + '\n\n'
        except Error as e:
            print(e)

    def set_comentario(self, nome, equipamento, comentario):
        try:
            comentario_antigo = self.check_comentario(nome, equipamento)
            sql = "UPDATE uso_equip SET comentario = ? WHERE nome = ? " +\
                "AND equipamento = ? AND hora_inicio = ?"
            novo_comentario = comentario_antigo + comentario
            cur = self.conn.cursor()
            cur.execute(sql,
                        (novo_comentario, nome, equipamento, self.hora_inicio))
            self.conn.commit()
        except Error as e:
            print(e)

    def check_id_inicio(self, nome, equipamento):
        try:
            if self.check_autorizacao_equip(nome, equipamento) is True:
                cur = self.conn.cursor()
                cur.execute(
                    "SELECT DISTINCT id, hora_inicio, hora_fim FROM uso_equip WHERE nome=? AND equipamento=? AND hora_fim IS NULL",
                    (nome, equipamento))
                rows = cur.fetchall()
                if rows:
                    # retorna a linha (id) do equip com hora_inicio e sem hora_fim
                    return str(
                        [item[0] for item in rows if item[2] is None][0])
                return rows
        except Error as e:
            print(e)

    def set_hora_fim(self, nome, equipamento, tempo_total):
        try:
            if self.check_autorizacao_equip(nome, equipamento) is True:
                linha_id = self.check_id_inicio(nome, equipamento)
                if linha_id == []:
                    print("ERRO! " + nome + ' não está usando o equipamento.')
                    return False
                hora = str(datetime.datetime.now())[:-7]
                sql = "UPDATE uso_equip SET hora_fim = ?, tempo_total = ? WHERE id = ?"
                cur = self.conn.cursor()
                cur.execute(sql, (hora, tempo_total, linha_id))
                self.conn.commit()
                print('Usuário: ' + nome + '\tFim: ' + hora)
        except Error as e:
            print(e)

    def force_hora_fim(self, nome, equipamento):
        # funcinando por enquanto apenas para um equipamento
        try:
            hora = str(datetime.datetime.now())[:-7]
            em_uso = self.check_equip_em_uso()
            if equipamento in [item[0] for item in em_uso]:
                self.set_hora_fim(em_uso[0][1], em_uso[0][0],
                                  "SAÍDA FORÇADA POR " + nome)
        except Error as e:
            print(e)

    def check_equip_em_uso(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT DISTINCT equipamento, nome FROM uso_equip WHERE hora_fim IS NULL"
            )
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def set_entrada_ou_saida(self, tag):
        try:
            nome = self.get_nome_from_tag(tag)
            check_presenca = self.check_tag_presenca_em_aberto(tag)
            if check_presenca == "Usuário não identificado!":
                return "Usuário não identificado!"

            elif check_presenca == "Não esta presente":
                hora_entrada = str(datetime.datetime.now())[:-7]
                sql = "INSERT INTO presenca(nome, tag, hora_entrada, " +\
                    "hora_saida) VALUES(?,?,?,?)"
                cur = self.conn.cursor()
                cur.execute(sql, (nome, tag, hora_entrada, None))
                self.conn.commit()
                print('Usuário: ' + nome + '\tEntrada: ' + hora_entrada)
                return "Entrada liberada! " + hora_entrada
            else:
                linha_db = check_presenca
                hora_saida = str(datetime.datetime.now())[:-7]
                sql = "UPDATE presenca SET hora_saida=? WHERE id = ?"
                cur = self.conn.cursor()
                cur.execute(sql, (hora_saida, linha_db))
                self.conn.commit()
                print('Usuário: ' + nome + '\tSaída: ' + hora_saida)
                return "Saída registrada! " + hora_saida

        except Error as e:
            print(e)

    def check_tag_presenca_em_aberto(self, tag):
        try:
            nome = self.get_nome_from_tag(tag)
            if nome == 'Tag sem nome associado':
                return "Usuário não identificado!"
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT id FROM presenca WHERE nome = ? AND "
                        + "hora_saida IS NULL", (nome, ))
            row = cur.fetchall()
            if row:
                return row[0][0]
            else:
                return "Não esta presente"
        except Error as e:
            print(e)

    def check_nome_presenca_em_aberto(self, nome):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT id FROM presenca WHERE nome = ? AND "
                        + "hora_saida IS NULL", (nome, ))
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
                "SELECT DISTINCT nome FROM presenca WHERE hora_saida IS NULL")
            rows = cur.fetchall()
            if rows:
                return [item[0] for item in rows]
            else:
                return []
        except Error as e:
            print(e)
            return False


if __name__ == '__main__':
    db = BancoDeDados()
