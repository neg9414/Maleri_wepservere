from flask import Flask, request, render_template, g, session, redirect, url_for
from datetime import date
import sqlite3, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "hemmelig_nøgle"
DB_FILE = "C:/Users/Lenovo/OneDrive - EUC Nordvestsjælland/1. Mine ting/Programmering B/Python/Database_wepservere/artworks.db"

# -------------------- DATABASE --------------------
def hent_db_genes():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# -------------------- FORSIDE --------------------
@app.route("/")
def forside():
    conn = sqlite3.connect("artworks.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM artworks")
    malerier = cur.fetchall()
    conn.close()

    today = date.today()
    random.seed(today.toordinal())

    dagens_maleri = random.choice(malerier)
    return render_template("forside.html", title="Kunstgalleri", dagens_maleri=dagens_maleri)

# -------------------- LOGIN / OPRET --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    db = hent_db_genes()

    if "username" in session:
        return render_template("login.html", already_logged_in=True, username=session["username"])

    fejl = None
    if request.method == "POST":
        form_type = request.form.get("form_type")
        username = request.form["username"].strip()
        password = request.form["password"]

        if form_type == "login":
            cur = db.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()
            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("forside"))
            else:
                fejl = "Forkert brugernavn eller kodeord."

        elif form_type == "signup":
            cur = db.execute("SELECT * FROM users WHERE username=?", (username,))
            if cur.fetchone():
                fejl = "Brugernavn findes allerede."
            else:
                hashed_pw = generate_password_hash(password)
                db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
                db.commit()
                cur = db.execute("SELECT * FROM users WHERE username=?", (username,))
                user = cur.fetchone()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("forside"))

    return render_template("login.html", fejl=fejl, title="Kunstgalleri")

# -------------------- LOGOUT --------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------- SØGNING --------------------
@app.route("/søgeside", methods=["GET", "POST"])
def søgeside():
    if request.method == "POST":
        søgeord = request.form.get("søgeord", "")
        return søg_i_db(søgeord)
    return render_template("søgeside.html", title="Kunstgalleri", resultater=None)

def søg_i_db(søgeord):
    db = hent_db_genes()
    cur = db.execute(""" SELECT id, painting, artist, year, genre, image, beskrivelse FROM artworks WHERE painting LIKE ? OR artist LIKE ? OR year LIKE ? OR genre LIKE ? OR beskrivelse LIKE ? """, tuple(['%' + søgeord + '%'] * 5))
    data = cur.fetchall()
    resultater = {"resultater": [dict(r) for r in data]}
    return render_template("søgeside.html", title="Kunstgalleri", resultater=resultater)


# -------------------- MALERI DETAILER --------------------
@app.route("/maleri/<int:artwork_id>")
def maleri_detail(artwork_id):
    db = hent_db_genes()
    cur = db.execute("SELECT * FROM artworks WHERE id=?", (artwork_id,))
    maleri = cur.fetchone()
    return render_template("maleri_detail.html", maleri=maleri)

# -------------------- DOCS --------------------
@app.route("/docs")
def docs():
    return render_template("docs.html", title="Kunstgalleri")

# -------------------- START APP --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
