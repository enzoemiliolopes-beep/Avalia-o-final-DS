import math
import os
import uuid

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from werkzeug.utils import secure_filename

from models import db, Categoria, Produto

bp = Blueprint("main", __name__)

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}
IMAGEM_PADRAO = "padrao.png"


def extensao_valida(nome_arquivo):
    """True se o arquivo tem ponto e a extensão está na lista permitida."""
    return "." in nome_arquivo and \
        nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def converter_preco(texto):
    """Converte o texto do formulário em float. Retorna None se for inválido."""
    try:
        valor = float((texto or "").strip().replace(",", "."))
    except ValueError:
        return None
    if math.isnan(valor) or math.isinf(valor): 
        return None
    return valor


def validar_dados(nome, preco_texto, categoria_id):
    """Valida os campos de texto. Retorna (preco, lista_de_erros)."""
    erros = []

    if len(nome) < 3:
        erros.append("O nome deve ter pelo menos 3 caracteres.")

    preco = converter_preco(preco_texto)
    if preco is None:
        erros.append("Informe um preço válido (ex.: 19.90).")
    elif preco <= 0:
        erros.append("O preço deve ser maior que zero.")

    if not categoria_id or db.session.get(Categoria, categoria_id) is None:
        erros.append("Selecione uma categoria válida.")

    return preco, erros


def salvar_foto(arquivo):
    """Salva a foto em static/uploads com nome único e devolve o nome do arquivo."""
    nome_seguro = secure_filename(arquivo.filename)
    nome_final = f"{uuid.uuid4().hex}_{nome_seguro}"  
    arquivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nome_final))
    return nome_final


def apagar_foto(nome_arquivo):
    """Remove a foto do disco, preservando sempre a padrao.png."""
    if not nome_arquivo or nome_arquivo == IMAGEM_PADRAO:
        return
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
    if os.path.exists(caminho):
        os.remove(caminho)


@bp.route("/")
def index():
    busca = request.args.get("busca", "").strip()

    consulta = Produto.query
    if busca:
        consulta = consulta.filter(Produto.nome.ilike(f"%{busca}%"))
    produtos = consulta.order_by(Produto.nome).all()  # ordem alfabética

    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("index.html", produtos=produtos,
                           categorias=categorias, busca=busca)


@bp.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form.get("nome", "").strip()
    categoria_id = request.form.get("categoria_id", type=int)
    foto = request.files.get("foto")

    preco, erros = validar_dados(nome, request.form.get("preco"), categoria_id)

    tem_foto = foto is not None and foto.filename != ""
    if tem_foto and not extensao_valida(foto.filename):
        erros.append("Extensão de imagem não permitida. Use: png, jpg, jpeg ou gif.")

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return redirect(url_for("main.index"))

    imagem = salvar_foto(foto) if tem_foto else IMAGEM_PADRAO

    db.session.add(Produto(nome=nome, preco=preco, imagem=imagem,
                           categoria_id=categoria_id))
    db.session.commit()
    flash("Produto cadastrado com sucesso!", "sucesso")
    return redirect(url_for("main.index"))


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = db.get_or_404(Produto, id)

    if request.method == "GET":
        categorias = Categoria.query.order_by(Categoria.nome).all()
        return render_template("editar.html", produto=produto, categorias=categorias)

    nome = request.form.get("nome", "").strip()
    categoria_id = request.form.get("categoria_id", type=int)
    foto = request.files.get("foto")

    preco, erros = validar_dados(nome, request.form.get("preco"), categoria_id)

    tem_foto = foto is not None and foto.filename != ""
    if tem_foto and not extensao_valida(foto.filename):
        erros.append("Extensão de imagem não permitida. Use: png, jpg, jpeg ou gif.")

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return redirect(url_for("main.editar", id=id))

    foto_antiga = produto.imagem
    produto.nome = nome
    produto.preco = preco
    produto.categoria_id = categoria_id

    if tem_foto:
        produto.imagem = salvar_foto(foto)

    db.session.commit()

    if tem_foto:
        apagar_foto(foto_antiga)

    flash("Produto atualizado com sucesso!", "sucesso")
    return redirect(url_for("main.index"))


@bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    produto = db.get_or_404(Produto, id)
    foto = produto.imagem

    db.session.delete(produto)
    db.session.commit()
    apagar_foto(foto)  

    flash("Produto excluído.", "sucesso")
    return redirect(url_for("main.index"))
