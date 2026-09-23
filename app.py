import streamlit as st
import pandas as pd
from google import genai
from banco import criar_tabelas, adicionar_produto, listar_produtos

# Inicializa o banco de dados
criar_tabelas()

st.set_page_config(page_title="Gestão de Mercearia", layout="wide")

st.title("📦 Sistema de Gestão - Minha Mercearia")

# Aba de navegação
aba = st.radio("Navegação:", ["📋 Ver Estoque", "➕ Cadastrar Produto", "🤖 Assistente IA"], horizontal=True)

st.divider()

if aba == "➕ Cadastrar Produto":
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
            
        submit = st.form_submit_button("Salvar Produto")
        
        if submit:
            if nome and categoria_digitada:
                adicionar_produto(nome, categoria_digitada, quantidade, preco_custo, preco_venda, fornecedor)
                st.success(f"✅ Produto '{nome}' cadastrado com sucesso!")
            else:
                st.error("⚠️ Por favor, preencha o Nome e a Categoria do produto.")

elif aba == "📋 Ver Estoque":
    st.subheader("Produtos Cadastrados")
    
    produtos = listar_produtos()
    
    if produtos:
        df = pd.DataFrame(produtos, columns=["ID", "Produto", "Categoria", "Estoque", "Preço Custo (R$)", "Preço Venda (R$)", "Fornecedor"])
        
        st.dataframe(
            df.style.format({"Preço Custo (R$)": "R$ {:.2f}", "Preço Venda (R$)": "R$ {:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum produto cadastrado ainda.")

elif aba == "🤖 Assistente IA":
    st.header("Assistente Virtual de Compras e Estoque")

    api_key_input = st.text_input("Insira sua API Key do Google Gemini:", type="password", key="gemini_api_key_input")
    pergunta = st.text_area("Faça uma pergunta sobre gestão, ofertas ou precificação:", key="gemini_pergunta_input")

    if st.button("Consultar IA", key="btn_consultar_ia"):
        api_key = api_key_input.strip() if api_key_input else ""
        
        if not api_key:
            st.warning("Por favor, insira a sua API Key do Gemini.")
        elif not pergunta:
            st.warning("Por favor, digite uma pergunta.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                produtos = listar_produtos()
                contexto = f"Dados do estoque atual: {produtos}\n\nPergunta do usuário: {pergunta}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contexto,
                )
                
                st.markdown("### Resposta da IA:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Erro ao consultar a IA: {e}")
