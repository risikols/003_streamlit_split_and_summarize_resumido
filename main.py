import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumidor Realista", layout="wide")
st.title("Resumidor de PDF/TXT")

# ---------------------- Funciones ----------------------
def resumir_bloque(texto, max_sentencias=3):
    bloques = texto.split("\n\n")
    resumen_parrafos = []
    for bloque in bloques:
        frases = [f.strip() for f in bloque.split(".") if f.strip()]
        resumen_parrafos.append(". ".join(frases[:max_sentencias]))
    return "\n\n".join(resumen_parrafos)

def dividir_en_bloques(texto, max_parrafos=50):
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

# ---------------------- Inicializar session_state ----------------------
if "texto" not in st.session_state:
    st.session_state.texto = ""
if "resumen" not in st.session_state:
    st.session_state.resumen = ""

# ---------------------- File uploader ----------------------
uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"], key="uploader")

if uploaded_file:
    # Resetear siempre el estado
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

    # Generar resumen
    if st.session_state.texto:
        resumen_total = []
        for bloque in dividir_en_bloques(st.session_state.texto, max_parrafos=50):
            resumen_total.append(resumir_bloque(bloque, max_sentencias=3))
        st.session_state.resumen = "\n\n".join(resumen_total)

    # Forzar recarga de la app para que los nuevos widgets se muestren
    st.experimental_rerun()

# ---------------------- Mostrar contenido ----------------------
if st.session_state.texto:
    st.subheader("Texto original")
    st.text_area("Texto completo", st.session_state.texto, height=300, key="texto_original_area")

if st.session_state.resumen:
    st.subheader("Resumen generado")
    st.text_area("Resumen", st.session_state.resumen, height=400, key="resumen_area")


