# Controle de Uso de Equipamento

Utilize esse programa para criar um banco de dados contendo registro de usuários e um logbook do uso de equipamento.

## Configurações

Ao rodar o programa pela primeira vez, será realizado o cadastro do administrador do programa.


Com "TelaCheia = True", fica praticamente impossível de fechar o programa sem ser usuário cadastrado (se descobrir uma forma, me avise!). :) 

A única maneira de fechar o programa é usando o gerenciador de tarefas para fechar o terminal de python que está rodando o programa. Se descobrir outra forma, me avise. :)
A ideia é realmente dificultar fechar o programa. Só é para fazer isso caso realmente desejado pelo usuário.

## (RPI) Passo a passo para que o programa seja inicializado automaticamente:
- 

## (Windows) Passo a passo para que o programa seja inicializado automaticamente:
Escolha um dos dois jeitos abaixo:
### Jeito 1
  - Criar um arquivo de atalho do RegistroDeUso.pyw
  - Associar o pythonw.exe para abrir as extensões .pyw
  - Copiar o atalho gerado anteriormente (ex. "RegistroDeUso.pyw - Shortcut") para a pasta de Startup
  - Ex.: 
   - Executável em "C:\Users\gpenello\Miniconda3\pythonw.exe"
   - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

### Jeito 2  
  - Criar um arquivo RunRegistroDeUso.bat para inicializar o programa.
  Ex.:
```
"C:\Users\gpenello\Miniconda3\python.exe" "D:\OneDrive - IF-UFRJ\UFRJ\Programas\Python\registro-de-uso-presenca-lab\Controle_UsoDeEquipamento\RegistroDeUso.py"
pause
```          
  - Copiar o arquivo .bat gerado anteriormente para a pasta de Startup
  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"


## (Windows) Instalar o programa AutoHotKey  
Importante para desabilitar os comandos alt+tab, windows+tab e CTRL+Esc dos teclados
 - https://www.autohotkey.com/


G. M. Penello, 2019
gpenello@gmail.com