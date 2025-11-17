import streamlit as st
from database import *

# Inicializa banco
criar_tabela()

# Configuração da página
st.set_page_config(page_title="Controle de Estoque", page_icon="📊", layout="centered")
st.title("📊 Sistema de Controle de Estoque")

# Menu lateral
menu = [
    "Listar Produtos",
    "Buscar Produto",
    "Entrada de Estoque",
    "Saída de Estoque"
]
opcao = st.sidebar.selectbox("Menu", menu)

# --- LISTAR PRODUTOS ---
if opcao == "Listar Produtos":
    st.subheader("📋 Lista de Produtos")
    produtos = listar_produtos()

    if produtos:
        for p in produtos:
            alerta = "⚠️" if p[2] < p[3] else ""
            st.write(
                f"**ID:** {p[0]} | **Nome:** {p[1]} | **Qtd:** {p[2]} | **Mín:** {p[3]} | **Fornecedor:** {p[4]} {alerta}"
            )
    else:
        st.info("Nenhum produto cadastrado.")

# --- BUSCAR PRODUTO ---
elif opcao == "Buscar Produto":
    st.subheader("🔎 Buscar Produto")
    termo = st.text_input("Digite parte do nome do produto:")

    if st.button("Buscar"):
        resultados = buscar_produto(termo)
        if resultados:
            for p in resultados:
                st.write(
                    f"**ID:** {p[0]} | **Nome:** {p[1]} | **Qtd:** {p[2]} | **Mín:** {p[3]} | **Fornecedor:** {p[4]}"
                )
        else:
            st.warning("Nenhum produto encontrado.")

# --- ENTRADA DE ESTOQUE ---
elif opcao == "Entrada de Estoque":
    st.subheader("📦 Entrada de Estoque")
    id_produto = st.number_input("ID do produto", min_value=1, step=1)
    quantidade = st.number_input("Quantidade a adicionar", min_value=1, step=1)

    if st.button("Adicionar ao estoque"):
        if atualizar_estoque(id_produto, quantidade, "entrada"):
            st.success(f"✅ {quantidade} unidades adicionadas ao estoque!")
        else:
            st.error("Produto não encontrado.")

# --- SAÍDA DE ESTOQUE ---
elif opcao == "Saída de Estoque":
    st.subheader("📤 Saída de Estoque")
    id_produto = st.number_input("ID do produto", min_value=1, step=1)
    quantidade = st.number_input("Quantidade a remover", min_value=1, step=1)

    if st.button("Remover do estoque"):
        if atualizar_estoque(id_produto, quantidade, "saida"):
            st.success(f"✅ {quantidade} unidades removidas do estoque!")
        else:
            st.error("Produto não encontrado.")
