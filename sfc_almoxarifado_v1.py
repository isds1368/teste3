
import streamlit as st
import hashlib
import random
import string
from datetime import datetime

st.set_page_config(page_title="SFC - Almoxarifado", layout="wide")

st.markdown("""
<style>
body { background-color: #111; }
.main { background-color: #111; color: white; }
.title { text-align: center; font-size: 42px; font-weight: bold; color: white; }
button { background-color: #8B0000 !important; color: white !important; border-radius: 8px !important; height: 45px !important; }
.card { padding: 20px; border-radius: 10px; background-color: #1c1c1c; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def gerar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def menu():
    cols = st.columns(6)
    pages = ["home","entrada","saida","estoque","notas","dashboard"]
    names = ["Início","Entrada","Saída","Estoque","Notas","Dashboard"]

    for i, col in enumerate(cols):
        with col:
            if st.button(names[i]):
                st.session_state.page = pages[i]

def home():
    st.markdown("<div class='title'>SFC - ALMOXARIFADO</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Entrar", use_container_width=True):
            st.session_state.page = "dashboard"

def entrada():
    st.subheader("Entrada de Produtos")
    with st.form("entrada"):
        nome = st.text_input("Produto")
        qtd = st.number_input("Quantidade", min_value=1.0)
        unidade = st.selectbox("Unidade", ["UN","CX"])
        file = st.file_uploader("Nota Fiscal", type=["pdf"])
        if st.form_submit_button("Registrar Entrada"):
            st.success("Entrada registrada")

def saida():
    st.subheader("Saída de Produtos")
    with st.form("saida"):
        produto = st.text_input("Produto")
        qtd = st.number_input("Quantidade", min_value=1.0)
        setor = st.text_input("Setor Solicitante")
        retirante = st.text_input("Nome do Retirante")
        if st.form_submit_button("Registrar Saída"):
            st.success("Saída registrada")

def estoque():
    st.subheader("Controle de Estoque")
    st.markdown("<div class='card'>Tabela de estoque aqui</div>", unsafe_allow_html=True)

def notas():
    st.subheader("Notas Fiscais")
    st.write("Envio para financeiro")

def dashboard():
    st.subheader("Dashboard")
    col1,col2,col3 = st.columns(3)
    col1.markdown("<div class='card'>Produtos<br><b>120</b></div>", unsafe_allow_html=True)
    col2.markdown("<div class='card'>Estoque Baixo<br><b>8</b></div>", unsafe_allow_html=True)
    col3.markdown("<div class='card'>Movimentações<br><b>25</b></div>", unsafe_allow_html=True)

menu()

if st.session_state.page == "home":
    home()
elif st.session_state.page == "entrada":
    entrada()
elif st.session_state.page == "saida":
    saida()
elif st.session_state.page == "estoque":
    estoque()
elif st.session_state.page == "notas":
    notas()
elif st.session_state.page == "dashboard":
    dashboard()
