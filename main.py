import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumen Simulado", layout="wide")
st.title("Resumidor PDF/TXT (Simulado)")

# Subida de archivo
uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"])

def resumir_texto(texto):
    """
    Resumen simulado: toma el texto y devuelve los primeros 3 bloques de información.
    Cada bloque separado por un punto o salto de línea.
    """
    bloques = [b.strip() for b in texto.split("\n") if b.strip()]
    if len(bloques) > 3:
        bloques = bloques[:3]
    resumen = " ".join(bloques)
    return resumen

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text() + "\n"
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
