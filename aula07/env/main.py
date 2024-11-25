from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('imc.html')

@app.route("/calcular_imc_post", methods=["POST"])#convertendo a rota para post
def calcular():
    altura = float(request.form['txt_altura'])
   # print(altura)
    #para pegar o valor do dado do formulário é necessário importar e usar o request + .daonde vem o dado(no caso de um formulário, "form") e dentro dos parenteses coloca o name do input do valor
    #e o float para converter o valor de string para float
    peso = float(request.form['txt_peso'])
    imc = peso / (altura * altura)
    return render_template("imc.html", result_imc = f'{imc:2f}')#retornando o valor do imc dentro da página html imc, e atribuindo o valor de imc dentro da variavel result_imc dentro de imc.html

#pegando dados de uma página html (igual no caso acima, pegando de um formulário) através do método get
@app.route("/calcular_imc_get")
def calcular_imc_get():
    args = request.args #preceisa criar essa variavel "args" (pode se qualquer nome) para pode captar os dados de uma página/formulário pelo método get (no método get, os dados digitados pelo usuário aparece na url do navegador e os dados ficam salvos no navegador(para dados que podem ser vistos), no post não aparece nada na url e não fica salvo- o post é definido para senhas e dados que não pode ser expostos)
    altura = float(args.get("txt_altura"))
    peso = float(args.get("txt_peso"))
    imc = peso / (altura * altura)

    if (imc < 18):
        resultado = "Magrelo"
        imagem = "./static/thin_person.webp"
    
    if (imc >= 18 and imc < 26):
        resultado = "Normal"
        imagem = "./static/normal_person.png"

    if (imc >= 26):
        resultado = "Obeso"
        imagem = "./static/fat_person.webp"

    

    # f'{valor:.2f'} = arredondando um valor float, para 2 casas depois da virgula
    return render_template("imc.html", result_imc = f'{imc:.2f}', result = resultado, Imagem = imagem)

app.run()