#!/usr/bin/python3
# -*- coding: utf-8 -*-

# https://www.raspberrypi.org/forums/viewtopic.php?t=43509

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QInputDialog, QMessageBox, QDesktopWidget, QSplashScreen
import sys
import time

import criptografarPassword as cript
from BancoDeDados_Lab import BancoDeDados

import time
from threading import Thread
from pirc522 import RFID
'''
# Pinos para o RFID(Board):
1, 6, 18, 19, 21, 22, 23, 24
'''
# alternativa ao threading
# QtCore.QThread

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class Leitura_Cartoes(QtCore.QThread):
#class Leitura_Cartoes():
    # https://pimylifeup.com/raspberry-pi-rfid-rc522/
    
    sig = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.bool_run = True
        self.rfid = RFID()
        
    def parar_leitura(self):
        self.bool_run = False
        
    def voltar_leitura(self):
        self.bool_run = True
    
    def run(self):
        while True:
            if self.bool_run is True:
                # Verifica se existe uma tag próxima do módulo
                (error, tag_type) = self.rfid.request()
                if not error:
                    (error, uid) = self.rfid.anticoll()
                    if not error:
                        uid = ':'.join(['%X' % x for x in uid])
                        uid = str(uid)
                        print(uid)
                        self.sig.emit(uid)
                        self.bool_run = False



