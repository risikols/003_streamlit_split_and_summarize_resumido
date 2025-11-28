import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumen Simulado", layout="wide")
st.title("Resumidor PDF/TXT (Simulado)")

uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"])

def resumir_texto(texto):
    """
    Resumen simulado: toma los primeros 3 bloques de texto separados por salto de línea.
    """
    bloques = [b.strip() for b in texto.split("\n") if b.strip()]
    resumen = " ".join(bloques[:3]) if bloques else ""
    return resumen

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            texto = "".join(page.extract_text() + "\n" for page in reader.pages)
            resumen = resumir_texto(texto)
            st.subheader("Resumen del PDF")
            st.write(resumen)
        except Exception as e:
            st.error(f"Error al leer el PDF: {e}")
    elif uploaded_file.type == "text/plain":
        try:
            texto = uploaded_file.read().decode("utf-8")
            resumen = resumir_texto(texto)
            st.subheader("Resumen del TXT")
            st.write(resumen)
        except Exception as e:
            st.error(f"Error al leer el TXT: {e}")
