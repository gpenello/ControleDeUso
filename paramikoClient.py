import paramiko


class Client():

    def __init__(self):
        self.client = paramiko.SSHClient()

    def conectar(self, host='raspberrypi.local', username='pi', password='raspberry'):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # talvez usar apenas na primeira vez que rodar
        self.client.connect(host, username=username, password=password)
        self.stdin = None
        self.stdout = None
        self.stderr = None

    # executando comandos na máquina remota
    # stdin, stdout, stderr = client.exec_command('cd ..; sudo ls')
    # stdin.write('lab2\n')
    def executar_comando(self, comando='ls'):
        self.stdin, self.stdout, self.stderr = self.client.exec_command(comando)
        # print('##############3')
        # print(self.stdout.readlines())
        # print(self.stderr.readlines())
        # print('##############3')

    def executar_comando_sudo(self, comando='ls', password="raspberry"):
        self.stdin, self.stdout, self.stderr = self.client.exec_command("sudo " + comando)
        self.stdin.write(password + '\n')
        # print('##############3')
        # print(self.stdout.readlines())
        # print(self.stderr.readlines())
        # print('##############3')

    def baixar_arquivo(self, path_file_origem, path_file_destino):
        baixar = self.client.open_sftp()
        # client.get('/home/pi/Documents/conectando.py','conectando3.py')
        baixar.get(path_file_origem, path_file_destino)
        baixar.close()

    def enviar_arquivo(self, path_file_origem, path_file_destino):
        enviar = self.client.open_sftp()
        # client.put('conectando.py','/home/pi/Documents/conectando.py')
        enviar.put(path_file_origem, path_file_destino)
        enviar.close()

    def fechar_cliente(self):
        self.client.close()


if __name__ == "__main__":
    client = Client()
    client.conectar('raspberrypi.local', 'pi', 'lab2')
    client.executar_comando('ls')
    if 'Registros de uso\n' not in client.stdout:
        client.executar_comando('mkdir "Registros de uso"')
    arquivo = "BancoDeDados_Lab.py"
    client.enviar_arquivo(arquivo, 'Registros de uso/' + arquivo)
    client.fechar_cliente()
