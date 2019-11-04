#!/usr/bin/python3
# -*- coding: utf-8 -*-
#%%
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QDesktopWidget, QSplashScreen
import sys
import time
import os
import subprocess
import signal
from sys import platform

import criptografarPassword as cript
from BancoDeDados_Local import BancoDeDados
import paramikoClient


class DesignerMainWindow(QMainWindow):

    equipamento = 'LaserCutter'  # colocar o nome do equipamento do arquivo db
    TelaCheia = True
    software_externo_path = '/home/pi/Documents/registro-de-uso-presenca-lab/K40_Whisperer-0.37_src/k40_whisperer.py'
    servidorFTP = False
    host, user, senha = ('raspberrypi.local', 'pi', 'lab2')
    

    # -----------------------------------------------
    # IMPORTANTE: FALTA INTEGRAR OS BANCOS DE DADOS LOCAIS COM O DO RPi de presença com tag RFID.
    # Eles estão diferentes!
    # -----------------------------------------------

    # ------------------------------------------------------
    # Ainda não testado completamente
    forcar_presenca = False

    # -----------------------------------------------

    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        uic.loadUi('GUI/telaControle.ui', self)

        self.sair = False
        # TEM QUE REFAZER ESTA PARTE COMENTADA ABAIXO PARA USAR O SERVIDOR COM PRESENÇA PELO TAG    
        # if self.servidorFTP is True:
        #     self.baixar_db_usuarios()
        # self.db_usuario = BancoDeDados("./log/BancoDeDados_Usuarios.db")

        arquivo = "./log/BancoDeDados_Local_" + self.equipamento + ".db"
        self.db = BancoDeDados(arquivo)

        self.novoUsuario = NovoUsuario(self)
        self.todosUsuarios = TelaTodosUsuarios(self)
        self.historicoDeUso = TelaHistoricoDeUso(self)
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        #        self.setWindowFlags()
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password.returnPressed.connect(self.get_login_pass)
        self.btn_novo.clicked.connect(self.cadastrarNovoUsuario)
        self.btn_usuarios.clicked.connect(self.verTodosUsuarios)
        self.btn_tempo.clicked.connect(self.verHistoricoDeUso)

        self.btn_ok.clicked.connect(self.get_login_pass)
        self.btn_power.clicked.connect(self.shutdown)
        if self.servidorFTP is True:
            self.btn_novo.setEnabled(False)
        # self.btn_sair.clicked.connect(self.fechar)
        self.center()
        self.permitir_min = False
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))
        # self.installEventFilter(AltTab())

        if platform == "linux" or platform == "linux2":
            self.software_externo = subprocess.Popen(['sudo', 'python3', self.software_externo_path])

    def shutdown(self):
        reply = QMessageBox.question(self, 'Desligando...',
                                        'Desligar o computador?', QMessageBox.Yes,
                                        QMessageBox.No)
        if reply == QMessageBox.Yes:
            if platform == "linux" or platform == "linux2":
                subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
            elif platform == "win32":
                QMessageBox.about(self, "Desligando...","Este comando funciona apenas em Linux.")


    def baixar_db_usuarios(self):
        try:
            cliente = paramikoClient.Client()
            cliente.conectar(self.host, self.user, self.senha)
            arquivo = "/home/pi/Documents/Controle_presencaLab/log/BancoDeDados_Usuarios.db"
            cliente.baixar_arquivo(arquivo, "./log/BancoDeDados_Usuarios.db")
            cliente.fechar_cliente()

        except Exception as e:
            print(str(e))
            QMessageBox.about(
                self, "Erro de conexão com o rpi:",
                str(e) +
                "\n\nVerificar se o servidor FTP está ligado e se a conexão com a internet está ok."
            )

    def reload_db(self):
        self.db.fechar_conn()
        arquivo = "./log/BancoDeDados_Local_" + self.equipamento + ".db"
        self.db = BancoDeDados(arquivo)

    def enviar_db_local_FTP(self):
        try:
            cliente = paramikoClient.Client()
            cliente.conectar(self.host, self.user, self.senha)
            cliente.executar_comando('ls')
            if 'Registros de uso\n' not in cliente.stdout.readlines():
                cliente.executar_comando('mkdir "Registros de uso"')
                print("Pasta 'Registros de uso' criada no RPi.")
            arquivo = "BancoDeDados_Local_" + self.equipamento + ".db"
            cliente.enviar_arquivo("./log/" + arquivo,
                                   'Registros de uso/' + arquivo)
            cliente.fechar_cliente()

        except Exception as e:
            print(str(e))
            QMessageBox.about(
                self, "Erro de conexão com o rpi:",
                str(e) +
                "\n\nVerificar se o servidor FTP está ligado e se a conexão com a internet está ok."
            )

        self.lbl_info.setText("")


    def verHistoricoDeUso(self):

        senha_autorizacao, ok = QInputDialog.getText(
            self, "Aguardando autorização...", "Senha de autorização:",
            QtWidgets.QLineEdit.Password)
        if ok:
            if cript.check_autorizacao(senha_autorizacao):
                self.keep_minimized()
                self.historicoDeUso.popular_combobox()
                self.historicoDeUso.show()
                self.historicoDeUso.activateWindow()
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha de autorização não confere!")        



    def verTodosUsuarios(self):

        senha_autorizacao, ok = QInputDialog.getText(
            self, "Aguardando autorização...", "Senha de autorização:",
            QtWidgets.QLineEdit.Password)
        if ok:
            if cript.check_autorizacao(senha_autorizacao):
                self.keep_minimized()
                self.todosUsuarios.popular_combobox()
                self.todosUsuarios.show()
                self.todosUsuarios.activateWindow()
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha de autorização não confere!")        

    def cadastrarNovoUsuario(self):

        senha_autorizacao, ok = QInputDialog.getText(
            self, "Aguardando autorização...", "Senha de autorização:",
            QtWidgets.QLineEdit.Password)
        if ok:
            if cript.check_autorizacao(senha_autorizacao):
                self.keep_minimized()
                self.novoUsuario.show()
                self.novoUsuario.activateWindow()
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha de autorização não confere!")

    def get_login_pass(self):
        # if self.servidorFTP is True:
        #     self.baixar_db_usuarios()
        # self.db_usuario = BancoDeDados("./log/BancoDeDados_Usuarios.db")
        login = self.txt_login.text()
        password = self.txt_password.text()
        self.txt_login.setText('')
        self.txt_password.setText('')
        # dados_usuario = self.db_usuario.check_usuario(login)

        dados_usuario = self.db.check_usuario(login)

        if login == 'admin':
            if cript.check_autorizacao(password):
                self.permitir_min = True
                self.showMinimized()
                time.sleep(1)
                self.permitir_min = False
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha do administrador não confere!")
        elif dados_usuario != []:
            senha = dados_usuario[7]
            if self.forcar_presenca is True:
                # bool_presente = self.db_usuario.check_login_presenca_em_aberto(
                #     login)
                bool_presente = self.db.check_login_presenca_em_aberto(
                    login)
                if bool_presente is False:
                    QMessageBox.about(
                        self, "Erro!",
                        str("Marque presença no lab. antes de utilizar os " +
                            "equipamentos!"))
                    return
            if cript.check_password(senha, password):
                disponivel, login_usando = self.db.set_hora_inicio(
                    login, self.equipamento)
                if not disponivel:
                    texto = login_usando + \
                        ' está usando este equipamento. Deseja forçar a saída dele?'
                    reply = QMessageBox.question(self, 'Equipamento em uso!',
                                                 texto, QMessageBox.Yes,
                                                 QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.db.force_hora_fim(login, self.equipamento)
                        self.db.set_hora_inicio(login, self.equipamento)
                        self.janelatempo = TempoUso(self, login)
                        self.janelatempo.show()
                        self.janelatempo.activateWindow()
                        self.keep_minimized()
                        if platform == "linux" or platform == "linux2":
                            self.abrir_software_externo()


                else:
                    self.db.set_hora_inicio(login, self.equipamento)
                    self.janelatempo = TempoUso(self, login)
                    self.janelatempo.show()
                    self.janelatempo.activateWindow()
                    self.keep_minimized()
                    if platform == "linux" or platform == "linux2":
                        self.abrir_software_externo()
                    
            else:
                QMessageBox.about(self, "Erro!", str("Senha não confere!"))
        else:
            QMessageBox.about(self, "Erro!", "Usuário não cadastrado!")

    def abrir_software_externo(self):
        if self.software_externo.poll() != None:
            if platform == "linux" or platform == "linux2":
                self.software_externo = subprocess.Popen(['sudo', 'python3', self.software_externo_path])

    def changeEvent(self, e):
        if e.type() == e.WindowStateChange:
            if self.permitir_min is True:
                self.showMinimized()
            else:
                if self.TelaCheia is True:
                    self.showFullScreen()
                else:
                    self.showNormal()
                self.db.export_all_db_to_csv()
                                
                if self.servidorFTP is True:
                    self.enviar_db_local_FTP()
                
            self.activateWindow()
        try:       
            self.txt_login.setFocus()
        except AttributeError:
            pass

    def keep_minimized(self):
        self.permitir_min = True
        self.showMinimized()

    def fechar(self):  # só era usado com o btn_sair durante os testes
        self.sair = True
        self.close()

    def center(self):
        centroTela = QDesktopWidget().availableGeometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(centroTela)
        self.move(qr.topLeft())

    # def keyPressEvent(self, event):
    #     if event.modifiers() == QtCore.Qt.AltModifier:
    #         print('mod')    
    #         event.ignore()
    #         return



    def closeEvent(self, event):
        if self.sair is False:
            event.ignore()


class TelaTodosUsuarios(QMainWindow):

    def __init__(self, janelaPrincipal, parent=None):
        super(TelaTodosUsuarios, self).__init__(parent)
        uic.loadUi('GUI/telaTodosUsuarios.ui', self)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))

        self.janelaPrincipal = janelaPrincipal
        self.popular_combobox()

        self.cbx_logins.activated.connect(self.login_selecionado)
        self.btn_remover.clicked.connect(self.remover_usuario)

    def popular_combobox(self):
        self.cbx_logins.clear()
        self.cbx_logins.addItem("Selecione o usuário:")
        # todos_usuarios = self.janelaPrincipal.db_usuario.check_todos_usuarios_do_equip('LaserCutter')
        todos_usuarios = self.janelaPrincipal.db.check_todos_usuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_usuarios)
        # todos_superusuarios = self.janelaPrincipal.db_usuario.check_todos_superusuarios_do_equip('LaserCutter')
        todos_superusuarios = self.janelaPrincipal.db.check_todos_superusuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_superusuarios)


    def remover_usuario(self):
        
        login = self.cbx_logins.currentText()

        if login == "Selecione o usuário:":
            QMessageBox.about(self, "Selecione usuário!", "Nenhum usuário foi selecionado.")
            self.close()
            return           
        
        senha_autorizacao, ok = QInputDialog.getText(
            self, "Aguardando autorização...", "Remover usuário: " + login + "\nSenha de autorização:",
            QtWidgets.QLineEdit.Password)

        if ok:
            if cript.check_autorizacao(senha_autorizacao):
                self.janelaPrincipal.db.remove_usuario_por_login(login)
                QMessageBox.about(self, "OK!", login + " removido do banco de dados!")
            else:
                QMessageBox.about(self, "Erro!",
                                    "Senha de autorização não confere!")  
        
            
        self.close()
        


    def login_selecionado(self, idx):
        login = self.cbx_logins.currentText()

        if login == "Selecione o usuário:":
            return
        # dados = self.janelaPrincipal.db_usuario.check_usuario(login)
        dados = self.janelaPrincipal.db.check_usuario(login)
        idx, tag, login, nome, email, add_por, permissao, senha, grupo = dados
        if tag == None:
            tag = "Tag não cadastrada."
        self.lbl_tag.setText(tag)
        self.lbl_login.setText(login)
        self.lbl_nome.setText(nome)
        self.lbl_email.setText(email)
        self.lbl_adicionadopor.setText(add_por)
        self.lbl_permissao.setText(permissao)
        self.lbl_grupo.setText(grupo)
        
        
    def closeEvent(self, event):

        self.lbl_tag.setText("")
        self.lbl_login.setText("")
        self.lbl_nome.setText("")
        self.lbl_email.setText("")
        self.lbl_adicionadopor.setText("")
        self.lbl_permissao.setText("")
        self.lbl_grupo.setText("")

        self.janelaPrincipal.permitir_min = False
        if self.janelaPrincipal.TelaCheia is True:
            self.janelaPrincipal.showFullScreen()
        else:
            self.janelaPrincipal.showNormal()
        self.janelaPrincipal.activateWindow()
        self.janelaPrincipal.txt_login.setFocus()


