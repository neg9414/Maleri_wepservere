from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def forside():
    return render_template("forside.html", title="Hello")

@app.route("/login_profil")
def login_profil():
    return render_template("login_profil.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/docs")
def docs():
    return render_template("docs.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)