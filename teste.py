import os
import sqlite3
import database

# === CONFIGURAÇÃO ===
BANCO_TESTE = "estoque_teste.db"

# Usa um banco de dados temporário para não alterar o real
def conectar_teste():
    return sqlite3.connect(BANCO_TESTE)

# === FUNÇÃO AUXILIAR PARA AMBIENTE DE TESTE ===
def preparar_banco_teste():
    """Cria um banco de dados de teste limpo."""
    if os.path.exists(BANCO_TESTE):
        os.remove(BANCO_TESTE)

    conexao = conectar_teste()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            quantidade_minima INTEGER NOT NULL,
            fornecedor TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()
    print("✅ Banco de teste criado com sucesso.")

# === TESTES ===
def testar_insercao():
    print("\n🧩 Teste: Inserir produtos...")
    database.conectar = conectar_teste  # redireciona conexão para banco de teste
    database.adicionar_produto("Parafuso", 50, 10, "ABC Metais")
    database.adicionar_produto("Porca", 5, 20, "ABC Metais")
    database.adicionar_produto("Arruela", 100, 30, "FixTudo Ltda")
    print("✅ Inserções concluídas com sucesso.")

def testar_listagem():
    print("\n📋 Teste: Listar produtos...")
    produtos = database.listar_produtos()
    for p in produtos:
        print(f"ID={p[0]} | Nome={p[1]} | Estoque={p[2]} | Mín={p[3]} | Fornecedor={p[4]}")
    assert len(produtos) == 3, "Erro: número de produtos incorreto"
    print("✅ Listagem funcionando.")

def testar_busca():
    print("\n🔍 Teste: Buscar produto pelo nome...")
    resultados = database.buscar_produto("Porca")
    assert len(resultados) == 1, "Erro: busca retornou resultado incorreto"
    print(f"✅ Produto encontrado: {resultados[0][1]}")

def testar_atualizacao_estoque():
    print("\n📦 Teste: Entrada e saída de estoque...")
    produtos = database.listar_produtos()
    id_parafuso = produtos[0][0]

    # Entrada de 20
    database.atualizar_estoque(id_parafuso, 20, "entrada")
    # Saída de 15
    database.atualizar_estoque(id_parafuso, 15, "saida")

    # Verifica resultado
    atualizados = database.listar_produtos()
    for p in atualizados:
        if p[0] == id_parafuso:
            print(f"🔁 Estoque final de {p[1]}: {p[2]}")
            assert p[2] == 55, "Erro: cálculo de estoque incorreto"
    print("✅ Atualização de estoque funcionando corretamente.")

def testar_alerta_estoque_baixo():
    print("\n⚠️ Teste: Produtos abaixo do mínimo...")
    baixo = database.produtos_abaixo_minimo()
    for p in baixo:
        print(f"⚠️ {p[1]} — Estoque: {p[2]} | Mínimo: {p[3]}")
    assert any(p[1] == "Porca" for p in baixo), "Erro: produto com estoque baixo não detectado"
    print("✅ Alerta de estoque baixo funcionando.")

def testar_delecao():
    print("\n🗑️ Teste: Deletar produto...")
    produtos = database.listar_produtos()
    id_para_deletar = produtos[1][0]  # Porca
    database.deletar_produto(id_para_deletar)
    restantes = database.listar_produtos()
    nomes_restantes = [p[1] for p in restantes]
    assert "Porca" not in nomes_restantes, "Erro: produto não foi deletado"
    print("✅ Deleção funcionando corretamente.")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    print("🚀 Iniciando testes de controle de estoque...\n")
    preparar_banco_teste()
    testar_insercao()
    testar_listagem()
    testar_busca()
    testar_atualizacao_estoque()
    testar_alerta_estoque_baixo()
    testar_delecao()
    print("\n✅ Todos os testes foram concluídos com sucesso!")
