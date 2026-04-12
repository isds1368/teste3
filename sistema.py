import streamlit as st
import hashlib
import pytesseract
from PIL import Image
import re
from datetime import datetime

# =========================
# 🔐 AUTENTICAÇÃO
# =========================

usuarios = {
    "admin": {
        "senha": hashlib.sha256("1234".encode()).hexdigest(),
        "nome": "Administrador"
    }
}

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_login(usuario, senha):
    if usuario in usuarios:
        return usuarios[usuario]["senha"] == hash_senha(senha)
    return False

# =========================
# 📄 LEITURA PDF
# =========================

def extrair_texto_pdf(arquivo):
    texto = ""

    try:
        with pdfplumber.open(arquivo) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""
    except:
        pass

    if texto.strip() == "":
        try:
            with pdfplumber.open(arquivo) as pdf:
                for pagina in pdf.pages:
                    imagem = pagina.to_image(resolution=300).original
                    texto += pytesseract.image_to_string(imagem)
        except:
            pass

    return texto

# =========================
# 🔍 EXTRAÇÃO DE DADOS
# =========================

def extrair_dados(texto):
    dados = {}

    cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
    valor = re.search(r'R\$\s?\d+[.,]\d{2}', texto)
    data = re.search(r'\d{2}/\d{2}/\d{4}', texto)

    if cnpj:
        dados["cnpj"] = cnpj.group()
    if valor:
        dados["valor"] = valor.group()
    if data:
        dados["data"] = data.group()

    return dados

# =========================
# 🧠 IDENTIFICAÇÃO DOCUMENTO
# =========================

def identificar_tipo(texto):
    t = texto.lower()

    if "nota fiscal de serviço" in t or "iss" in t:
        return "nota_servico"
    elif "danfe" in t or "nf-e" in t:
        return "danfe"
    elif "fatura" in t:
        return "fatura"
    elif "recibo" in t:
        return "recibo"
    else:
        return "outro"

# =========================
# 📊 SESSION
# =========================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================
# 🔐 LOGIN
# =========================

if not st.session_state.logado:
    st.title("Login")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if verificar_login(user, senha):
            st.session_state.logado = True
            st.session_state.usuario = user
            st.rerun()
        else:
            st.error("Login inválido")

    st.stop()

# =========================
# 📥 UPLOAD PDF
# =========================

st.title("Nova Conta via PDF")

arquivo = st.file_uploader("Envie o PDF", type=["pdf"])

if arquivo:
    texto = extrair_texto_pdf(arquivo)

    st.subheader("Texto extraído")
    st.text_area("", texto, height=150)

    dados = extrair_dados(texto)
    tipo = identificar_tipo(texto)

    st.write("Tipo identificado:", tipo)

    # =========================
    # 🧾 FORMULÁRIO
    # =========================

    descricao = st.text_input("Descrição", "Documento importado")
    valor = st.text_input("Valor", dados.get("valor", ""))
    data = st.text_input("Data de vencimento", dados.get("data", ""))

    # =========================
    # 📌 CONTRATO
    # =========================

    contrato = st.radio("Pertence a contrato?", ["Não", "Sim"])

    numero_contrato = ""
    if contrato == "Sim":
        numero_contrato = st.text_input("Número do contrato")

    # =========================
    # ⚙️ REGRA DE STATUS
    # =========================

    status_operacional = ""
    divergencia = ""
    motivo = ""

    if tipo == "nota_servico":
        status_operacional = "Aguardando criação de folha"

        divergencia = st.radio(
            "Há divergência?",
            ["Não há divergência", "Erro de faturamento", "Falta de verba"]
        )

        if divergencia == "Erro de faturamento":
            motivo = "erro de faturamento"

        elif divergencia == "Falta de verba":
            motivo = "falta de verba"

    else:
        status_operacional = "Enviar para pagamento"

    st.write("Status definido:", status_operacional)

    # =========================
    # 💾 SALVAR
    # =========================

    if st.button("Salvar Conta"):

        agora = datetime.now()

        st.success("Conta registrada com sucesso!")

        st.write("📌 Auditoria:")
        st.write(f"Último registro feito por: {st.session_state.usuario}")
        st.write(f"Data: {agora.strftime('%d/%m/%Y %H:%M')}")

        st.write("📊 Resumo:")
        st.write({
            "descricao": descricao,
            "valor": valor,
            "data": data,
            "tipo_documento": tipo,
            "status_operacional": status_operacional,
            "divergencia": motivo,
            "contrato": numero_contrato
        })

        st.write("📝 Follow-up automático:")

        if tipo == "nota_servico":
            if motivo:
                st.write(f"Divergência identificada: {motivo}")
            else:
                st.write("Aguardando criação de folha")
        else:
            st.write("Documento enviado para pagamento")