class TelaHistoricoDeUso(QMainWindow):

    def __init__(self, janelaPrincipal, parent=None):
        super(TelaHistoricoDeUso, self).__init__(parent)
        uic.loadUi('GUI/telaHistDeUso.ui', self)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))

        self.janelaPrincipal = janelaPrincipal
        self.popular_combobox()

        self.cbx_logins.activated.connect(self.login_selecionado)
        self.cbx_grupos.activated.connect(self.grupo_selecionado)


    def popular_combobox(self):
        self.cbx_logins.clear()
        self.cbx_logins.addItem("Selecione o usuário:")
        self.cbx_logins.addItem("Todos os usuarios")
        # todos_usuarios = self.janelaPrincipal.db_usuario.check_todos_usuarios_do_equip('LaserCutter')
        todos_usuarios = self.janelaPrincipal.db.check_todos_usuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_usuarios)
        # todos_superusuarios = self.janelaPrincipal.db_usuario.check_todos_superusuarios_do_equip('LaserCutter')
        todos_superusuarios = self.janelaPrincipal.db.check_todos_superusuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_superusuarios)    


        self.cbx_grupos.clear()
        self.cbx_grupos.addItem("Selecione o grupo de pesquisa ou orientador:")
        todos_grupos = self.janelaPrincipal.db.check_todos_grupos_do_equip()
        self.cbx_grupos.addItems(todos_grupos)

    def get_uso_login(self, login):
        dados = self.janelaPrincipal.db.check_uso_equip(login)
        nome = self.janelaPrincipal.db.get_nome_from_login(login)

        if dados == []:
            uso_txt = "Usuário ainda não usou o equipamento."
            tempo_total = ""
            return nome, uso_txt, tempo_total

        uso_txt = self.txt_uso.toPlainText()
        uso_txt += "### Usuário: " + nome + " ###\r\n"
        uso_txt += '   Dia      -   Tempo de Uso  -  Situação'
        tempo_total = self.lbl_tempo_total.text()
        for linha in dados:
            uso_txt += '\r\n'
            dia = linha[2][-19:-9] 
            tempo_de_uso = linha[4]
            situacao = linha[5]
            if tempo_de_uso is None:
                uso_txt += dia + ' - Equipamento ainda em uso' + ' - ' + str(situacao) 
                tempo_total = tempo_total + ' + Em uso'
            else:        
                uso_txt += dia + ' - ' + tempo_de_uso + '     -     ' + str(situacao)
                tempo_total = self.somar_tempo(tempo_total,tempo_de_uso)
        uso_txt+='\r\n##########################\r\n\r\n'


        self.lbl_nome.setText(nome)
        self.txt_uso.setText(uso_txt)
        self.lbl_tempo_total.setText(tempo_total)


    def get_uso_id(self, id):
        dados = self.janelaPrincipal.db.check_uso_equip_id(id)
        nome = self.janelaPrincipal.db.get_nome_from_id(id)

        uso_txt = self.txt_uso.toPlainText()
        tempo_total = self.lbl_tempo_total.text()
        for linha in dados:
            uso_txt += '\r\n'
            dia = linha[2][-19:-9] 
            tempo_de_uso = linha[4]
            situacao = linha[5]
            if tempo_de_uso is None:
                uso_txt += nome + ' - ' + dia + ' - Equipamento ainda em uso' + ' - ' + str(situacao) 
                tempo_total = tempo_total + ' + Em uso'
            else:        
                uso_txt += nome + ' - ' + dia + ' - ' + tempo_de_uso + '     -     ' + str(situacao)
                tempo_total = self.somar_tempo(tempo_total,tempo_de_uso)


        self.lbl_nome.setText(nome)
        self.txt_uso.setText(uso_txt)
        self.lbl_tempo_total.setText(tempo_total)

    def login_selecionado(self, idx):
        self.cbx_grupos.clear()
        self.cbx_grupos.addItem("Selecione o grupo de pesquisa ou orientador:")
        todos_grupos = self.janelaPrincipal.db.check_todos_grupos_do_equip()
        self.cbx_grupos.addItems(todos_grupos)
        
        self.txt_uso.setText("")
        self.lbl_tempo_total.setText('00:00:00')

        login = self.cbx_logins.currentText()
        if login == "Selecione o usuário:":
            return
        elif login == "Todos os usuarios":
            linhas = self.janelaPrincipal.db.todas_linhas_de_uso(self.janelaPrincipal.equipamento)
            self.txt_uso.setText("Usuario - Dia - Tempo - Situacao")
            for linha in linhas:
                self.get_uso_id(linha[0])
                self.lbl_email.setText("Todos os usuarios.")
                self.lbl_grupo.setText("Todos os usuarios.")
            return
        # dados = self.janelaPrincipal.db_usuario.check_usuario(login)
        email = self.janelaPrincipal.db.get_email_from_login(login)
        grupo = self.janelaPrincipal.db.get_grupo_from_login(login)
        self.lbl_email.setText(email)
        self.lbl_grupo.setText(grupo)
        self.get_uso_login(login)


        
    def somar_tempo(self, tempo1, tempo2):      
        t1_seg = int(tempo1[-2:])
        t1_min = int(tempo1[-5:-3])
        t1_hora = int(tempo1[-8:-6])
        t2_seg = int(tempo2[-2:])
        t2_min = int(tempo2[-5:-3])
        t2_hora = int(tempo2[-8:-6])

        seg = t1_seg + t2_seg        
        min_extra = seg/60
        seg = int(seg%60)
        min = t1_min + t2_min + min_extra
        hora_extra = min/60
        min = int(min%60)
        hora = int(t1_hora + t2_hora + hora_extra)

        if seg < 10:
            s = '0' + str(seg)
        else:
            s = str(seg)               
        if min < 10:
            m = '0' + str(min)
        else:
            m = str(min)
        if hora < 10:
            h = '0' + str(hora)
        else:
            h = str(hora)      

        return h + ':' + m + ':' + s


    def grupo_selecionado(self, idx):
        self.cbx_logins.clear()
        self.cbx_logins.addItem("Selecione o usuário:")
        self.cbx_logins.addItem("Todos os usuarios")
        # todos_usuarios = self.janelaPrincipal.db_usuario.check_todos_usuarios_do_equip('LaserCutter')
        todos_usuarios = self.janelaPrincipal.db.check_todos_usuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_usuarios)
        # todos_superusuarios = self.janelaPrincipal.db_usuario.check_todos_superusuarios_do_equip('LaserCutter')
        todos_superusuarios = self.janelaPrincipal.db.check_todos_superusuarios_do_equip('LaserCutter')
        self.cbx_logins.addItems(todos_superusuarios)    

        grupo = self.cbx_grupos.currentText()
        if grupo == "Selecione o grupo de pesquisa ou orientador:":
            return
        usuarios = self.janelaPrincipal.db.check_todos_usuarios_do_grupo(grupo)
        self.txt_uso.setText("")
        self.lbl_tempo_total.setText('00:00:00')
        for login in usuarios:
            self.get_uso_login(login)

        self.lbl_nome.setText('Todos os usuários do mesmo grupo ou orientador.')
        self.lbl_email.setText("")
        self.lbl_grupo.setText(grupo)



    def closeEvent(self, event):

        self.lbl_nome.setText("")
        self.lbl_grupo.setText("")
        self.lbl_email.setText("")
        self.txt_uso.setText("")
        self.lbl_tempo_total.setText("")


        self.janelaPrincipal.permitir_min = False
        if self.janelaPrincipal.TelaCheia is True:
            self.janelaPrincipal.showFullScreen()
        else:
            self.janelaPrincipal.showNormal()
        self.janelaPrincipal.activateWindow()
        self.janelaPrincipal.txt_login.setFocus()


