import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="Herramienta para resumir archivos", layout="wide")
st.title("RESUME tus PDF/TXT")

# ---------------------- Funciones ----------------------
def dividir_en_bloques_por_lineas(texto):
    """
    Divide el texto en bloques usando como separador
    más de dos líneas en blanco consecutivas.
    """
    bloques = re.split(r'\n{3,}', texto.replace('\r\n', '\n').replace('\r', '\n'))
    bloques = [b.strip() for b in bloques if b.strip()]
    return bloques

def resumir_bloque(texto, max_sentencias=3):
    """
    Resume un bloque completo tomando hasta max_sentencias frases en total.
    """
    # Dividir todo el bloque en frases
    frases = [f.strip() for f in re.split(r'\. ', texto) if f.strip()]
    resumen_frases = frases[:max_sentencias]
    return ". ".join(resumen_frases) + ("." if resumen_frases else "")

def leer_pdf(file):
    reader = PdfReader(file)
    texto = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texto += page_text + "\n\n"
    return texto

def leer_txt(file):
    return file.read().decode("utf-8")

# ---------------------- Inicializar session_state ----------------------
if "texto" not in st.session_state:
    st.session_state.texto = ""
if "resumen" not in st.session_state:
    st.session_state.resumen = ""
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 0

# ---------------------- File uploader ----------------------
uploaded_file = st.file_uploader("Seleccione archivo", type=["pdf", "txt"], key="uploader")

if uploaded_file:
    st.session_state.file_counter += 1
    st.session_state.texto = ""
    st.session_state.resumen = ""

    # Leer archivo
    if uploaded_file.type == "application/pdf":
        st.session_state.texto = leer_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        st.session_state.texto = leer_txt(uploaded_file)
    else:
        st.error("Formato no soportado")
        st.session_state.texto = ""

    # Generar resumen por bloques (separados por más de dos líneas en blanco)
    if st.session_state.texto:
        bloques = dividir_en_bloques_por_lineas(st.session_state.texto)
        resumen_total = [resumir_bloque(b, max_sentencias=3) for b in bloques]  # máximo 2 frases por bloque
        st.session_state.resumen = "\n\n".join(resumen_total)

# ---------------------- Mostrar contenido ----------------------
if st.session_state.texto:
    st.subheader("Texto original")
    st.text_area(
        "Texto completo",
        st.session_state.texto,
        height=300,
        key=f"texto_original_area_{st.session_state.file_counter}"
    )

if st.session_state.resumen:
    st.subheader("Resumen generado")
    st.text_area(
        "Resumen",
        st.session_state.resumen,
        height=400,
        key=f"resumen_area_{st.session_state.file_counter}"
    )

