import streamlit as st
from database import *

# Inicializa banco
criar_tabela()

# Configuração da página
st.set_page_config(page_title="Controle de Estoque", page_icon="📦", layout="centered")
st.title("📦 Sistema de Controle de Estoque")

menu = [
    "Cadastrar Produto",
    "Listar Produtos",
    "Buscar Produto",
    "Entrada de Estoque",
    "Saída de Estoque",
    "Excluir Produto",
    "Alerta de Estoque Baixo"
]
opcao = st.sidebar.selectbox("Menu", menu)

# --- CADASTRAR PRODUTO ---
if opcao == "Cadastrar Produto":
    st.subheader("Adicionar novo produto")
    nome = st.text_input("Nome do produto")
    quantidade_estoque = st.number_input("Quantidade em estoque", min_value=0, step=1)
    quantidade_minima = st.number_input("Quantidade mínima em estoque", min_value=0, step=1)
    fornecedor = st.text_input("Fornecedor")

    if st.button("Salvar produto"):
        if nome and fornecedor:
            adicionar_produto(nome, quantidade_estoque, quantidade_minima, fornecedor)
            st.success(f"Produto '{nome}' adicionado com sucesso!")
        else:
            st.warning("Preencha todos os campos obrigatórios.")

# --- LISTAR PRODUTOS ---
elif opcao == "Listar Produtos":
    st.subheader("Lista de produtos cadastrados")
    produtos = listar_produtos()

    if produtos:
        for p in produtos:
            alerta = "⚠️" if p[2] < p[3] else ""
            st.write(f"**ID:** {p[0]} | **Nome:** {p[1]} | **Qtd:** {p[2]} | **Mín:** {p[3]} | **Fornecedor:** {p[4]} {alerta}")
    else:
        st.info("Nenhum produto cadastrado.")

# --- BUSCAR PRODUTO ---
elif opcao == "Buscar Produto":
    st.subheader("Buscar produto por nome")
    termo = st.text_input("Digite parte do nome do produto")

    if st.button("Buscar"):
        resultados = buscar_produto(termo)
        if resultados:
            for p in resultados:
                st.write(f"**ID:** {p[0]} | **Nome:** {p[1]} | **Qtd:** {p[2]} | **Mín:** {p[3]} | **Fornecedor:** {p[4]}")
        else:
            st.warning("Nenhum produto encontrado.")

# --- ENTRADA DE ESTOQUE ---
elif opcao == "Entrada de Estoque":
    st.subheader("Registrar entrada de produtos")
    id_produto = st.number_input("ID do produto", min_value=1, step=1)
    quantidade = st.number_input("Quantidade a adicionar", min_value=1, step=1)

    if st.button("Adicionar ao estoque"):
        if atualizar_estoque(id_produto, quantidade, "entrada"):
            st.success("Estoque atualizado com sucesso!")
        else:
            st.error("Produto não encontrado.")

# --- SAÍDA DE ESTOQUE ---
elif opcao == "Saída de Estoque":
    st.subheader("Registrar saída de produtos")
    id_produto = st.number_input("ID do produto", min_value=1, step=1)
    quantidade = st.number_input("Quantidade a remover", min_value=1, step=1)

    if st.button("Remover do estoque"):
        if atualizar_estoque(id_produto, quantidade, "saida"):
            st.success("Saída registrada com sucesso!")
        else:
            st.error("Produto não encontrado.")

# --- EXCLUIR PRODUTO ---
elif opcao == "Excluir Produto":
    st.subheader("Excluir produto pelo ID")
    id_produto = st.number_input("Informe o ID do produto", min_value=1, step=1)
    if st.button("Excluir"):
        deletar_produto(id_produto)
        st.success(f"Produto com ID {id_produto} excluído com sucesso!")

# --- ALERTA DE ESTOQUE BAIXO ---
elif opcao == "Alerta de Estoque Baixo":
    st.subheader("Produtos com estoque abaixo do mínimo")
    abaixo = produtos_abaixo_minimo()

    if abaixo:
        for p in abaixo:
            st.error(f"⚠️ {p[1]} — Estoque: {p[2]} | Mínimo: {p[3]} | Fornecedor: {p[4]}")
    else:
        st.success("✅ Todos os produtos estão com estoque adequado.")

