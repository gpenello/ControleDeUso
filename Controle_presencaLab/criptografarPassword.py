# https://www.pythoncentral.io/hashing-strings-with-python/

autorizacao = '58350f5fc3e0b7289c8555b0b6ef898d42f0cbe8d555db1768f550dd8ab85b46:20e313933f3742dfa882ee11c63e2f85'

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
            print("Senha do adminisrador foi atualizada!")    
        else:
            print("Erro! Senha do administrador não confere! Tente novamente.")            
    else:
        print("Erro! Senhas repetidas não conferem!")                