class NovoUsuario(QMainWindow):

    def __init__(self, janelaPrincipal, parent=None):
        super(NovoUsuario, self).__init__(parent)
        uic.loadUi('GUI/telaRegistrarNovo.ui', self)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))

        self.janelaPrincipal = janelaPrincipal
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password_2.returnPressed.connect(self.get_login_pass)
        self.btn_sair.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.get_login_pass)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))

    def get_login_pass(self):
        login = self.txt_login.text()
        nome = self.txt_nome.text()
        email = self.txt_email.text()
        grupo = self.txt_grupoPesq.text()
        password = self.txt_password.text()
        password2 = self.txt_password_2.text()
        self.txt_login.setText('')
        self.txt_nome.setText('')
        self.txt_email.setText('')
        self.txt_password.setText('')   
        self.txt_password_2.setText('')
        self.txt_grupoPesq.setText('')

        # dados = self.janelaPrincipal.db_usuario.check_usuario(login)
        dados = self.janelaPrincipal.db.check_usuario(login)
        if dados != []:
            QMessageBox.about(self, "Usuário já existe!", "Todos os dados deste usuário serão recadastrados.")

        if login != "" and password == password2:
            password = cript.hash_password(password)

            senha_autorizacao, ok = QInputDialog.getText(
                self, "Aguardando autorização...", "Senha de autorização:",
                QtWidgets.QLineEdit.Password)
            if ok:
                if cript.check_autorizacao(senha_autorizacao):
                    if dados != []:
                        self.janelaPrincipal.db.remove_usuario_para_recadastro(login)

                    self.janelaPrincipal.db.add_novo_usuario(
                        None, login, nome, email, password, "Administrador", grupo)
                    self.janelaPrincipal.db.add_autorizacao_equip(
                        login, nome, self.janelaPrincipal.equipamento)
                    QMessageBox.about(self, "OK!", "Cadastro realizado!")

                else:
                    QMessageBox.about(self, "Erro!",
                                      "Senha de autorização não confere!")
                    self.txt_login.setText(login)
                    self.txt_nome.setText(nome)
                    self.txt_email.setText(email)
                    self.txt_grupo.setText(grupo)
                    self.txt_password.setText(password2)
                    self.txt_password_2.setText(password2)

            else:
                QMessageBox.about(self, "Erro!", "Cadastro não realizado! ")

        else:
            QMessageBox.about(self, "Erro!", "Senha não confere!")
            self.txt_login.setText(login)
            self.txt_nome.setText(nome)
            self.txt_email.setText(email)

    def closeEvent(self, event):
        self.janelaPrincipal.permitir_min = False
        if self.janelaPrincipal.TelaCheia is True:
            self.janelaPrincipal.showFullScreen()
        else:
            self.janelaPrincipal.showNormal()
        self.janelaPrincipal.activateWindow()
        self.janelaPrincipal.txt_login.setFocus()


