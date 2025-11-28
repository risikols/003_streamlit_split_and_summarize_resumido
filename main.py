import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="PDF/TXT Summarizer Local", layout="wide")
st.title("📝 PDF/TXT Summarizer (Local, sin OpenAI)")

# Subida de archivo
uploaded_file = st.file_uploader("Sube tu PDF o TXT aquí", type=["pdf", "txt"])

def extract_text(file):
    """Extrae texto de PDF o TXT"""
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    else:
        return file.getvalue().decode("utf-8").strip()

def local_summary(text, max_sentences=10):
    """
    Genera un resumen local simple.
    Toma las primeras 'max_sentences' oraciones del texto.
    """
    # Dividir en oraciones básicas
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = " ".join(sentences[:max_sentences])
    if len(sentences) > max_sentences:
        summary += "..."
    return summary

if uploaded_file:
    text = extract_text(uploaded_file)
    if not text:
        st.error("No se encontró texto en el archivo.")
    else:
        st.subheader("Texto extraído")
        st.text_area("Contenido del archivo", text, height=300)

        if st.button("Generar resumen"):
            with st.spinner("Generando resumen local..."):
                summary = local_summary(text, max_sentences=10)
                st.subheader("Resumen generado (local)")
                st.write(summary)
