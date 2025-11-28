import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="PDF/TXT Summarizer Local", layout="wide")
st.title("📝 Resumen Local de PDF/TXT")

# Selección del archivo
uploaded_file = st.file_uploader("Sube tu PDF o TXT aquí", type=["pdf", "txt"])

# Número de líneas del resumen
num_lines = st.slider("Número de líneas del resumen", min_value=1, max_value=20, value=5)

def summarize_text(text, max_lines=5):
    """
    Función simple para simular un resumen: divide en frases y toma las primeras max_lines.
    """
    # Dividir por líneas y luego limpiar espacios vacíos
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # También puedes separar por puntos para frases más finas
    sentences = []
    for line in lines:
        sentences.extend([s.strip() for s in line.split('.') if s.strip()])
    # Tomar solo las primeras max_lines frases
    summary = sentences[:max_lines]
    return ". ".join(summary) + ("." if summary else "")

if uploaded_file:
    text = ""
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.error(f"No se pudo leer el PDF: {e}")
    elif file_type == "txt":
        try:
            text = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"No se pudo leer el TXT: {e}")

    if text.strip():
        st.subheader("Contenido extraído")
        st.text_area("Texto completo", text, height=300)

        st.subheader("Resumen generado")
        summary = summarize_text(text, max_lines=num_lines)
        st.write(summary)
    else:
        st.warning("No se encontró texto en el archivo.")
