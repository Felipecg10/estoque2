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

# --- SISTEMA DE SENHA ---
senha_correta = "admin"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acesso Restrito")

    senha = st.text_input("Digite a senha:", type="password")

    if st.button("Entrar"):
        if senha == senha_correta:
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("❌ Senha incorreta!")

    st.stop()

# --- BOTÃO DE SAIR ---
st.sidebar.button("Sair", on_click=lambda: logout())

def logout():
    st.session_state.autenticado = False
    st.experimental_rerun()

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

    # Carrega produtos
    produtos = listar_produtos()

    if produtos:
        # Lista apenas nomes
        nomes = [p[1] for p in produtos]
        nome_escolhido = st.selectbox("Selecione o produto", nomes)

        # Descobre o ID verdadeiro do produto selecionado
        id_produto = None
        for p in produtos:
            if p[1] == nome_escolhido:
                id_produto = p[0]
                break

        quantidade = st.number_input("Quantidade a adicionar", min_value=1, step=1)

        if st.button("Adicionar ao estoque"):
            if atualizar_estoque(id_produto, quantidade, "entrada"):
                st.success(f"Entrada registrada para '{nome_escolhido}'!")
            else:
                st.error("Erro ao atualizar o estoque.")
    else:
        st.warning("Nenhum produto cadastrado.")

# --- SAÍDA DE ESTOQUE (POR NOME) ---
elif opcao == "Saída de Estoque":
    st.subheader("Registrar saída de produtos")

    produtos = listar_produtos()

    if produtos:
        nomes = [p[1] for p in produtos]
        nome_escolhido = st.selectbox("Selecione o produto", nomes)

        id_produto = next((p[0] for p in produtos if p[1] == nome_escolhido), None)

        quantidade = st.number_input("Quantidade a remover", min_value=1, step=1)

        if st.button("Remover"):
            if atualizar_estoque(id_produto, quantidade, "saida"):
                st.success(f"Saída registrada: -{quantidade} em '{nome_escolhido}'")
            else:
                st.error("Erro ao atualizar o estoque.")
    else:
        st.warning("Nenhum produto cadastrado.")

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

