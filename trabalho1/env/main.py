from flask import Flask, redirect, render_template, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"# Chave secreta necessária para usar flash messages

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

    msg = "Disciplina cadastrada com sucesso!"

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

    query_associacao_professor_disciplina = "SELECT * FROM Arthur_trabalho_professor_disciplina WHERE id_disciplina = %s"
    
    meucursor.execute(query_associacao_professor_disciplina, (id,))

    valida_professor_disciplina = meucursor.fetchone()

    if valida_professor_disciplina:
        flash("Não foi possível excluir a disciplina selecionada. Existe um ou mais professores que lecionam esta disciplina, é necessário deletar o professores primeiro antes da disciplina.")
        return redirect("/tela_exc_edit_disc")
    
    query_associacao_curso_disciplina = "SELECT * FROM Arthur_trabalho_curso_disciplina WHERE id_disciplina = %s"
    
    meucursor.execute(query_associacao_curso_disciplina, (id,))

    valida_curso_disciplina = meucursor.fetchone()

    if valida_curso_disciplina:
        flash("Não foi possível excluir a disciplina selecionada. Existe um ou mais cursos que possuem esta disciplina em sua grade, é necessário deletar os cursos primeiro antes da disciplina.")
        return redirect("/tela_exc_edit_disc")

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

    msg = "Dados da disciplina alterados com sucesso!"

    return render_template("tela_edit_disciplina.html", mensagem = msg, alterado = True)

@app.route("/tela_cad_curso")
def tela_cad_curso():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT * FROM Arthur_trabalho_disciplina"

    meucursor.execute(query)

    resultado = meucursor.fetchall()

    return render_template("tela_cad_curso.html", disciplinas = resultado)

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

    flash("Curso cadastrado com sucesso!")

    return redirect("/tela_cad_curso")

@app.route("/tela_exc_edit_curso")
def tela_exc_edit_curso():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = """
        SELECT c.id, c.nome, SUM(d.carga_horaria) AS carga_total
        FROM Arthur_trabalho_curso AS c
        JOIN Arthur_trabalho_curso_disciplina AS cd ON c.id = cd.id_curso
        JOIN Arthur_trabalho_disciplina AS d ON cd.id_disciplina = d.id
        GROUP BY c.id
    """

    meucursor.execute(query)

    resultado = meucursor.fetchall()

    return render_template("tela_exc_edit_curso.html", cursos = resultado, pesquisa = False)

@app.route("/procura_curso", methods = ["POST"])
def procura_curso():
    curso_pesquisado = request.form["pesquisa_curso"]

    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = """
        SELECT c.id, c.nome, SUM(d.carga_horaria) AS carga_total
        FROM Arthur_trabalho_curso AS c
        JOIN Arthur_trabalho_curso_disciplina AS cd ON c.id = cd.id_curso
        JOIN Arthur_trabalho_disciplina AS d ON cd.id_disciplina = d.id
        WHERE c.nome = %s
        GROUP BY c.id
    """

    meucursor.execute(query, (curso_pesquisado,))

    resultado = meucursor.fetchall()

    if resultado:
        return render_template("tela_exc_edit_curso.html", cursos = resultado, pesquisa = True)
    else:
        msg = "Curso não encontrado."
        return render_template("tela_exc_edit_curso.html", mensagem = msg, pesquisa = True)
    
