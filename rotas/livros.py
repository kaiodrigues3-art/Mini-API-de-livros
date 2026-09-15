from flask import Blueprint
from flask import request
from flask import jsonify
import pyodbc
from funcoes.conexao import (
    dados_conexao, listar, consulta, cadastrar_livro, excluir, editar_porid
)

livros_bp = Blueprint('rlivros', __name__)


@livros_bp.route('/livros', methods=['GET'])
def listar_livros():
    try:
        livros = listar(dados_conexao)
        return jsonify(livros)
    except pyodbc.Error as erro:
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        return jsonify({'erro': str(erro)}), 500

    
@livros_bp.route('/livros/<int:id>', methods=['GET'])
def consultar(id):
    try:
        livros = consulta(dados_conexao, id)
        if livros is None:
            return jsonify({'erro': 'Este livro não existe'}), 404
        else:
            return jsonify(livros)
    except pyodbc.Error as erro:
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        return jsonify({'erro': str(erro)}), 500


@livros_bp.route('/cadastro', methods=['POST'])
def cadastrar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({'erro': 'O corpo da requisição deve ser válido'}), 400
    if 'titulo' not in dados:
        return jsonify({'erro': 'Você não digitou o título'}), 400
    if 'autor' not in dados:
        return jsonify({'erro': 'Você não digitou o autor'}), 400
    titulo = dados['titulo']
    autor = dados['autor']
    try:
        teste = cadastrar_livro(dados_conexao, titulo, autor)
        if teste == True:     
            return 'livro cadastrado com sucesso', 201
        else:
            return jsonify({'erro': 'não foi possível cadastrar o livro'}), 500
    except pyodbc.Error as erro:
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        return jsonify({'erro': str(erro)}), 500


@livros_bp.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    try:
        if excluir(dados_conexao, id) == 0:
            return jsonify({'erro': 'O livro selecionado não existe'}), 404
        else:
            return 'Livro excluído com sucesso!'
    except pyodbc.Error as erro:
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        return jsonify({'Erro': str(erro)}), 500


@livros_bp.route('/livros', methods=['PUT'])
def editar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({'erro': 'O corpo da requisição deve ser válido'}), 400
    if 'id' not in dados:
        return jsonify({'erro': 'Você não digitou o id'}), 400
    if not isinstance(dados['id'], int):
        return jsonify({'erro': 'O id é inválido'}), 400
    if 'titulo' not in dados:
        return jsonify({'erro': 'Você não digitou o título'}), 400
    if 'autor' not in dados:
        return jsonify({'erro': 'Você não digitou o autor'}), 400
    if not isinstance(dados['autor'], str):
        return jsonify({'erro': 'O autor deve ser um texto'}), 400
    if not isinstance(dados['titulo'], str):
        return jsonify({'erro': 'O título deve ser um texto'}), 400
    if not dados['titulo'].strip():
        return jsonify({'erro': 'O titulo não pode estar vazio'}), 400
    if not dados['autor'].strip():
        return jsonify({'erro': 'O autor não pode estar vazio'}), 400
    titulo = dados['titulo']
    autor = dados['autor']
    id = dados['id']
    try:
        if editar_porid(dados_conexao, id, titulo, autor) == 0:   
            return jsonify({'erro': 'O livro selecionado não existe'}), 404
        else:
            return 'Livro editado com sucesso!', 201
    except pyodbc.Error as erro:
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        return jsonify({'erro': str(erro)}), 500