from flask import Flask # importando no python, primeiro flask é um objeto dentro do Flask (classe)

app = Flask(__name__) #app é uma variavel 

@app.route('/') #é uma rota raiz, início do site (www.site"/") é o caminho da url, route (rota, caminho) = url, a rota "/" chama a função index, quando o usuário entra na "url" "ip"+"/", a função "index", quando voce cria uma rota, a função atrelada a ela precisa ficar na linha abaixo dela,
def index(): # def = function, para poder declarar uma função, function = def
    return "olá mundo"



@app.route('/rota2')
def NomeDaFuncao():
    return "outro texto"
# .\Scripts\python.exe .\main.py atalho para rodar o arquivo python, após isso entrar no link http abaixo no terminal

app.run() #esse comando é o que chama as funções (que faz as funções funcionarem), ele precisa ser o último comando do arquivo python para poder rodar todas as funções dentro do código python

# para poder executar um arquivo python é so clicar nos 3 pontos do lado de executar no vs code, executar e pronto, toda vez que fizer uma atualização no código, é preciso interromper a execução do arquivo com o atalho cntrl + c, fazer a mudança no código python, e apertar "cntrl + s" para salvar e fazer o processo de executar novamente 

# para navegar entre as "rotas", é so colocar a url + "/rota"