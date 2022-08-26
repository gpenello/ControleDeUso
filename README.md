## Copyright (c) 2020 Controle de Uso

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Controle de Uso de Equipamento
Utilize esse programa para criar um banco de dados contendo registro de usuários e um logbook do uso de equipamento.

## Configurações

Ao rodar o programa pela primeira vez, será realizado o cadastro do administrador do programa. No linux, o programa já acertará os arquivos para a inicialização automática. No Windows, a inicialização automática deve ser feita manualmente. Com checkbox TelaCheia selecionado, fica praticamente impossível de fechar o programa sem ser usuário cadastrado (se descobrir uma forma, me avise!). :) 

A ideia é realmente dificultar fechar o programa! 

Confira o arquivo Programa "Controle de Uso de Equipamento.pptx" para ver algumas informações adicionais contendo imagens das janelas do programa.

---

# (Windows) Versão do instalador

Baixe e rode o arquivo de instalação "RegistroDeUso_instalador.exe". O instalador irá facilitar o processo de inicialização automática do programa. Esta versão não conta com o botão de atualização pelo Git (o botão está desativado).


# (Windows) Versão rodando em python
## Passo a passo para que o programa seja inicializado automaticamente:

No Windows, a inicialização automática deve ser feita manualmente.
  - Rodar o programa a primeira vez e cadastrar o administrador.
  - Após criar a conta de administrador, copiar o arquivo "Run_RegistroDeUso.bat" gerado anteriormente para a pasta de Startup: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"
  - Instalar o programa AutoHotKey 

Importante para desabilitar os comandos alt+tab, windows+tab e CTRL+Esc dos teclados

 - https://www.autohotkey.com/

O programa tem que estar instalado em "C:\Program Files\AutoHotkey\AutoHotkey.exe"

##### (WINDOWS) A PRINCÍPIO NÃO PRECISA MAIS FAZER OS PASSOS ABAIXO. AGORA QUASE TUDO ESTÁ SENDO FEITO NA INICIALIZAÇÃO DO ADMINISTRADOR. (DEIXANDO AQUI APENAS PARA REFERÊNCIA)

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


---

---
### Linux

- Rodar a primeira vez como root e cadastrar o administrador.
```
sudo python3 RegistroDeUso.pyw
```
- Após criar a conta de administrador, o programa já alterou o sistema para a inicialização automática. Caso o programa não esteja inicializando automaticamente após o reboot, siga os passos abaixo.

##### (LINUX) A PRINCÍPIO NÃO PRECISA MAIS FAZER OS PASSOS ABAIXO. AGORA TUDO ESTÁ SENDO FEITO NA INICIALIZAÇÃO DO ADMINISTRADOR. (DEIXANDO AQUI APENAS PARA REFERÊNCIA OU ERROS)


Se o programa não iniciar automaticamente, o problema pode estar no arquivo /etc/sudoers. Verificar como o comando:
```  
sudo visudo
```  
ou 
```  
pkexec visudo
```  

Outra possibilidade é o programa estar instalado em um caminho que contenha espaço ou caracteres especiais. 

Outras tentativas:
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

---


G. M. Penello, 2019
gpenello@gmail.com
