import pyodbc
import os
from flask import jsonify
from dotenv import load_dotenv



load_dotenv() #Carrega os dados de login do servidor MySQL que estão no arquivo .env

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSS = os.getenv("DB_PASSS")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")
dados_conexao = (f"DRIVER={DB_DRIVER};"
                    f"Server={DB_HOST};"
                    f"Database={DB_NAME};"
                    f"User={DB_USER};"
                    f"Password={DB_PASSS};")


def cadastrar_livro(dados_conexao, titulo, autor):
    try:
        with pyodbc.connect(dados_conexao) as conexao:
            print('Conectado com sucesso!')
            cursor = conexao.cursor()
            comando = """insert into llivros(titulo, autor)
            values
            (?, ?)"""
            cursor.execute(comando, (titulo, autor))
            conexao.commit()
            return True
    except pyodbc.Error as erro:
        print(f'Erro no banco de dados {erro}')
        return jsonify({'erro': str(erro)})
    except Exception as erro:
        print(f'Erro inesperado, código -> {erro}')
        return jsonify({'erro': str(erro)})

def listar(dados_conexao):
    try:
        with pyodbc.connect(dados_conexao) as conexao:
            print('Conectado com sucesso')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM llivros")
            dados = cursor.fetchall()
            colunas = [coluna[0] for coluna in cursor.description]
            dados_formatados = []
            for l in dados:
                dados_formatados.append(dict(zip(colunas, l)))
            return jsonify(dados_formatados)
    except pyodbc.Error as erro:
        print('Erro no banco de dados')
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        print('Erro geral')
        return jsonify({'erro': str(erro)}), 500
    

def consulta(dados_conexao, id):
    try:
         with pyodbc.connect(dados_conexao) as conexao:
            print('Conectado com sucesso')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM llivros where id = ?", (id,))
            dados = cursor.fetchall()
            if not dados:
                return None
            colunas = []
            for c in cursor.description:
                colunas.append(c[0])
            print(colunas)
            dados_formatados = []
            for l in dados:
                dados_formatados.append(dict(zip(colunas, l)))
            return jsonify(dados_formatados)
    except pyodbc.Error as erro:
        print('Erro no banco de dados')
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        print('Erro geral')
        return jsonify({'erro': str(erro)}), 500

    
def excluir(dados_conexao, id):
    try:
        with pyodbc.connect(dados_conexao) as conexao:
            print('Conectado com sucesso!')
            cursor = conexao.cursor()
            comando = "delete from llivros where id = ?;"
            cursor.execute(comando, (id,))
            conexao.commit()
            c = cursor.rowcount
            return c
    except pyodbc.Error as erro:
        print('Erro no banco de dados')
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        print('Erro geral')
        return jsonify({'erro': str(erro)}), 500
        

def editar_porid(dados_conexao, id, titulo, autor):
    try:
        with pyodbc.connect(dados_conexao) as conexao:
            print('Conectado com sucesso')
            cursor = conexao.cursor()
            cursor.execute("update llivros set titulo = ?, autor = ? where id = ?", (titulo, autor, id))
            conexao.commit()
            c = cursor.rowcount
            return c
    except pyodbc.Error as erro:
        print('Erro no banco de dados')
        return jsonify({'erro': str(erro)}), 500
    except Exception as erro:
        print('Erro geral')
        return jsonify({'erro': str(erro)}), 500


excluir(dados_conexao, 999)