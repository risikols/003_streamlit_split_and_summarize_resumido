import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumidor PDF/TXT", layout="wide")
st.title("Resumidor Simulado de Archivos PDF y TXT")

uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"])

def resumir_texto(texto, max_lineas=3):
    """
    Devuelve un resumen simulado: los primeros max_lineas bloques de texto.
    """
    bloques = [b.strip() for b in texto.split("\n") if b.strip()]
    resumen = " ".join(bloques[:max_lineas]) if bloques else ""
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
