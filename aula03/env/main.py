from flask import Flask, render_template

app = Flask(__name__) #instanciando o flask dentro da variavel app

@app.route('/') #app.rout = criando uma rota na url do programa, só a barra é a rota raiz, home
def index(): #def criando uma função index, ":" = significa o fim da declaração da função
    return render_template("index.html", uma_variavel_no_html = "Arthur")#retornando uma página web dentro da rota #retorno da função
#em python não possui chave para inserir chaves para identar, porém precisa colocar um espaço no comando da função, aperta um tab e ja era; não precisa declarar a variavel, é so escrever a variavel e seu valor

@app.route("/pedro")
def pedro():
    return render_template("pedro.html", nome = "Pedro")

@app.route("/joel")
def joel():
    return render_template("joel.html", nome = "Joel")

@app.route("/jean")
def jean():
    return render_template("jean.html", nome = "Jean")


@app.route("/boasvindas")
def bemvindo():
    return render_template("pagina2.html", contador = 5)


#app.run(debug=true) = faz com que o site atualize sempre que voce atualiza o vs code, debuga sempre com uma atualização no vs

app.run()#.run é um método que faz rodar a função
#para executar é so ir nos 3 pontos -> executar -> iniciar a depuração ->arquivo python