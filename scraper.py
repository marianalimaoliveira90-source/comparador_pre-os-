import pandas as pd
from datetime import datetime

# Lista completa de produtos de supermercado
BASE_DADOS_PRODUTOS = [
    # --- ALIMENTOS BÁSICOS ---
    {"Categoria": "Alimentos Básicos", "Produto": "Arroz Tio João 5kg", "Marca": "Tio João", "Preço (R$)": 26.90, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Arroz Caminho Novo 5kg", "Marca": "Caminho Novo", "Preço (R$)": 23.80, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Arroz Emoções 5kg", "Marca": "Emoções", "Preço (R$)": 25.90, "Fornecedor": "Atacadista Local", "Cidade": "Itabaiana"},
    {"Categoria": "Alimentos Básicos", "Produto": "Feijão Carioca Kicaldo 1kg", "Marca": "Kicaldo", "Preço (R$)": 7.50, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Feijão Carioca Turquesa 1kg", "Marca": "Turquesa", "Preço (R$)": 6.99, "Fornecedor": "GBarbosa", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Açúcar Cristal União 1kg", "Marca": "União", "Preço (R$)": 4.20, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Açúcar Cristal Pindorama 1kg", "Marca": "Pindorama", "Preço (R$)": 3.79, "Fornecedor": "Assaí", "Cidade": "Nossa Senhora do Socorro"},
    {"Categoria": "Alimentos Básicos", "Produto": "Óleo de Soja Liza 900ml", "Marca": "Liza", "Preço (R$)": 5.80, "Fornecedor": "GBarbosa", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Óleo de Soja Soya 900ml", "Marca": "Soya", "Preço (R$)": 5.65, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Farinha de Trigo Dona Benta 1kg", "Marca": "Dona Benta", "Preço (R$)": 4.29, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Alimentos Básicos", "Produto": "Macarrão Espaguete Barilla 500g", "Marca": "Barilla", "Preço (R$)": 4.99, "Fornecedor": "Assaí", "Cidade": "Aracaju"},

    # --- BEBIDAS E MATINAIS ---
    {"Categoria": "Bebidas e Matinais", "Produto": "Café Maratá 250g", "Marca": "Maratá", "Preço (R$)": 9.90, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Bebidas e Matinais", "Produto": "Café Pilão 500g", "Marca": "Pilão", "Preço (R$)": 14.90, "Fornecedor": "Atacado Local", "Cidade": "Itabaiana"},
    {"Categoria": "Bebidas e Matinais", "Produto": "Leite Integral Betânia 1L", "Marca": "Betânia", "Preço (R$)": 4.99, "Fornecedor": "GBarbosa", "Cidade": "Aracaju"},
    {"Categoria": "Bebidas e Matinais", "Produto": "Achocolatado Nescau 370g", "Marca": "Nescau", "Preço (R$)": 6.80, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Bebidas e Matinais", "Produto": "Refrigerante Coca-Cola 2L", "Marca": "Coca-Cola", "Preço (R$)": 8.99, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Bebidas e Matinais", "Produto": "Suco de Caju Concentrado Maratá 500ml", "Marca": "Maratá", "Preço (R$)": 4.19, "Fornecedor": "Assaí", "Cidade": "Aracaju"},

    # --- LIMPEZA ---
    {"Categoria": "Limpeza", "Produto": "Sabão em Pó Omo Lavagem Perfeita 1.6kg", "Marca": "Omo", "Preço (R$)": 19.90, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Limpeza", "Produto": "Sabão em Pó Brilhante 1.6kg", "Marca": "Brilhante", "Preço (R$)": 16.90, "Fornecedor": "Assaí", "Cidade": "Nossa Senhora do Socorro"},
    {"Categoria": "Limpeza", "Produto": "Detergente Neutro Ypê 500ml", "Marca": "Ypê", "Preço (R$)": 2.39, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Limpeza", "Produto": "Limpador Multiuso Veja 500ml", "Marca": "Veja", "Preço (R$)": 5.89, "Fornecedor": "GBarbosa", "Cidade": "Aracaju"},
    {"Categoria": "Limpeza", "Produto": "Água Sanitária Qboa 2L", "Marca": "Qboa", "Preço (R$)": 6.49, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Limpeza", "Produto": "Amaciante Concentrado Downy 1L", "Marca": "Downy", "Preço (R$)": 15.90, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Limpeza", "Produto": "Sabão em Barra Ypê 5un", "Marca": "Ypê", "Preço (R$)": 11.50, "Fornecedor": "Supermercado Local", "Cidade": "Itabaiana"},

    # --- HIGIENE E BELEZA ---
    {"Categoria": "Higiene e Beleza", "Produto": "Desodorante Aerosol Rexona 150ml", "Marca": "Rexona", "Preço (R$)": 12.90, "Fornecedor": "GBarbosa", "Cidade": "Aracaju"},
    {"Categoria": "Higiene e Beleza", "Produto": "Creme Dental Colgate Total 12 90g", "Marca": "Colgate", "Preço (R$)": 4.79, "Fornecedor": "Assaí", "Cidade": "Aracaju"},
    {"Categoria": "Higiene e Beleza", "Produto": "Papel Higiênico Neve Folha Dupla 12un", "Marca": "Neve", "Preço (R$)": 18.50, "Fornecedor": "Atacadão", "Cidade": "Aracaju"},
    {"Categoria": "Higiene e Beleza", "Produto": "Sabonete em Barra Dove 90g", "Marca": "Dove", "Preço (R$)": 3.49, "Fornecedor": "Atacadão", "Cidade": "Nossa Senhora do Socorro"}
]

def buscar_produtos(categoria="Todas", termo_busca="", cidade="Todas"):
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    dados = []

    for item in BASE_DADOS_PRODUTOS:
        item_copia = item.copy()
        item_copia["Data Atualização"] = data_atual
        dados.append(item_copia)

    df = pd.DataFrame(dados)

    # Filtro por Categoria
    if categoria != "Todas":
        df = df[df["Categoria"] == categoria]

    # Filtro por Cidade
    if cidade != "Todas":
        df = df[df["Cidade"] == cidade]

    # Filtro por Busca do Usuário
    if termo_busca:
        mascara = (
            df["Produto"].str.contains(termo_busca, case=False, na=False) |
            df["Marca"].str.contains(termo_busca, case=False, na=False) |
            df["Fornecedor"].str.contains(termo_busca, case=False, na=False)
        )
        df = df[mascara]

    return df