@app.route("/exclui_curso/<id>")
def exclui_curso(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_associacao_curso_aluno = "SELECT * FROM Arthur_trabalho_aluno_curso WHERE id_curso = %s"
    
    meucursor.execute(query_associacao_curso_aluno, (id,))

    valida_curso_aluno = meucursor.fetchone()

    if valida_curso_aluno:
        flash("Não foi possível excluir o curso selecionado. Existem um ou mais alunos matriculados neste curso, é necessário remover os alunos primeiro antes do curso.")
        return redirect("/tela_exc_edit_curso")
    
    query_curso_disciplina = "DELETE FROM Arthur_trabalho_curso_disciplina WHERE id_curso = %s"

    meucursor.execute(query_curso_disciplina, (id,))

    db.commit() 

    query_curso = "DELETE FROM Arthur_trabalho_curso WHERE id = %s"

    meucursor.execute(query_curso, (id,))

    db.commit() 

    return redirect("/tela_exc_edit_curso")

@app.route("/tela_edit_curso/<id>")
def tela_edit_curso(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_curso = "SELECT nome FROM Arthur_trabalho_curso WHERE id = %s" 

    # Buscar o nome do curso
    meucursor.execute(query_curso, (id,))

    curso = meucursor.fetchone()

    # Buscar todas as disciplinas cadastradas/associadas no curso 
    query_disciplinas_curso = """
        SELECT d.id, d.nome, d.carga_horaria
        FROM Arthur_trabalho_disciplina AS d
        LEFT JOIN Arthur_trabalho_curso_disciplina AS cd ON d.id = cd.id_disciplina
        WHERE cd.id_curso = %s
    """
    meucursor.execute(query_disciplinas_curso, (id,))
    disciplinas_associadas = meucursor.fetchall()

    # Buscando todas as disciplinas disponíveis (para preencher o checkbox)
    query_disciplinas_todas = "SELECT * FROM Arthur_trabalho_disciplina"
    meucursor.execute(query_disciplinas_todas)
    todas_disciplinas = meucursor.fetchall()

    return render_template(
        "tela_edit_curso.html",
        curso={"id": id, "nome": curso[0]},
        disciplinas_associadas=[d[0] for d in disciplinas_associadas],  # IDs das disciplinas associadas
        todas_disciplinas = todas_disciplinas, alterado = False
    )

@app.route("/salva_curso/<id>", methods = ["POST"])
def salva_curso(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    nome = request.form["nome_curso"]

    query_nome_curso = "UPDATE Arthur_trabalho_curso SET nome = %s WHERE id = %s"

    meucursor.execute(query_nome_curso, (nome, id))#alterando  o nome do curso

    #apagando as disciplinas associadas ao curso
    query_deleta_disciplinas = "DELETE FROM Arthur_trabalho_curso_disciplina WHERE id_curso = %s"

    meucursor.execute(query_deleta_disciplinas, (id,))

    #inserindo as disciplinas atualizadas ao curso
    query_atualiza_disciplinas = "INSERT INTO Arthur_trabalho_curso_disciplina (id_curso, id_disciplina) VALUES (%s, %s)"

    disciplinas_selecionadas = request.form.getlist("disciplinas")#lista de ids das disciplinas selecionadas

    for id_disciplina in disciplinas_selecionadas:
        meucursor.execute(query_atualiza_disciplinas, (id, id_disciplina))

    db.commit()#salvando alterações

    msg = "Dados do curso alterados com sucesso!"

    return render_template("tela_edit_curso.html", alterado = True, mensagem = msg)


@app.route("/tela_cad_professor")
def tela_cad_professor():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query = "SELECT * FROM Arthur_trabalho_disciplina"

    meucursor.execute(query)

    resultado = meucursor.fetchall()

    return render_template("tela_cad_professor.html", disciplinas = resultado)

@app.route("/cadastra_professor", methods = ["POST"])
def cadastra_professor():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    nome_professor = request.form["nome_professor"]
    telefone = request.form["telefone"]
    usuario_professor = request.form["usuario_professor"]
    senha_professor = request.form["senha_professor"]

    #criando e salvando o nome, telefone, usuario e senha do professor na tabela professor do banco de dados
    query_cria_dados_professor = "INSERT INTO Arthur_trabalho_professor (nome, telefone, usuario, senha) VALUES (%s, %s, %s, %s)"

    meucursor.execute(query_cria_dados_professor, (nome_professor, telefone, usuario_professor, senha_professor))

    db.commit()

    #pegando o id do professor criado
    id_professor = meucursor.lastrowid 

    #pegando os valores(no caso o id, o que foi passado como parâmetro no campo value no input) das disciplinas selecionadas no formulário (getlist)
    disciplinas = request.form.getlist("disciplinas") #no caso vai ser a lista dos ids das respectivas disciplinas

    #salvando as associações na tabela Arthur_trabalho_professor_disciplina do banco de dados
    query_associacao_professor_disciplina = "INSERT INTO Arthur_trabalho_professor_disciplina (id_professor, id_disciplina) VALUES (%s, %s)"
    
    for id_disciplina in disciplinas:
        meucursor.execute(query_associacao_professor_disciplina, (id_professor, id_disciplina))#iterando sobre as disciplinas selecionadas e salvando o valor do id do professor (que vai ser fixo, um por vez, "um curso possui varias disciplinas") e a lista/array de ids das disciplinas selecionadas no form na tabela professor_disciplina
    
    db.commit()#salvando no banco

    flash("Professor(a) cadastrado com sucesso!")

    return redirect("/tela_cad_professor")
 
@app.route("/tela_exc_edit_professor")
def tela_edit_exc_professor():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    # Consulta SQL para obter o ID, nome do professor e suas disciplinas
    query = """
        SELECT 
            p.id AS professor_id, 
            p.nome AS professor_nome, 
            d.nome AS disciplina_nome
        FROM 
            Arthur_trabalho_professor AS p
        LEFT JOIN 
            Arthur_trabalho_professor_disciplina AS pd ON p.id = pd.id_professor
        LEFT JOIN 
            Arthur_trabalho_disciplina AS d ON pd.id_disciplina = d.id
        ORDER BY 
            p.id, d.nome;
    """

    meucursor.execute(query)
    resultados = meucursor.fetchall()

    # Organizando os dados em um dicionário: {professor_id: {"nome": nome, "disciplinas": [disciplinas]}}
    professores = {}

    for professor_id, professor_nome, disciplina_nome in resultados:
        if professor_id not in professores:
            professores[professor_id] = {"nome": professor_nome, "disciplinas": []}
        if disciplina_nome:
            professores[professor_id]["disciplinas"].append(disciplina_nome)
    
    return render_template("tela_exc_edit_professor.html", professores = professores, pesquisa = False)

@app.route("/procura_professor", methods = ["POST"])
def procura_professor():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    # Consulta SQL para obter o ID, nome do professor e suas disciplinas
    query = """
        SELECT 
            p.id AS professor_id, 
            p.nome AS professor_nome, 
            d.nome AS disciplina_nome
        FROM 
            Arthur_trabalho_professor AS p
        LEFT JOIN 
            Arthur_trabalho_professor_disciplina AS pd ON p.id = pd.id_professor
        LEFT JOIN 
            Arthur_trabalho_disciplina AS d ON pd.id_disciplina = d.id
        WHERE p.nome = %s
        ORDER BY 
            p.id, d.nome;
    """

    professor_pesquisado = request.form["pesquisa_professor"]

    meucursor.execute(query, (professor_pesquisado,))

    resultado = meucursor.fetchall()

    # Organizando os dados em um dicionário: {professor_id: {"nome": nome, "disciplinas": [disciplinas]}}
    professores = {}

    for professor_id, professor_nome, disciplina_nome in resultado:
        if professor_id not in professores:
            professores[professor_id] = {"nome": professor_nome, "disciplinas": []}
        if disciplina_nome:
            professores[professor_id]["disciplinas"].append(disciplina_nome)

    if professores:
        return render_template("tela_exc_edit_professor.html", professores = professores, pesquisa = True)
    else:
        msg = "Professor não encontrado."
        return render_template("tela_exc_edit_professor.html", mensagem = msg, pesquisa = True)
    
@app.route("/exclui_professor/<id>")
def exclui_professor(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_ids_disciplina = "SELECT id_disciplina FROM Arthur_trabalho_professor_disciplina WHERE id_professor = %s"
    
    meucursor.execute(query_ids_disciplina, (id,))

    ids_disciplinas_associadas = meucursor.fetchall()

    query_ids_curso = "SELECT id_curso FROM Arthur_trabalho_curso_disciplina WHERE id_disciplina = %s"

    for id_disciplina in ids_disciplinas_associadas:
        meucursor.execute(query_ids_curso, (id_disciplina))

    ids_cursos_associados = meucursor.fetchall()

    query_id_aluno = "SELECT id_aluno FROM Arthur_trabalho_aluno_curso WHERE id_curso = %s"

    for id_curso in ids_cursos_associados:
        meucursor.execute(query_id_aluno, (id_curso))

    id_aluno = meucursor.fetchone()

    if id_aluno:
        flash("Não foi possível deletar o professor selecionado. O professor já se encontra cadastrado em um ou mais cursos que possuem alunos matriculados, para remover o professor é necessário remover os alunos matriculados no curso que possui a matéria lecionada pelo professor primeiro.")
        return redirect("/tela_exc_edit_professor")

    #deletando associações entre professor e disciplina (de acordo com o id do professor)
    query_deleta_professor_disciplina = "DELETE FROM Arthur_trabalho_professor_disciplina WHERE id_professor = %s"
    meucursor.execute(query_deleta_professor_disciplina, (id,))

    #deletando o professor da tabela professor (de acordo com id do professor)
    query_deleta_professor = "DELETE FROM Arthur_trabalho_professor WHERE id = %s"  
    meucursor.execute(query_deleta_professor, (id,))

    db.commit()#salvando alterações

    return redirect("/tela_exc_edit_professor")

@app.route("/tela_edit_professor/<id>")
def tela_edit_professor(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_dados_professor = "SELECT nome, telefone, usuario, senha FROM Arthur_trabalho_professor WHERE id = %s" 

    # Buscando o nome do professor
    meucursor.execute(query_dados_professor, (id,))

    dados_professor = meucursor.fetchone()

    # Buscar todas as disciplinas cadastradas/associadas ao professor 
    query_disciplinas_professor = """
        SELECT d.id, d.nome, d.carga_horaria
        FROM Arthur_trabalho_disciplina AS d
        LEFT JOIN Arthur_trabalho_professor_disciplina AS cd ON d.id = cd.id_disciplina
        WHERE cd.id_professor = %s
    """
    meucursor.execute(query_disciplinas_professor, (id,))
    disciplinas_associadas = meucursor.fetchall()

    # Buscando todas as disciplinas disponíveis (para preencher o checkbox)
    query_disciplinas_todas = "SELECT * FROM Arthur_trabalho_disciplina"
    meucursor.execute(query_disciplinas_todas)
    todas_disciplinas = meucursor.fetchall()

    return render_template(
        "tela_edit_professor.html",
        id = id, professor = dados_professor,
        disciplinas_associadas=[d[0] for d in disciplinas_associadas],  # IDs das disciplinas associadas
        todas_disciplinas = todas_disciplinas, alterado = False
    )

@app.route("/salva_professor/<id>", methods=["POST"])
def salva_professor(id):
    db = mysql.connector.connect(
        host="201.23.3.86", 
        user="usr_aluno", 
        password="E$tud@_m@1$", 
        port=5000, 
        database="aula_fatec"
    )

    meucursor = db.cursor()

    nome_professor = request.form["nome_professor"]
    telefone = request.form["telefone"]
    usuario_professor = request.form["usuario_professor"]
    senha_professor = request.form["senha_professor"]

    # Atualizando os dados do professor
    query_atualiza_dados_professor = """
        UPDATE Arthur_trabalho_professor 
        SET nome = %s, telefone = %s, usuario = %s, senha = %s 
        WHERE id = %s
    """
    meucursor.execute(query_atualiza_dados_professor, (nome_professor, telefone, usuario_professor, senha_professor, id))

    # Apagando as disciplinas associadas ao professor
    query_deleta_disciplinas = "DELETE FROM Arthur_trabalho_professor_disciplina WHERE id_professor = %s"
    meucursor.execute(query_deleta_disciplinas, (id,))

    # Inserindo as disciplinas atualizadas
    query_atualiza_disciplinas = "INSERT INTO Arthur_trabalho_professor_disciplina (id_professor, id_disciplina) VALUES (%s, %s)"
    disciplinas_selecionadas = request.form.getlist("disciplinas")  # Lista de IDs das disciplinas

    for id_disciplina in disciplinas_selecionadas:
        meucursor.execute(query_atualiza_disciplinas, (id, id_disciplina))

    db.commit()#salvando alterações

    msg = "Dados do professor(a) alterados com sucesso!"

    return render_template("tela_edit_professor.html", alterado=True, mensagem=msg)

@app.route("/tela_cad_aluno")
def tela_cad_aluno():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_todos_cursos = "SELECT * FROM Arthur_trabalho_curso"

    meucursor.execute(query_todos_cursos)

    resultado = meucursor.fetchall()

    return render_template("tela_cad_aluno.html", cursos = resultado)


@app.route("/cadastra_aluno", methods = ["POST"])
def cadastra_aluno():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    nome_aluno = request.form["nome_aluno"]
    cpf = request.form["cpf"]
    endereco = request.form["endereco"]
    senha_aluno = request.form["senha_aluno"]

    #criando e salvando o nome, cpf, endereco e senha do aluno na tabela aluno do banco de dados
    query_cria_dados_professor = "INSERT INTO Arthur_trabalho_aluno (nome, cpf, endereco, senha) VALUES (%s, %s, %s, %s)"

    meucursor.execute(query_cria_dados_professor, (nome_aluno, cpf, endereco, senha_aluno))

    db.commit()

    #pegando o id do aluno criado
    id_aluno = meucursor.lastrowid 

    #pegando os valores(no caso o id, o que foi passado como parâmetro no campo value no input) do curso selecionado no formulário (getlist)
    cursos = request.form.getlist("cursos") #no caso vai ser um item  da lista dos ids dos cursos

    #salvando as associações na tabela Arthur_trabalho_aluno_curso do banco de dados
    query_associacao_aluno_curso = "INSERT INTO Arthur_trabalho_aluno_curso (id_aluno, id_curso) VALUES (%s, %s)"
    
    for id_curso in cursos:
        meucursor.execute(query_associacao_aluno_curso, (id_aluno, id_curso))#iterando e pegando o curso selecionado dentre a lista de cursos e salvando o valor do id do curso
    
    db.commit()#salvando no banco

    flash("Aluno(a) cadastrado com sucesso!")

    return redirect("/tela_cad_aluno")

@app.route("/tela_exc_edit_aluno")
def tela_exc_edit_aluno():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    # Consulta SQL para obter o ID, nome do aluno e seus cursos
    query = """
        SELECT 
            aluno.id AS id_aluno,
            aluno.nome AS nome_aluno,
            aluno.cpf AS cpf_aluno,
            curso.nome AS nome_curso
        FROM 
            Arthur_trabalho_aluno AS aluno
        JOIN 
            Arthur_trabalho_aluno_curso AS aluno_curso
            ON aluno.id = aluno_curso.id_aluno
        JOIN 
            Arthur_trabalho_curso AS curso
            ON aluno_curso.id_curso = curso.id
        ORDER BY 
            aluno.nome, curso.nome;
    """

    meucursor.execute(query)
    resultado = meucursor.fetchall()

    return render_template("tela_exc_edit_aluno.html", alunos = resultado, pesquisa = False)

@app.route("/procura_aluno", methods = ["POST"])
def procura_aluno():
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    #pegando o nome do aluno digitado pelo usuário no campo de pesquisa
    nome_pesquisado = request.form["pesquisa_aluno"]

    # Consulta SQL para obter o ID, nome do aluno e seus cursos, de acordo com o nome pesquisado
    query = """
        SELECT 
            aluno.id AS id_aluno,
            aluno.nome AS nome_aluno,
            aluno.cpf AS cpf_aluno,
            curso.nome AS nome_curso
        FROM 
            Arthur_trabalho_aluno AS aluno
        JOIN 
            Arthur_trabalho_aluno_curso AS aluno_curso
            ON aluno.id = aluno_curso.id_aluno
        JOIN 
            Arthur_trabalho_curso AS curso
            ON aluno_curso.id_curso = curso.id
        WHERE
            aluno.nome = %s
        ORDER BY 
            aluno.nome, curso.nome;
    """

    meucursor.execute(query, (nome_pesquisado,))
    resultado = meucursor.fetchall()

    if resultado:
        return render_template("tela_exc_edit_aluno.html", alunos = resultado, pesquisa = True)
    else:
        msg = "Aluno não encontrado."
        return render_template("tela_exc_edit_aluno.html", mensagem = msg, pesquisa = True)

@app.route("/exclui_aluno/<id>")
def exclui_aluno(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    #query que deleta as associações entre alunos e cursos (tabela Arthur_trabalho_aluno_curso)

    query_associacao_aluno_curso = "DELETE FROM Arthur_trabalho_aluno_curso WHERE id_aluno = %s"

    meucursor.execute(query_associacao_aluno_curso, (id,))

    #query que deleta o aluno na tabela aluno
    query_deleta_aluno = "DELETE FROM Arthur_trabalho_aluno WHERE id = %s"

    meucursor.execute(query_deleta_aluno, (id,))

    db.commit() #salvando as alterações (no caso a exclusão de um aluno e suas associações entre cursos) no banco de dados

    return redirect("/tela_exc_edit_aluno")

@app.route("/tela_edit_aluno/<id>")
def tela_edit_aluno(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    query_dados_aluno = "SELECT * FROM Arthur_trabalho_aluno WHERE id = %s" 

    # pegando os dados do aluno conforme seu id
    meucursor.execute(query_dados_aluno, (id,))

    dados_aluno = meucursor.fetchone()

    # pegando o curso em que o aluno está matriculado
    query_curso_aluno = """
        SELECT d.id
        FROM Arthur_trabalho_curso AS d
        LEFT JOIN Arthur_trabalho_aluno_curso AS cd ON d.id = cd.id_curso
        WHERE cd.id_aluno = %s
    """
    meucursor.execute(query_curso_aluno, (id,))
    id_curso_associado = meucursor.fetchone()

    # Buscando todas os cursos disponíveis (para preencher o checkbox)
    query_cursos_todos = "SELECT id, nome FROM Arthur_trabalho_curso"
    meucursor.execute(query_cursos_todos)
    todos_cursos = meucursor.fetchall()

    return render_template(
        "tela_edit_aluno.html", aluno = dados_aluno,
        id_curso_associado = id_curso_associado,
        todos_cursos = todos_cursos, alterado = False
    )

@app.route("/salva_aluno/<id>", methods = ["POST"])
def salva_aluno(id):
    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    meucursor = db.cursor()

    nome_aluno = request.form["nome_aluno"]
    cpf = request.form["cpf"]
    endereco = request.form["endereco"]
    senha_aluno = request.form["senha_aluno"]

    # Atualizando os dados do aluno
    query_atualiza_dados_aluno = """
        UPDATE Arthur_trabalho_aluno 
        SET nome = %s, cpf = %s, endereco = %s, senha = %s 
        WHERE id = %s
    """

    meucursor.execute(query_atualiza_dados_aluno,(nome_aluno, cpf, endereco, senha_aluno, id))

    #removendo associações antigas entre aluno e curso
    query_associacao_antiga = "DELETE FROM Arthur_trabalho_aluno_curso WHERE id_aluno = %s"

    meucursor.execute(query_associacao_antiga, (id,))

    #pegar o curso selecionado no formulário
    curso_atualizado = request.form.getlist("cursos")

    #query que vai atualizar o curso do aluno
    query_nova_associacao = "INSERT INTO Arthur_trabalho_aluno_curso (id_aluno, id_curso) VALUES (%s, %s)"

    for id_curso in curso_atualizado:
        meucursor.execute(query_nova_associacao, (id, id_curso))

    db.commit()#salvando alterações dos dados do aluno

    msg = "Dados do aluno(a) alterados com sucesso."

    return render_template("tela_edit_aluno.html", mensagem = msg, alterado = True)

app.run(debug=True)