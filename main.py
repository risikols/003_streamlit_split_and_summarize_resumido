import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="Resumidor Local", layout="wide")
st.title("Resumidor Local PDF/TXT (Simulado)")

uploaded_file = st.file_uploader("Sube un PDF o TXT", type=["pdf", "txt"])

def summarize_text(text, max_sentences=3):
    """
    Función que simula un resumen.
    Devuelve las primeras `max_sentences` frases del texto.
    """
    # Separar por puntos
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    summary = ". ".join(sentences[:max_sentences])
    if summary:
        summary += "."
    return summary

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
    else:
        st.error("Formato no soportado")
        st.stop()

    st.subheader("Texto original")
    st.text_area("Texto completo:", text, height=200)

    st.subheader("Resumen simulado")
    # Puedes cambiar max_sentences para resúmenes más largos o más cortos
    summary = summarize_text(text, max_sentences=3)
    st.text_area("Resumen:", summary, height=150)
