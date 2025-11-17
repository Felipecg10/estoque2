import sqlite3
from pathlib import Path

# Caminho absoluto da pasta onde este arquivo está
BASE_DIR = Path(__file__).parent.resolve()

# Caminho completo do banco
DB_PATH = BASE_DIR / "estoque.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            quantidade_minima INTEGER NOT NULL,
            fornecedor TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

# Adiciona novo produto
def adicionar_produto(nome, quantidade_estoque, quantidade_minima, fornecedor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, quantidade_estoque, quantidade_minima, fornecedor) VALUES (?, ?, ?, ?)",
        (nome, quantidade_estoque, quantidade_minima, fornecedor)
    )
    conexao.commit()
    conexao.close()

# Lista todos os produtos
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    return produtos

# Busca produto por nome
def buscar_produto(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{nome}%",))
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

# Deleta produto
def deletar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conexao.commit()
    conexao.close()

# Atualiza quantidade (entrada ou saída)
def atualizar_estoque(id_produto, quantidade, operacao="entrada"):
    conexao = conectar()
    cursor = conexao.cursor()
    # Busca quantidade atual
    cursor.execute("SELECT quantidade_estoque FROM produtos WHERE id = ?", (id_produto,))
    result = cursor.fetchone()
    if not result:
        conexao.close()
        return False  # produto não encontrado

    qtd_atual = result[0]
    if operacao == "entrada":
        nova_qtd = qtd_atual + quantidade
    elif operacao == "saida":
        nova_qtd = max(0, qtd_atual - quantidade)  # evita estoque negativo
    else:
        conexao.close()
        return False

    cursor.execute("UPDATE produtos SET quantidade_estoque = ? WHERE id = ?", (nova_qtd, id_produto))
    conexao.commit()
    conexao.close()
    return True

# Lista produtos abaixo do estoque mínimo
def produtos_abaixo_minimo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE quantidade_estoque < quantidade_minima")
    resultados = cursor.fetchall()
    conexao.close()
    return resultados
