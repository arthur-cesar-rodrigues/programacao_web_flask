from flask import Flask, render_template, request, redirect
import mysql.connector #para importar o drive do mysql é preciso inserir essa linha (importar o mysql)

app = Flask(__name__)

@app.route("/tela_cadastro")
def cad_usuario():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")
    meucursor = db.cursor()
    query = "SELECT  nome, email, senha, codigo FROM Arthur_tbusuario"   #selecionando todos os dados que foram cadastrados
    meucursor.execute(query) #executando a linha do select
    resultado = meucursor.fetchall() #aqui pegamos to resultado da query e adicionamos no variavel resultado (pegamos todos os usuários cadastrados(fetchall) no banco atráves do resultado da query(select) e adicionamos na variavel resultado, e após isso no return do render template atribuimos na variavel users o valor do resultado)
    
    return render_template("cad_usuario.html", usuarios = resultado)

@app.route("/inserir_usuario", methods = ["POST"])
def insere_dados():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")
    #para conectar a variavel db com o banco de dados é preciso informar as informações necessarárias do login no servidor do banco; informar: o host (ip do servidor), user(usuario do servidor do banco), password(senha do servidor do banco), port(port/porta do servidor do banco), database(nome do banco do servidor)
    # query = "INSERT INTO arthur_usuario (nome, email, senha) VALUES ('" + nome + "','" + email + "')" essa é uma das formas de inserir os dados dentro do banco
    query = "INSERT INTO Arthur_tbusuario (nome, email, senha) VALUES (%s, %s, %s)" #essa é outra forma de inserir dados dentro do banco "%s", significa que os valor inseridos vai ser uma string
    valores = (nome, email, senha)

    meucursor = db.cursor() #cria um cursor para a conexão (db) com o banco de dados, é um obj da conexão com o banco, apartir dele podemos realizar ações no banco de dados
    meucursor.execute(query, valores)#.execute realiza a ação/func que vai ser usada dentro do banco de dados, o primeiro valor é o comando que vai ser executado dentro do banco e valores os valores que vai ser inseridos através do comando do banco
    db.commit()#.commit = abre uma transação com o banco (insert, delete,update), e essa transação commit salva as alterações no banco
    # a transação roollback = faz a transação mais nao grava no banco
    #   return render_template("cad_usuario.html") #inserimos esse return para que quando for ser enviado dados para o banco a pagina atualizar
    return redirect("/tela_cadastro")#na verdade ao invés de usarmos render_template(carrega apenas a página html- apenas o que está escrito no html) usamos o redirect (carrega a rota: as funções do rota + página html associada)

@app.route("/")
def telaLogin():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def fazerLogin():
    email = request.form["email"]
    senha = request.form["senha"]
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")
    meucursor = db.cursor()
    query = "select nome, email, senha from Arthur_tbusuario where email = '" + email + "'and senha = '" + senha + "'"
    # o comando acima verifica se o usuario e senha existem no banco
    meucursor.execute(query)
    print (meucursor.rowcount) #.rowcount = retorna quantas linhas foram retornadas no banco de dados (ou seja, se no banco rodar mais de uma linha, existe aquele nome/usuario com aquela senha no banco, é o que retorna no select)
    if meucursor.fetchall():#fetchall = retorna se foi retornado alguma linha la no banco(faz o mesmo do que o de cima)
        # return "Deu certo"
        return redirect("/tela_menu")
    else:
        return render_template("login.html", mensagem = "usuario ou senha inválida")
# para instalar o drive do mysql no ambiente virtual, é preciso ativar o ambiente virtual .\activate e inserir o seguinte o seguinte código no terminal "pip install mysql-connector-python" e espera instalar

@app.route("/tela_menu")
def menu():
    return render_template("menu.html")

@app.route("/excluir_usuario/<id>")#para passar um valor em uma rota é preciso depois da rota adicionar a rota "/<valor>", porém no caso vamos fazer uma rota de deletar a func precisa pegar esse valor dentro do paramemtro com esse mesmo nome no caso: func(valor):...
def excluir_usuario(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")
    meucursor = db.cursor()
    query = "DELETE FROM Arthur_tbusuario WHERE codigo = " + id #criando comando do banco para deletar uma linha (um usuario)
    meucursor.execute(query)#comando para fazer a exlusão
    db.commit() #comando para salvar no banco a exlusão feita
    return redirect("/tela_cadastro")

app.run()