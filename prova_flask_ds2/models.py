from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

  
    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=False, default="padrao.png")

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"
