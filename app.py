#API -Interface para disponibilizar recursos e/ou funcionalidades
#1. Objetivo: Criar uma API que disponibiliza a consulta, criação, edição e exclusão de livros
#2. URL base -localhost.com
"""3. Endpoints - Tipos de funcionalidades: 
localhost/livros (GET)
localhost/livros (PUT)
localhost/livros/id (GET)
localhost/livros/id (PUT)
localhost/livros/id (DEL)
"""
from flask import Flask
from rotas.livros import livros_bp
app = Flask(__name__)
app.register_blueprint(livros_bp)



if __name__ == '__main__':
    app.run(host='localhost', debug=True)