class TempoUso(QMainWindow):

    def __init__(self, janelaPrincipal, usuario, parent=None):
        super(TempoUso, self).__init__(parent)
        uic.loadUi('GUI/telaTempoUso.ui', self)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))
        self.login = usuario
        self.janelaPrincipal = janelaPrincipal
        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(1000)
        self.checkThreadTimer.timeout.connect(self.update)
        self.checkThreadTimer.start()
        self.tempo_seg = 0
        self.tempo_min = 0
        self.tempo_hora = 0
        self.tempo_de_uso = 0

        # email = self.janelaPrincipal.db_usuario.get_email(self.login)
        email = self.janelaPrincipal.db.get_email_from_login(self.login)
        nome = self.janelaPrincipal.db.get_nome_from_login(self.login)
        self.lbl_usuario.setText("Em uso por: " + nome + "\n(" + email +
                                 ")")

        self.btn_sair.clicked.connect(self.close)
        self.btn_comentario.clicked.connect(self.comentar)
        self.setWindowIcon(QtGui.QIcon('./imagens/icon.png'))

    def comentar(self):
        comentario = self.txt_comentario.toPlainText()
        self.janelaPrincipal.db.set_comentario(
            self.login, self.janelaPrincipal.equipamento, comentario)
        self.txt_comentario.setText("")
        QMessageBox.about(self, "Comentário!", "Comentário inserido no banco de dados.")


    def update(self):
        self.tempo_seg += 1
        if self.tempo_seg % 60 == 0:
            self.tempo_seg = 0
            self.tempo_min += 1
            if self.tempo_min % 60 == 0:
                self.tempo_min = 0
                self.tempo_hora += 1
        if self.tempo_seg < 10:
            s = '0' + str(self.tempo_seg)
        else:
            s = str(self.tempo_seg)               
        if self.tempo_min < 10:
            m = '0' + str(self.tempo_min)
        else:
            m = str(self.tempo_min)
        if self.tempo_hora < 10:
            h = '0' + str(self.tempo_hora)
        else:
            h = str(self.tempo_hora)                
        self.tempo_de_uso = h + ':' + m + ':' + s
        self.lbl_tempo.setText(self.tempo_de_uso)
        self.setWindowTitle(self.tempo_de_uso)
        if self.tempo_seg % 60 == 0:
            if self.janelaPrincipal.servidorFTP is True:
                self.janelaPrincipal.lbl_info.setText("Salvando no servidor FTP...")
            self.janelaPrincipal.db.set_hora_fim_seguranca(
                self.login, self.janelaPrincipal.equipamento, self.tempo_de_uso)

    def closeEvent(self, event):
        texto = "Finalizar o uso do equipamento?"
        reply = QMessageBox.question(self, 'Sair?', texto, QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.checkThreadTimer.stop()
            self.tempo_seg = 0
            self.tempo_min = 0
            self.tempo_hora = 0
            if self.janelaPrincipal.servidorFTP is True:
                self.janelaPrincipal.lbl_info.setText(
                    "Salvando no servidor FTP...")
            self.janelaPrincipal.db.set_hora_fim(
                self.login, self.janelaPrincipal.equipamento, self.tempo_de_uso)
            self.tempo_de_uso = 0
            self.janelaPrincipal.permitir_min = False
            time.sleep(1)
            if self.janelaPrincipal.TelaCheia is True:
                self.janelaPrincipal.showFullScreen()
            else:
                self.janelaPrincipal.showNormal()
            self.janelaPrincipal.activateWindow()
            self.janelaPrincipal.txt_login.setFocus()



        else:
            event.ignore()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    splash_pix = QtGui.QPixmap('./imagens/splashscreen.png')
    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    time.sleep(5)
    splash.close()
    app.processEvents()

    dmw = DesignerMainWindow()

    if dmw.TelaCheia is True:
        dmw.showFullScreen()
    else:
        dmw.showNormal()
    dmw.activateWindow()
    dmw.txt_login.setFocus()

    sys.exit(app.exec_())


#%%
