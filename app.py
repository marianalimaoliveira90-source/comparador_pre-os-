import streamlit as st
import pandas as pd
from google import genai
from banco import criar_tabelas, cadastrar_usuario_inicial, verificar_login, adicionar_produto, listar_produtos

# Inicializa o banco de dados
criar_tabelas()

# Configuração do usuário e senha de acesso
USUARIO_DONO = "edijan"
SENHA_DONO = "edijan1972"

cadastrar_usuario_inicial(USUARIO_DONO, SENHA_DONO)

st.set_page_config(page_title="Gestão Privada - Mercearia", layout="wide")

# Controle de Sessão de Login
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔒 Login de Acesso - Gestão Privada")
    usuario_input = st.text_input("Usuário")
    senha_input = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if verificar_login(usuario_input, senha_input):
            st.session_state["autenticado"] = True
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# Conteúdo do Sistema após o Login
st.title("📊 Sistema de Gestão - Minha Mercearia")

aba = st.radio("Navegação:", ["📦 Ver Estoque", "➕ Cadastrar Produto", "🤖 Assistente IA"], horizontal=True)
st.divider()

if aba == "📦 Ver Estoque":
    st.subheader("Produtos Cadastrados")
    produtos = listar_produtos()
    if produtos:
        df = pd.DataFrame(produtos, columns=["ID", "Nome", "Categoria", "Quantidade", "Preço Custo", "Preço Venda", "Fornecedor"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum produto cadastrado ainda.")

elif aba == "➕ Cadastrar Produto":
    st.subheader("Cadastrar Novo Item")
    with st.form("form_produto"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Produto (ex: Arroz Tio João 5kg)")
            categoria_digitada = st.text_input("Categoria (ex: Alimentos, Limpeza, Bebidas)")
            quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
        with col2:
            preco_custo = st.number_input("Preço de Custo (R$)", min_value=0.0, format="%.2f")
            preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f")
            fornecedor = st.text_input("Fornecedor (ex: Atacadão, Assaí)")
        
        salvar = st.form_submit_button("Salvar Produto")
        if salvar:
            if nome:
                adicionar_produto(nome, categoria_digitada, quantidade, preco_custo, preco_venda, fornecedor)
                st.success(f"Produto '{nome}' cadastrado com sucesso!")
            else:
                st.warning("Preencha o nome do produto.")

elif aba == "🤖 Assistente IA":
    st.subheader("Assistente Virtual de Compras e Estoque")
    api_key = st.text_input("Insira sua API Key do Google Gemini:", type="password")
    pergunta = st.text_area("Faça uma pergunta sobre gestão, ofertas ou precificação:")

    if st.button("Consultar IA"):
        if api_key and pergunta:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=pergunta,
                )
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao consultar a IA: {e}")
        else:
            st.warning("Preencha a chave de API e a sua pergunta.")
