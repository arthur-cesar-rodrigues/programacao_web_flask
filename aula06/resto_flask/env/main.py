from flask import Flask, render_template

app = Flask(__name__)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/reservartion")
def reservation():
    return render_template("reservation.html")
 

@app.route("/special_dishes")
def sprecial_Dishes():
    return render_template("special-dishes.html")
# será que precisa criar renomear o arquivo special-dishes.html para special_dishes.html (por conta do problema do flask com os traços) ?

@app.route("/team")
def team():
    return render_template("team.html")

app.run()