class DesignerMainWindow(QMainWindow):
    servidorFTP = True
    TelaCheia = True
    equipamento = 'RPi'  # colocar o nome do equipamento do arquivo db
    host, user, senha = ('raspberrypi.local', 'pi', 'lab2')

    # -----------------------------------------------
    # falta implementar o rpi registrando presença e compartilhando isso com
    # todos os outros pcs conectados a ele. Tenho ainda que fazer este programa
    forcar_presenca = False

    # -----------------------------------------------

    def __init__(self, parent=None):
        
        self.sair = False
        arquivo = os.path.join(dir_path, 'log/BancoDeDados_Usuarios.db')
        self.db = BancoDeDados(arquivo)
        self.novoUsuario = NovoUsuario(self)
        self.ler_cartao = Leitura_Cartoes()
        self.janelaAddTag = AddTag(self)
        
        self.ler_cartao.start()
        self.ler_cartao.sig.connect(self.tag_lido)
        
        self.inserindo_novo_tag = False
        self.nome_do_novo_tag = ""

        super(DesignerMainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(dir_path, 'GUI/telaControle_presenca.ui'), self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        #        self.setWindowFlags()
        self.btn_novo.clicked.connect(self.cadastrarNovoUsuario)
        self.btn_addTag.clicked.connect(self.addTag)
        # self.btn_sair.clicked.connect(self.fechar)
        self.center()
        self.permitir_min = False
        self.setWindowIcon(QtGui.QIcon(os.path.join(dir_path,'imagens/icon.png')))
        self.update_listaPresentes()

    def update_listaPresentes(self):
        self.cBox_listaPresentes.clear()
        usuarios = self.db.check_lista_presentes()
        self.cBox_listaPresentes.addItems(["Lista de presentes:"]+usuarios)
        model = self.cBox_listaPresentes.model()
        for idx in range(len(usuarios)):
            self.cBox_listaPresentes.model().item(idx+1).setEnabled(False)
            self.cBox_listaPresentes.model().item(idx+1).setForeground(QtGui.QColor('black'))
        
        
    def tag_lido(self, tag):
        if self.inserindo_novo_tag is True:
            resposta = self.db.set_tag(self.nome_do_novo_tag, tag)
            if resposta is True:
                self.nome_do_novo_tag = ""
                self.janelaAddTag.lbl_instrucao.setText("OK!")
            else:
                self.nome_do_novo_tag = ""
                self.janelaAddTag.lbl_instrucao.setText("Erro! Tag já em utilização por outro usuário?" )
        else:
            nome = self.db.get_nome_from_tag(tag)
            if nome == "Tag sem nome associado":
                self.lbl_leituraTag.setText("Não reconhecido, não há nome associado a este tag!")
            else:
                resposta = self.db.set_entrada_ou_saida(tag)
                self.lbl_leituraTag.setText("Usuário: "+ nome + "\n" + resposta)
        
        app.processEvents()
        QtCore.QTimer.singleShot(4000, self.voltar_a_ler_tag)
        self.db.export_all_db_to_csv()
        self.update_listaPresentes()
    
            
    def voltar_a_ler_tag(self):
        self.ler_cartao.voltar_leitura()
        self.lbl_leituraTag.setText("Aproxime seu tag...")
            

    def remover_tag_do_nome(self, nome):
        self.db.remove_tag(nome)

            
    def addTag(self):
        self.ler_cartao.bool_run = False
        senha_autorizacao, ok = QInputDialog.getText(
            self, "Aguardando autorização...", "Senha de autorização:",
            QtWidgets.QLineEdit.Password)
        if ok:
            if cript.check_autorizacao(senha_autorizacao):
                self.keep_minimized()
                self.janelaAddTag.show()
                self.janelaAddTag.activateWindow()
                self.inserindo_novo_tag = True
                self.janelaAddTag.popular_usuarios()
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha de autorização não confere!")
                self.ler_cartao.bool_run = True

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

    def get_nome_pass(self):
        nome = self.txt_nome.text()
        password = self.txt_password.text()
        self.txt_nome.setText('')
        self.txt_password.setText('')
        dados_usuario = self.db.check_usuario(nome)
        if nome == 'admin':
            if cript.check_autorizacao(password):
                self.permitir_min = True
                self.showMinimized()
                time.sleep(1)
                self.permitir_min = False
            else:
                QMessageBox.about(self, "Erro!",
                                  "Senha do administrador não confere!")
        elif dados_usuario != []:
            if self.forcar_presenca is True:
                nome_presente = self.db.check_nome_presenca_em_aberto(nome)
                if nome_presente is False:
                    QMessageBox.about(
                        self, "Erro!",
                        str("Marque presença no lab. antes de utilizar os " +
                            "equipamentos!"))
                    return
            if cript.check_password(dados_usuario[-1], password):
                disponivel, nome_usando = self.db.set_hora_inicio(
                    nome, self.equipamento)
                if not disponivel:
                    texto = nome_usando + \
                        ' está usando este equipamento. Deseja forçar a saída dele?'
                    reply = QMessageBox.question(self, 'Equipamento em uso!',
                                                 texto, QMessageBox.Yes,
                                                 QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.db.force_hora_fim(nome, self.equipamento)
                        self.db.set_hora_inicio(nome, self.equipamento)
                        self.janelatempo = TempoUso(self, nome)
                        self.janelatempo.show()
                        self.janelatempo.activateWindow()
                        self.keep_minimized()

                else:
                    self.db.set_hora_inicio(nome, self.equipamento)
                    self.janelatempo = TempoUso(self, nome)
                    self.janelatempo.show()
                    self.janelatempo.activateWindow()
                    self.keep_minimized()
            else:
                QMessageBox.about(self, "Erro!", str("Senha não confere!"))
        else:
            QMessageBox.about(self, "Erro!", "Usuário não cadastrado!")

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
                self.bool_run = True

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

    def closeEvent(self, event):
        if self.sair is False:
            event.ignore()


class NovoUsuario(QMainWindow):

    def __init__(self, janelaPrincipal, parent=None):
        super(NovoUsuario, self).__init__(parent)
        uic.loadUi(os.path.join(dir_path,'GUI/telaRegistrarNovo.ui'), self)
        self.janelaPrincipal = janelaPrincipal
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password_2.returnPressed.connect(self.get_nome_pass)
        self.btn_sair.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.get_nome_pass)
        self.setWindowIcon(QtGui.QIcon(os.path.join(dir_path,'imagens/icon.png')))

    def get_nome_pass(self):
        nome = self.txt_nome.text()
        email = self.txt_email.text()
        password = self.txt_password.text()
        password2 = self.txt_password_2.text()
        self.txt_nome.setText('')
        self.txt_email.setText('')
        self.txt_password.setText('')
        self.txt_password_2.setText('')

        dados = self.janelaPrincipal.db.check_usuario(nome)
        if dados != []:
            QMessageBox.about(self, "Erro!", "Usuário já existe!")
            return

        if nome != "" and password == password2:
            password = cript.hash_password(password)

            senha_autorizacao, ok = QInputDialog.getText(
                self, "Aguardando autorização...", "Senha de autorização:",
                QtWidgets.QLineEdit.Password)
            if ok:
                if cript.check_autorizacao(senha_autorizacao):
                    self.janelaPrincipal.db.add_novo_usuario(
                        None, nome, email, password, "Administrador")
                    self.janelaPrincipal.db.add_autorizacao_nome_equip(
                        nome, self.janelaPrincipal.equipamento)
                    QMessageBox.about(self, "OK!", "Cadastro realizado!")
                else:
                    QMessageBox.about(self, "Erro!",
                                      "Senha de autorização não confere!")
                    self.txt_nome.setText(nome)
                    self.txt_email.setText(email)
                    self.txt_password.setText(password2)
                    self.txt_password_2.setText(password2)

            else:
                QMessageBox.about(self, "Erro!", "Cadastro não realizado!")

        else:
            QMessageBox.about(self, "Erro!", "Senha não confere!")
            self.txt_nome.setText(nome)
            self.txt_email.setText(email)

    def closeEvent(self, event):
        self.janelaPrincipal.permitir_min = False
        if self.janelaPrincipal.TelaCheia is True:
            self.janelaPrincipal.showFullScreen()
        else:
            self.janelaPrincipal.showNormal()
        self.janelaPrincipal.activateWindow()
        


class AddTag(QMainWindow):

    def __init__(self, janelaPrincipal, parent=None):
        super(AddTag, self).__init__(parent)
        uic.loadUi(os.path.join(dir_path,'GUI/tela_addTag.ui'), self)
        self.janelaPrincipal = janelaPrincipal
        self.btn_sair.clicked.connect(self.close)
        self.btn_removerTag.clicked.connect(self.removerTag)
        self.btn_removerTag.setEnabled(False)
        self.comboBox.activated.connect(self.selectionchange)
    
    def removerTag(self):
        self.janelaPrincipal.ler_cartao.bool_run = False       
        nome = self.comboBox.currentText()
        self.janelaPrincipal.remover_tag_do_nome(nome)
        self.lbl_instrucao.setText("Tag removido do usuário " + nome)    
        QtCore.QTimer.singleShot(3000, self.popular_usuarios)
        
    def selectionchange(self, idx):
        nome = self.comboBox.currentText()
        if nome == "Selecione o usuário:":
            self.janelaPrincipal.ler_cartao.bool_run = False       
            self.lbl_instrucao.setText(
                "Aguarde  para aproximar o tag a ser cadastrado.")
        else:
            self.janelaPrincipal.ler_cartao.bool_run = True       
            self.lbl_instrucao.setText(nome +
                                       " aproxime seu tag para cadastrar.")
            self.btn_removerTag.setEnabled(True)                                       
            self.janelaPrincipal.nome_do_novo_tag = nome
            QtCore.QTimer.singleShot(30000, self.popular_usuarios)
    
    def popular_usuarios(self):
        self.comboBox.clear()
        usuarios = ["Selecione o usuário:"
                    ] + self.janelaPrincipal.db.check_lista_usuarios()
        self.comboBox.addItems(usuarios)
        self.lbl_instrucao.setText(
                "Aguarde  para aproximar o tag a ser cadastrado.")
        self.janelaPrincipal.ler_cartao.bool_run = False       
        self.btn_removerTag.setEnabled(False)
        
    def closeEvent(self, event):
        self.janelaPrincipal.permitir_min = False
        time.sleep(1)
        if self.janelaPrincipal.TelaCheia is True:
            self.janelaPrincipal.showFullScreen()
        else:
            self.janelaPrincipal.showNormal()
        self.janelaPrincipal.activateWindow()
        self.janelaPrincipal.inserindo_novo_tag = False
        self.janelaPrincipal.ler_cartao.bool_run = True       
        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    splash_pix = QtGui.QPixmap(os.path.join(dir_path,'imagens/splashscreen.png'))
    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    time.sleep(3)
    splash.close()
    app.processEvents()

    dmw = DesignerMainWindow()

    if dmw.TelaCheia is True:
        # dmw.resize(1280, 800);
        # dmw.setWindowState(QtCore.Qt.WindowFullScreen)
        dmw.showFullScreen()
    else:
        dmw.showNormal()
    dmw.activateWindow()

    sys.exit(app.exec_())
