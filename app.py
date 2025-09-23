from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DB_FILE = "./db/genes.db"

def hent_db_genes():
    if "db" not in g:
        g.db = sqlite3.connect("genes.sql")
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route("/")
def forside():
    return render_template("forside.html", title="Hello")

@app.route("/login_profil")
def login_profil():
    return render_template("login_profil.html")

@app.route("/søgeside", methods=["GET", "POST"])
def søgeside():
        if request.method == "POST":
            søgeord = request.form.get("søgeord", "")
            return søg_i_db(søgeord)
        return render_template("søgeside.html", titel="Velkommen", resultater=[])

def søg_i_db(søgeord):
    db = hent_db_genes() 
    cur = db.execute("""SELECT id, gene_name, gene_family, description FROM genes WHERE gene_name LIKE ? OR description LIKE ?""", ('%' + søgeord + '%'))
    data = cur.fetchall()
    resultater = {"resultater": [dict(u) for u in data]}
    return render_template("sødeside.html", titel="Søgeresultater", resultater=resultater)

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/farvoritter")
def farvoritter():
    return render_template("farvoritter.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)