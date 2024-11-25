from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("cliente.html")

@app.route("/cad_cliente", methods = ["POST"])
def cadastrarCliente():
    nome = request.form["nome"]
    cpf = request.form["cpf"] 
    rg = request.form["rg"]
    endereco = request.form["endereco"]
    bairro = request.form["bairro"]
    cidade = request.form["cidade"]
    cep = request.form["cep"]

    db = mysql.connector.connect(host = "201.23.3.86", user = "usr_aluno", password = "E$tud@_m@1$", port = 5000, database = "aula_fatec")

    query = "INSERT INTO Arthur_exercicio (nome, cpf, rg, endereco, bairro, cidade, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    valores = (nome, cpf, rg, endereco, bairro, cidade, cep)

    meucursor = db.cursor()

    meucursor.execute(query, valores)

    db.commit()

    return render_template("cliente.html")

app.run()