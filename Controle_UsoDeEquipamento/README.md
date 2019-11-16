# Controle de Uso de Equipamento

Utilize esse programa para criar um banco de dados contendo registro de usuários e um logbook do uso de equipamento.

## Configurações

Ao rodar o programa pela primeira vez, será realizado o cadastro do administrador do programa.

Com checkbox TelaCheia selecionado, fica praticamente impossível de fechar o programa sem ser usuário cadastrado (se descobrir uma forma, me avise!). :) 

A ideia é realmente dificultar fechar o programa. 

## (RPI) Passo a passo para que o programa seja inicializado automaticamente:

  - Rodar o programa a primeira vez e cadastrar o administrador.
  - Após criar a conta de administrador, o programa já alterou o sistema para a inicialização automática. Caso não estea inicializando automaticamente, siga os passos abaixo.

### A PRINCÍPIO NÃO PRECISA MAIS FAZER OS PASSOS ABAIXO. AGORA TUDO ESTÁ SENDO FEITO NA INICIALIZAÇÃO DO ADMINISTRADOR. (DEIXANDO AQUI APENAS PARA REFERÊNCIA)

- Ajeitar o caminho do arquivo "start_python.sh" nas linhas 2 e 3
- Ex.:
```
cd /home/pi/Documents/registro-de-uso-presenca-lab/Controle_UsoDeEquipamento
/usr/bin/python3 RegistroDeUso.py
```          
- Ajeitar o caminho do arquivo "RegistroDeUso.service" na linha 7
- Ex.:
```
 ExecStart=/home/pi/start_python.sh 
```          
- copiar serviço para a pasta correta
- Ex.:
```
sudo cp RegistroDeUso.service \etc\system\systemd\RegistroDeUso.service
```          

- Habilitar o serviço:
```
sudo systemctl enable RegistroDeUso.service
```          



## (Windows) Passo a passo para que o programa seja inicializado automaticamente:
  - Rodar o programa a primeira vez e cadastrar o administrador.
  - Após criar a conta de administrador, copiar o arquivo "Run_RegistroDeUso.bat" gerado anteriormente para a pasta de Startup: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"


### NÃO PRECISA MAIS FAZER OS PASSOS ABAIXO. AGORA QUASE TUDO ESTÁ SENDO FEITO NA INICIALIZAÇÃO DO ADMINISTRADOR. (DEIXANDO AQUI APENAS PARA REFERÊNCIA)

Escolha um dos dois jeitos abaixo:
### Jeito 1

  - Associar o pythonw.exe para abrir as extensões .pyw
  - Após cadastrar o Administrador, copiar o arquivo "RegistroDeUso - Atalho" para a pasta de Startup
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

O programa tem que estar instalado em C:\Program Files\AutoHotkey\AutoHotkey.exe



G. M. Penello, 2019
gpenello@gmail.com