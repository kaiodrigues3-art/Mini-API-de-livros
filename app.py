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
        return livros
    except Exception as erro:
        return jsonify({'erro': str(erro)})


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({'erro': 'O corpo da requisição deve ser válido <400>'})
    if dados is None:
        return jsonify({'erro': 'É necessário enviar um json válido <400>'})
    if 'titulo' not in dados:
        return jsonify({'erro': 'Você não digitou o título <400>'})
    if 'autor' not in dados:
        return jsonify({'erro': 'Você não digitou o autor <400>'})
    titulo = dados['titulo']
    autor = dados['autor']
    try:
        cadastrar_livro(dados_conexao, titulo, autor)
        return 'livro cadastrado com sucesso'
    except Exception as erro:
        return jsonify({'erro': str(erro)})


@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    excluir(dados_conexao, id)
    return 'Livro excluído com sucesso!'


@app.route('/livros', methods=['PUT'])
def editar():
    dados = request.get_json()
    titulo = dados['titulo']
    autor = dados['autor']
    id = dados['id']
    editar_porid(dados_conexao, id, titulo, autor)
    return 'Livro editado com sucesso!'





app.run(host='localhost', debug=True)

