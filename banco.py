import sqlite3
import hashlib

def conectar():
    return sqlite3.connect("mercearia_privada.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela de Produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            fornecedor TEXT
        )
    """)
    
    # Tabela de Usuários para Login
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def gerar_hash_senha(senha):
    """Criptografa a senha para salvar com segurança."""
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario_inicial(usuario, senha):
    """Cria o seu usuário de acesso se ele ainda não existir."""
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = gerar_hash_senha(senha)
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Usuário já existe
    conn.close()

def verificar_login(usuario, senha):
    """Verifica se o usuário e senha estão corretos."""
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = gerar_hash_senha(senha)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_hash))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def adicionar_produto(nome, categoria, quantidade, preco_custo, preco_venda, fornecedor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, quantidade, preco_custo, preco_venda, fornecedor)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, categoria, quantidade, preco_custo, preco_venda, fornecedor))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, categoria, quantidade, preco_custo, preco_venda, fornecedor FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

if __name__ == "__main__":
    criar_tabelas()