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
from flask import Flask, request
from conexao import *
app = Flask(__name__)

@app.route('/livros', methods=['GET'])
def listar_livros():
    try:
        livros = listar(dados_conexao)
        return livros
    except Exception as erro:
        return jsonify({'erro': str(erro)})

    
@app.route('/livros/<int:id>', methods=['GET'])
def consultar(id):
    try:
        livros = consulta(dados_conexao, id)
        if livros is None:
            return jsonify({'erro': 'Este livro não existe'}), 404
        else:
            return livros
    except Exception as erro:
        return jsonify({'erro': str(erro)})


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({'erro': 'O corpo da requisição deve ser válido <400>'}), 400
    if 'titulo' not in dados:
        return jsonify({'erro': 'Você não digitou o título <400>'}), 400
    if 'autor' not in dados:
        return jsonify({'erro': 'Você não digitou o autor <400>'}), 400
    titulo = dados['titulo']
    autor = dados['autor']
    try:
        teste = cadastrar_livro(dados_conexao, titulo, autor)
        if teste == True:     
            return 'livro cadastrado com sucesso', 201
    except Exception as erro:
        return jsonify({'erro': str(erro)})


@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    try:
        if excluir(dados_conexao, id) == 0:
            return jsonify({'erro': 'O livro selecionado não existe'}), 404
        else:
            return 'Livro excluído com sucesso!'
    except Exception as erro:
        return jsonify({'Erro': str(erro)})


@app.route('/livros', methods=['PUT'])
def editar():
    dados = request.get_json()
    if not isinstance(dados, dict):
        return jsonify({'erro': 'O corpo da requisição deve ser válido <400>'}), 400
    if not isinstance(dados['id'], int):
        return jsonify({'erro': 'O id é inválido'}), 400
    if 'titulo' not in dados:
        return jsonify({'erro': 'Você não digitou o título <400>'}), 400
    if 'autor' not in dados:
        return jsonify({'erro': 'Você não digitou o autor <400>'}), 400
    if 'id' not in dados:
        return jsonify({'erro': 'Você não digitou o id <400>'}), 400
    titulo = dados['titulo']
    autor = dados['autor']
    id = dados['id']
    try:
        if editar_porid(dados_conexao, id, titulo, autor) == 0:   
            return jsonify({'erro': 'O livro selecionado não existe'}), 404
        else:
            return 'Livro editado com sucesso!', 201
    except Exception as erro:
        return jsonify({'erro': str(erro)})



if __name__ == '__main__':
    app.run(host='localhost', debug=True)

