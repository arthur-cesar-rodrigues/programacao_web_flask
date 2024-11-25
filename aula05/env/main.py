from flask import Flask, render_template

app = Flask(__name__)
#o css não pode ficar dentro da pasta templates, o arquivo css precisa estar dentro de uma pasta dentro de env e fora de templates com o nome de "static" (e mover o arquivo css para esse pasta)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

app.run()