import streamlit as st
import pandas as pd
from datetime pip install datetime
pip install sqlite3
pip install pdflumber

st.set_page_config(page_title="Contas a Pagar", layout="wide")

conn = sqlite3.connect("sistema.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT UNIQUE,
        senha TEXT,
        perfil TEXT
    )
    """)
    conn.commit()

init_db()

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

def verificar_login(matricula, senha):
    user = cursor.execute("SELECT * FROM usuarios WHERE matricula=?", (matricula,)).fetchone()
    if user and bcrypt.checkpw(senha.encode(), user[2]):
        return user
    return None

usuarios_count = cursor.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]

if usuarios_count == 0:
    st.title("🚀 Primeiro Acesso - Criar Administrador")

    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")

    if st.button("Criar Administrador"):
        cursor.execute(
            "INSERT INTO usuarios (matricula, senha, perfil) VALUES (?, ?, ?)",
            (matricula, hash_senha(senha), "admin")
        )
        conn.commit()
        st.success("Administrador criado! Reinicie a aplicação.")
    st.stop()

if "user" not in st.session_state:
    st.title("🔐 Login")

    matricula = st.text_input("Matrícula")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = verificar_login(matricula, senha)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Login inválido")

    st.stop()

perfil = st.session_state.user[3]

st.sidebar.title("Menu")

menu_options = ["Dashboard"]

if perfil == "admin":
    menu_options.append("Usuários")

menu = st.sidebar.selectbox("Navegação", menu_options)

if menu == "Dashboard":
    st.title("📊 Dashboard")
    st.write(f"Bem-vindo, {st.session_state.user[1]}")

if menu == "Usuários" and perfil == "admin":
    st.title("👥 Gerenciamento de Usuários")

    st.subheader("Cadastrar novo usuário")

    nova_matricula = st.text_input("Matrícula")
    nova_senha = st.text_input("Senha", type="password")
    novo_perfil = st.selectbox("Perfil", ["admin", "financeiro", "visualizacao"])

    if st.button("Cadastrar usuário"):
        try:
            cursor.execute(
                "INSERT INTO usuarios (matricula, senha, perfil) VALUES (?, ?, ?)",
                (nova_matricula, hash_senha(nova_senha), novo_perfil)
            )
            conn.commit()
            st.success("Usuário criado com sucesso")
        except:
            st.error("Erro: matrícula já existe")

    st.subheader("Usuários cadastrados")
    usuarios = pd.read_sql("SELECT id, matricula, perfil FROM usuarios", conn)
    st.dataframe(usuarios)
