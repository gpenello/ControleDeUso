# Controle de Uso de Equipamento

Utilize esse programa para criar um banco de dados contendo registro de usuários e um logbook do uso de equipamento.

## Passo a passo para que o programa seja inicializado automaticamente em Windows:
Escolha um dos dois jeitos abaixo:
### Jeito 1
  - Criar um arquivo de atalho do RegistroDeUso.pyw
  - Associar o pythonw.exe para abrir as extensões .pyw
  - Copiar o atalho gerado anteriormente (ex. "RegistroDeUso.pyw - Shortcut") para a pasta de Startup
  - Ex.: 
   - Executável em "C:\Users\gpenello\Miniconda3\pythonw.exe"
   - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

### Jeito 2  
  - Criar um arquivo RunRegistroDeUso.bat com o conteúdo:
```
"C:\Users\gpenello\Miniconda3\python.exe" "D:\OneDrive - IF-UFRJ\UFRJ\Programas\Python\registro-de-uso-presenca-lab\Controle_UsoDeEquipamento\RegistroDeUso.py"
pause
```          
  - Copiar o arquivo .bat gerado anteriormente para a pasta de Startup
  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"


## Instalar AutoHotKey (Windows) 
Importante para desabilitar os comandos alt+tab, windows+tab e CTRL+Esc dos teclados
 - https://www.autohotkey.com/


## Configurações

Ajeite as variáveis "TelaCheia" e "equipamento" no arquivo RegistroDeUso.pyw antes de rodar o programa e coloque o caminho completo do programa que quer que abra ao fazer o login:
Exemplo:
```
    equipamento = 'LaserCutter' 
    TelaCheia = True
    software_externo_path = '/home/pi/Documents/registro-de-uso-presenca-lab/K40_Whisperer-0.37_src/k40_whisperer.py'
```

Com "TelaCheia = True", fica praticamente impossível de fechar o programa sem ser usuário cadastrado (se descobrir uma forma, me avise!). :) 

A única maneira de fechar o programa é usando o gerenciador de tarefas para fechar o terminal de python que está rodando o programa. Se descobrir outra forma, me avise. :)
A ideia é realmente dificultar fechar o programa. Só é para fazer isso caso realmente desejado pelo usuário.

- (Não precisa mais fazer esse passo. Primeiro uso do programa cria botão para criar administrador) Para alterar a senha do administrador, rodar o arquivo "criptografarPassword.py". 

- (Agora existem outras formas de fazer isso.) Para minimizar a tela, use o nome 'admin' como usuário e a senha do administrador como password.

G. M. Penello, 2019
gpenello@gmail.com