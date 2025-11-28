import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumidor Realista", layout="wide")
st.title("Resumidor de PDF/TXT")

uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"], key="uploader")

def resumir_bloque(texto, max_sentencias=3):
    """
    Resume un bloque de texto tomando las primeras max_sentencias de cada párrafo
    """
    bloques = texto.split("\n\n")
    resumen_parrafos = []
    for bloque in bloques:
        frases = [f.strip() for f in bloque.split(".") if f.strip()]
        resumen_parrafos.append(". ".join(frases[:max_sentencias]))
    return "\n\n".join(resumen_parrafos)

def dividir_en_bloques(texto, max_parrafos=50):
    """
    Divide el texto en bloques de hasta max_parrafos párrafos
    """
    bloques = texto.split("\n\n")
    for i in range(0, len(bloques), max_parrafos):
        yield "\n\n".join(bloques[i:i + max_parrafos])

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
        st.text_area("Texto completo", texto, height=300, key="texto_original_area")

        st.subheader("Resumen generado")

        # Procesar el texto en bloques para documentos grandes
        resumen_total = []
        for i, bloque in enumerate(dividir_en_bloques(texto, max_parrafos=50)):
            resumen_bloque = resumir_bloque(bloque, max_sentencias=3)
            resumen_total.append(resumen_bloque)
        
        resumen_completo = "\n\n".join(resumen_total)
        st.text_area("Resumen", resumen_completo, height=400, key="resumen_area")

