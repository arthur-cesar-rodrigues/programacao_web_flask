from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def matematica():    
    return render_template("matematica.html")

@app.route("/fahrenheit")
def fahrenheit():
    
    return render_template("fahrenheit.html")

@app.route("/calc_fahrenheit")
def calFahrenheit():
    args = request.args

    celsius = float(args.get("celsius"))

    fahrenheit = (celsius * 1.8) + 32

    return render_template("fahrenheit.html", text = "A conversão de celsius para fahrenheit é", result_fahreheit = fahrenheit)
    

@app.route("/calculo2grau")
def calculo2grau():
    return render_template("calculo2grau.html")


app.run()