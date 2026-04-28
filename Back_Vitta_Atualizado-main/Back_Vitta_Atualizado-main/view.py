from flask import Flask, jsonify, request
import fdb
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÃO DO FIREBIRD ---
CONFIG = {
    'dsn': r'C:\CAMINHO\SEU_BANCO.FDB',  # Mude para o caminho real do seu arquivo
    'user': 'SYSDBA',
    'password': 'masterkey',
    'charset': 'UTF8'
}


def get_db_connection():
    return fdb.connect(**CONFIG)


# --- ROTAS PARA USUÁRIOS ---

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, ativo FROM USUARIO")
    # Transforma o resultado em uma lista de dicionários
    usuarios = [{"id": r[0], "nome": r[1], "email": r[2], "ativo": r[3]} for r in cur.fetchall()]
    conn.close()
    return jsonify(usuarios)


@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """INSERT INTO USUARIO (nome, email, senha, tipo, data_criacao, ativo) 
             VALUES (?, ?, ?, ?, ?, ?)"""
    cur.execute(sql, (dados['nome'], dados['email'], dados['senha'],
                      dados['tipo'], datetime.now(), True))
    conn.commit()
    conn.close()
    return jsonify({"status": "Usuario criado com sucesso!"}), 201


# --- ROTAS PARA PRODUTOS ---

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco, ativo FROM produtos")
    produtos = [{"id": r[0], "nome": r[1], "preco": float(r[2]), "ativo": r[3]} for r in cur.fetchall()]
    conn.close()
    return jsonify(produtos)


# --- ROTAS PARA PEDIDOS (Relacionamento) ---

@app.route('/pedidos/mesa/<int:mesa_id>', methods=['GET'])
def listar_pedidos_por_mesa(mesa_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Exemplo de consulta com JOIN usando suas tabelas
    sql = """
        SELECT p.id, p.data_pedido, p.status, m.numero 
        FROM pedidos p 
        JOIN mesas m ON p.mesa_id = m.id 
        WHERE p.mesa_id = ?
    """
    cur.execute(sql, (mesa_id,))
    pedidos = [{"id": r[0], "data": str(r[1]), "status": r[2], "mesa_num": r[3]} for r in cur.fetchall()]
    conn.close()
    return jsonify(pedidos)


# --- ROTA PARA CRIAR UM ITEM NO PEDIDO ---

@app.route('/itens-pedido', methods=['POST'])
def adicionar_item():
    d = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    # Cálculo automático do subtotal (quantidade * preco)
    subtotal = d['quantidade'] * d['preco_unitario']

    sql = """INSERT INTO itenspedido (pedido_id, produto_id, quantidade, preco_unitario, subtotal) 
             VALUES (?, ?, ?, ?, ?)"""
    cur.execute(sql, (d['pedido_id'], d['produto_id'], d['quantidade'], d['preco_unitario'], subtotal))

    conn.commit()
    conn.close()
    return jsonify({"message": "Item adicionado!"}), 201


# --- ROTA PARA PAGAMENTO ---

@app.route('/pagamentos', methods=['POST'])
def registrar_pagamento():
    d = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """INSERT INTO pagamentos (mesa_id, valor_total, forma_pagamento, data_pagamento, hora_pagamento) 
             VALUES (?, ?, ?, ?, ?)"""
    agora = datetime.now()
    cur.execute(sql, (d['mesa_id'], d['valor_total'], d['forma'], agora.date(), agora.time()))

    conn.commit()
    conn.close()
    return jsonify({"status": "Pagamento registrado!"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)