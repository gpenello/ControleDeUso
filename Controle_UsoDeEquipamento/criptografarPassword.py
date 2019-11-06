# https://www.pythoncentral.io/hashing-strings-with-python/

autorizacao = 'b88de78649ba8e368a50bec9b0e36c08d39e0d5b6dc99077df95dc8e38194396:000df336c93646ac9a5df307ed6c325a'

import uuid
import hashlib


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() +
                          password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() +
                                      user_password.encode()).hexdigest()

def check_autorizacao(senha_autorizacao):
    password, salt = autorizacao.split(
        ':')
    return password == hashlib.sha256(salt.encode() +
                                      senha_autorizacao.encode()).hexdigest()
    
                                      
if __name__ == '__main__':
    import re  # https://www.debuggex.com/cheatsheet/regex/python    
    import getpass
    import sys
    password_velho = getpass.getpass(prompt='Password antigo do administrador (a ser substituido): ')
    password_novo = getpass.getpass(prompt='Definir novo password para o administrador: ')
    password_novo2 = getpass.getpass(prompt='Repetir novo password para o administrador: ')
    if password_novo == password_novo2:
        hashed_password = hash_password(password_novo)
    
        with open(sys.argv[0], 'r', encoding='utf-8') as f:
            old_code = f.read()
        
        if check_autorizacao(password_velho):
        
            password_antigo = re.findall('autorizacao = (.*)', old_code)

            new_code = old_code.replace('autorizacao = ' + password_antigo[0],
                                        "autorizacao = '" + hashed_password + "'")

            with open(sys.argv[0], mode='w', encoding='utf-8') as f:
                f.write(new_code)
            print("Senha do administrador foi atualizada!")    
        else:
            print("Erro! Senha do administrador não confere! Tente novamente.")            
    else:
        print("Erro! Senhas repetidas não conferem!")                