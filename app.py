from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DB_FILE = "C:/Users/Lenovo/OneDrive - EUC Nordvestsjælland/1. Mine ting/Programmering B/Python/Database_wepservere/artworks.db"

@app.route("/")
def forside():
    return render_template("forside.html", title="Hello")

@app.route("/login_profil")
def login_profil():
    return render_template("login_profil.html")

def hent_db_genes():
    if "db" not in g:
        g.db = sqlite3.connect("artworks.db")
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
         db.close()

@app.route("/søgeside", methods=["GET", "POST"])
def søgeside():
        if request.method == "POST":
            søgeord = request.form.get("søgeord", "")
            return søg_i_db(søgeord)
        return render_template("søgeside.html", titel="Velkommen", resultater=[])

#id, artist, painting, year, genre, image
def søg_i_db(søgeord):
    db = hent_db_genes() 
    cur = db.execute("SELECT painting, artist FROM artworks WHERE artist LIKE ? ", ('%' + søgeord + '%',))
    data = cur.fetchall()
    resultater = {"resultater": [dict(r) for r in data]}
    print(resultater)
    return render_template("søgeside.html", titel="Søgeresultater", resultater=resultater)

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/farvoritter")
def farvoritter():
    return render_template("farvoritter.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)