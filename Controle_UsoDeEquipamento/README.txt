Passo a passo para que o programa seja inicializado automaticamente:

    Criar um arquivo de atalho do RegistroDeUso.pyw

    Associar o pythonw.exe para abrir as extensões .pyw
	- Ex.: Executável em "C:\Users\gpenello\Miniconda3\pythonw.exe"

    Copiar o atalho gerado anteriormente (ex. "RegistroDeUso.pyw - Shortcut") para a pasta de Startup
	- Pasta geral do Windows: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"


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