Passo a passo para que o programa seja inicializado automaticamente (dois jeitos):

Jeito 1)  - Criar um arquivo de atalho do RegistroDeUso.py
    	  - Associar o python.exe para abrir as extens�es .py
	    - Ex.: Execut�vel em "C:\Users\gpenello\Miniconda3\python.exe"
          - Copiar o atalho gerado anteriormente (ex. "RegistroDeUso.pyw - Shortcut") para a pasta de Startup
	  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

Jeito 2)  - Criar um arquivo RunRegistroDeUso.bat com o conte�do:

"C:\Users\gpenello\Miniconda3\python.exe" "D:\OneDrive - IF-UFRJ\UFRJ\Programas\Python\registro-de-uso-presenca-lab\Controle_UsoDeEquipamento\RegistroDeUso.py"
pause
          
          - Copiar o arquivo .bat gerado anteriormente para a pasta de Startup
	  - Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"



Para alterar a senha do administrador, rodar o arquivo "criptografarPassword.py".
Para minimizar a tela, use o nome 'admin' como usu�rio e a senha do administrador como password.

A �nica maneira de fechar o programa � usando o gerenciador de tarefas para fechar o terminal de python que est� rodando o programa. Se descobrir outra forma, me avise. :)
A ideia � realmente dificultar fechar o programa. S� � para fazer isso caso realmente desejado pelo usu�rio.


Ajeite as vari�veis "TelaCheia" e "equipamento" antes de rodar o programa. 
TelaCheia = True/False --> escolha um dos dois
equipamento = "Nome do equipamento desejado"

Com "TelaCheia = True", fica praticamente imposs�vel de fechar o programa sem ser usu�rio cadastrado (se descobrir uma forma, me avise!). 


G. M. Penello, 2019
gpenello@gmail.com