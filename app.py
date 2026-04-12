from flask import Flask, render_template

app = Flask(__name__)

formations = [
    "Introduction à DevOps",
    "Docker pour débutants",
    "Git et GitHub",
    "CI/CD avec GitHub Actions",
    "Administration Linux"
]

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/formations")
def liste_formations():
    return render_template("formations.html", formations=formations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)