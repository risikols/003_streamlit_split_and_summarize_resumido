import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="Resumidor Realista", layout="wide")
st.title("Resumidor de PDF/TXT")

uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"])

def resumir_texto(texto, max_sentencias=3):
    """Genera un resumen simple tomando las primeras frases de cada bloque."""
    bloques = texto.split("\n\n")  # separar por párrafos
    resumen = []
    for bloque in bloques:
        frases = [f.strip() for f in bloque.split(".") if f.strip()]
        resumen.extend(frases[:max_sentencias])
    return ". ".join(resumen) + ("." if resumen else "")

def leer_pdf(file):
    reader = PdfReader(file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n\n"
    return texto

def leer_txt(file):
    return file.read().decode("utf-8")

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        texto = leer_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        texto = leer_txt(uploaded_file)
    else:
        st.error("Formato no soportado")
        texto = ""
    
    if texto:
        st.subheader("Texto original")
        st.text_area("Texto completo", texto, height=300)
        
        st.subheader("Resumen generado")
        resumen = resumir_texto(texto, max_sentencias=3)
        st.text_area("Resumen", resumen, height=200)

        
        st.subheader("Resumen generado")
        resumen = resumir_texto(texto, max_sentencias=3)
        st.text_area("Resumen", resumen, height=200)
