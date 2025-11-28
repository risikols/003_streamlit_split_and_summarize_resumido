import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

st.title("Simulador de resúmenes PDF/TXT")

uploaded_file = st.file_uploader("Sube un archivo TXT o PDF", type=["txt", "pdf"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        content = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        st.error("Formato no soportado")
        content = ""

    st.subheader("Contenido original")
    st.text_area("Texto completo", content, height=200)

    # Simulación de resumen
    lines = content.splitlines()
    simulated_summary = " ".join(lines[:3])  # Tomamos las primeras 3 líneas como resumen
    st.subheader("Resumen simulado")
    st.text_area("Resumen", simulated_summary, height=100)
