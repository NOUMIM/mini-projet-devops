import os
import time
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///formations.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Formation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)


def attendre_base_de_donnees():
    for i in range(10):
        try:
            db.session.execute(text("SELECT 1"))
            print("Base de données connectée.")
            return
        except Exception:
            print(f"Tentative {i + 1}/10 : base de données indisponible...")
            time.sleep(2)
    print("Impossible de se connecter à la base de données.")


def initialiser_base():
    db.create_all()

    if Formation.query.count() == 0:
        formations_initiales = [
            Formation(
                titre="Introduction à DevOps",
                description="Découvrir les principes fondamentaux du DevOps et de l'automatisation."
            ),
            Formation(
                titre="Docker pour débutants",
                description="Apprendre à conteneuriser une application et à gérer les images Docker."
            ),
            Formation(
                titre="Git et GitHub",
                description="Maîtriser le versionnement du code et le travail collaboratif."
            ),
            Formation(
                titre="CI/CD avec GitHub Actions",
                description="Automatiser les tests, le build et le déploiement."
            ),
            Formation(
                titre="Administration Linux",
                description="Utiliser les commandes Linux utiles pour les projets DevOps."
            )
        ]

        db.session.add_all(formations_initiales)
        db.session.commit()
        print("Données initiales insérées avec succès.")


with app.app_context():
    attendre_base_de_donnees()
    initialiser_base()


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/formations")
def liste_formations():
    formations = Formation.query.all()
    return render_template("formations.html", formations=formations)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)