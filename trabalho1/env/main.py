from flask import Flask, redirect, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/tela_cad_disciplina")
def tela_cad_disciplina():
    return render_template("tela_cad_disciplina.html")

@app.route("/cadastra_disciplina", methods = ["POST"])
def cadastra_displina():
    nome_disciplina = request.form["nome_disciplina"]
    carga_horaria = request.form["carga_horaria"]

    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    query = "INSERT INTO Arthur_trabalho_disciplina (nome, carga_horaria) VALUES (%s, %s)"

    valores = (nome_disciplina, carga_horaria)

    meucursor = db.cursor()

    meucursor.execute(query, valores)

    db.commit()

    msg = "Disciplina cadastrada com sucesso!!!"

    return render_template("tela_cad_disciplina.html", mensagem = msg)

@app.route("/tela_exc_edit_disc")
def tela_exc_edit_disc():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT * FROM Arthur_trabalho_disciplina"

    meucursor.execute(query)

    resultado = meucursor.fetchall()

    return render_template("tela_exc_edit_disc.html", disciplinas = resultado, pesquisa = False)

@app.route("/procura_disciplina", methods = ["POST"])
def procura_disciplina():
    disciplina_pesquisada = request.form["pesquisa_disciplina"]

    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT * FROM Arthur_trabalho_disciplina WHERE nome = %s"

    meucursor.execute(query, (disciplina_pesquisada,))

    resultado = meucursor.fetchall()

    if resultado:
        return render_template("tela_exc_edit_disc.html", disciplinas = resultado, pesquisa = True)
    else:
        msg = "Disciplina não encontrada."
        return render_template("tela_exc_edit_disc.html", mensagem = msg, pesquisa = True)

@app.route("/exclui_disciplina/<id>")
def exclui_disciplina(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "DELETE FROM Arthur_trabalho_disciplina WHERE id = " + id 

    meucursor.execute(query)

    db.commit() 

    return redirect("/tela_exc_edit_disc")

@app.route("/tela_edit_disciplina/<id>")
def tela_edit_disciplina(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT nome, carga_horaria FROM Arthur_trabalho_disciplina WHERE id = %s " 

    meucursor.execute(query, (id,))

    resultado = meucursor.fetchone()#retorna a primeira linha que saiu como resultado do banco de dados

    nome, carga_horaria = resultado#pegando os valores que foram retornados da tabela e atribuindo as variaveis( na ordem, porque o primeiro valor retornado é o nome e o segundo é a carga_hoararia)

    return render_template("tela_edit_disciplina.html", id = id, nome = nome, carga_horaria = carga_horaria, alterado = False)

@app.route("/salva_disciplina/<id>", methods = ["POST"])
def salva_disciplina(id):
    nome_disciplina = request.form["nome_disciplina"]
    carga_horaria = request.form["carga_horaria"]

    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    query = "UPDATE Arthur_trabalho_disciplina SET nome = %s, carga_horaria = %s WHERE id = %s"#comando sql para atualizar os dados conforme o id

    valores = (nome_disciplina, carga_horaria, id)

    meucursor = db.cursor()

    meucursor.execute(query, valores)

    db.commit()#salvando as alterações no banco

    msg = "Disciplina alterada com sucesso!!!"

    return render_template("tela_edit_disciplina.html", mensagem = msg, alterado = True)

@app.route("/tela_cad_curso")
def tela_cad_curso():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT * FROM Arthur_trabalho_disciplina"

    meucursor.execute(query)

    resultado = meucursor.fetchall()

    msg = "Não existe disciplinas cadastradas. Cadastre disciplinas antes de cadastrar um curso."

    return render_template("tela_cad_curso.html", disciplinas = resultado, mensagem = msg)

@app.route("/cadastra_curso", methods = ["POST"])
def cadastra_curso():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    nome_curso = request.form["nome_curso"]

    #salvando o nome do curso na tabela curso do banco de dados
    query_salva_nome_curso = "INSERT INTO Arthur_trabalho_curso (nome) VALUES (%s)"
    meucursor.execute(query_salva_nome_curso, (nome_curso,))
    db.commit()

    #pegando o id do curso criado
    id_curso = meucursor.lastrowid 

    #pegando os valores(no caso o id, o que foi passado como parâmetro no campo value no input) das disciplinas selecionadas no formulário (getlist)
    disciplinas = request.form.getlist("disciplinas") #no caso vai ser a lista dos ids das respectivas disciplinas

    #salvando as associações na tabela curso_disciplina do banco de dados
    query_associacao_curso_disciplina = "INSERT INTO Arthur_trabalho_curso_disciplina (id_curso, id_disciplina) VALUES (%s, %s)"
    
    for id_disciplina in disciplinas:
        meucursor.execute(query_associacao_curso_disciplina, (id_curso, id_disciplina))#iterando sobre as disciplinas selecionadas e salvando o valor do id do curso (que vai ser fixo, um por vez, "um curso possui varias disciplinas") e a lista/array de ids das disciplinas selecionadas no form na tabela curso_disciplina
    
    db.commit()#salvando no banco
    
    return redirect("/tela_cad_curso")

app.run()