Passo a passo para que o programa seja inicializado automaticamente (dois jeitos):

Jeito 1)  - Criar um arquivo de atalho do RegistroDeUso.py
    	  - Associar o python.exe para abrir as extensões .py
	    - Ex.: Execut�vel em "C:\Users\gpenello\Miniconda3\python.exe"
          - Copiar o atalho gerado anteriormente (ex. "RegistroDeUso.pyw - Shortcut") para a pasta de Startup
	  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

Jeito 2)  - Criar um arquivo RunRegistroDeUso.bat com o conteúdo:

"C:\Users\gpenello\Miniconda3\python.exe" "D:\OneDrive - IF-UFRJ\UFRJ\Programas\Python\registro-de-uso-presenca-lab\Controle_UsoDeEquipamento\RegistroDeUso.py"
pause
          
          - Copiar o arquivo .bat gerado anteriormente para a pasta de Startup
	  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"


Instalar AutoHotKey para desabilitar os comandos alt+tab e windows+tab dos teclados

Para alterar a senha do administrador, rodar o arquivo "criptografarPassword.py".
Para minimizar a tela, use o nome 'admin' como usuário e a senha do administrador como password.

A única maneira de fechar o programa é usando o gerenciador de tarefas para fechar o terminal de python que está rodando o programa. Se descobrir outra forma, me avise. :)
A ideia é realmente dificultar fechar o programa. Só é para fazer isso caso realmente desejado pelo usuário.


Ajeite as variáveis "TelaCheia" e "equipamento" antes de rodar o programa. 
TelaCheia = True/False --> escolha um dos dois
equipamento = "Nome do equipamento desejado"

Com "TelaCheia = True", fica praticamente impossível de fechar o programa sem ser usuário cadastrado (se descobrir uma forma, me avise!). 


G. M. Penello, 2019
gpenello@gmail.com