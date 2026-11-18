import os

from flask import Flask

from models import db, Categoria
from routes import bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///produtos.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  

db.init_app(app)
app.register_blueprint(bp)

CATEGORIAS_INICIAIS = ["Eletrônicos", "Alimentos", "Roupas", "Livros"]

with app.app_context():
    db.create_all()

    if Categoria.query.count() == 0:
        for nome in CATEGORIAS_INICIAIS:
            db.session.add(Categoria(nome=nome))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
