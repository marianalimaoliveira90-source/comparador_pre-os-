import streamlit as st
import pandas as pd
import google.generativeai as genai
from banco import criar_tabelas, cadastrar_usuario_inicial, verificar_login, adicionar_produto, listar_produtos

# Inicializa o banco de dados
criar_tabelas()

# Configuração do usuário e senha
USUARIO_DONO = "edijan"
SENHA_DONO = "edijan1972"  # Sua senha configurada

cadastrar_usuario_inicial(USUARIO_DONO, SENHA_DONO)

st.set_page_config(page_title="Gestão Privada - Mercearia", layout="wide")

# Controle de Sessão de Login
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔒 Acesso Restrito - Mercearia")
    
    with st.form("form_login"):
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        btn_entrar = st.form_submit_button("Entrar")
        
        if btn_entrar:
            if verificar_login(usuario_input, senha_input):
                st.session_state["autenticado"] = True
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
else:
    # --- ÁREA LOGADA ---
    st.sidebar.title("👤 Painel do Proprietário")
    if st.sidebar.button("Sair / Logout"):
        st.session_state["autenticado"] = False
        st.rerun()

    st.title("📦 Sistema de Gestão - Mercearia")

    aba = st.radio("Navegação:", ["📋 Ver Estoque", "➕ Cadastrar Produto", "🤖 Assistente IA"], horizontal=True)
    st.divider()

    if aba == "➕ Cadastrar Produto":
        st.subheader("Cadastrar Novo Item")
        with st.form("form_produto"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Produto")
                categoria_digitada = st.text_input("Categoria")
                quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
            with col2:
                preco_custo = st.number_input("Preço de Custo (R$)", min_value=0.0, format="%.2f")
                preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f")
                fornecedor = st.text_input("Fornecedor")
                
            submit = st.form_submit_button("Salvar Produto")
            if submit:
                if nome and categoria_digitada:
                    adicionar_produto(nome, categoria_digitada, quantidade, preco_custo, preco_venda, fornecedor)
                    st.success(f"✅ Produto '{nome}' cadastrado com sucesso!")
                else:
                    st.error("⚠️ Preencha o Nome e a Categoria.")

    elif aba == "📋 Ver Estoque":
        st.subheader("Produtos Cadastrados")
        produtos = listar_produtos()
        if produtos:
            df = pd.DataFrame(produtos, columns=["ID", "Produto", "Categoria", "Estoque", "Preço Custo (R$)", "Preço Venda (R$)", "Fornecedor"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum produto cadastrado ainda.")

from google import genai

st.header("Assistente Virtual de Compras e Estoque")

api_key_input = st.text_input("Insira sua API Key do Google Gemini:", type="password", key="gemini_api_key_input")
pergunta = st.text_area("Faça uma pergunta sobre gestão, ofertas ou precificação:", key="gemini_pergunta_input")

if st.button("Consultar IA", key="btn_consultar_ia"):
    api_key = api_key_input.strip() if api_key_input else ""
    
    if not api_key:
        st.warning("Por favor, insira a API Key.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            produtos = listar_produtos()
            contexto = f"Dados do estoque atual: {produtos}\n\nPergunta do usuário: {pergunta}"
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=contexto,
            )
            
            st.markdown("### Resposta da IA:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Erro ao consultar a IA: {e}")