# Cadastro de Produtos

Avaliação Final – DS1 (Etec de Itaquera / Centro Paula Souza).

# 1. Descrição do sistema e tecnologias

Sistema web para cadastrar, listar, buscar, editar e excluir produtos, cada um
ligado a uma categoria (relação 1:N: uma categoria tem vários produtos). Os dados
ficam salvos em um banco de dados e **não se perdem** ao reiniciar o servidor.

Funcionalidades:
- Cadastro de produto com nome, preço, categoria e foto (opcional; sem foto usa `padrao.png`).
- Validações: nome com no mínimo 3 caracteres, preço maior que zero (e válido), extensão de imagem permitida (png, jpg, jpeg, gif).
- Busca por nome, sempre em ordem alfabética.
- Edição de produto (a foto antiga é apagada do disco ao ser trocada).
- Exclusão de produto (a foto também é apagada do disco, preservando a `padrao.png`).

Tecnologias: Python 3, Flask, Flask-SQLAlchemy (ORM), SQLite, Jinja2, HTML e CSS.

Estrutura de pastas:

```
prova_flask_ds1/
├── app.py            # cria o app, configura o banco e cadastra as categorias iniciais
├── models.py         # tabelas Categoria e Produto
├── routes.py         # rotas (listar, salvar, editar, excluir)
├── requirements.txt
├── .gitignore
├── README.md
├── templates/        # base.html, index.html, editar.html
└── static/
    ├── css/style.css
    └── uploads/padrao.png
```

# 2. Como rodar o projeto localmente

```bash
git clone <URL_DO_REPOSITORIO>
cd prova_flask_ds1

python -m venv venv
venv\Scripts\activate     


python app.py
```

Abra no navegador: http://127.0.0.1:5000

O banco (`instance/produtos.db`) e as categorias iniciais são criados automaticamente
na primeira execução.

# 3. Comandos Git utilizados

```bash
git init                                  
git add .                              
git commit -m "Projeto de produtos com Flask e SQLAlchemy"  
git branch -M main                       
git remote add origin https://github.com/enzoemiliolopes-beep/Avalia-o-final-DS.git  
git push -u origin main                   
