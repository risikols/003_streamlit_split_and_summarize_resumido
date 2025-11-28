import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resumidor Realista", layout="wide")
st.title("Resumidor de PDF/TXT")

# ---------------------- Funciones ----------------------
def dividir_en_bloques(texto, max_parrafos=50):
    """
    Divide el texto en bloques de hasta max_parrafos párrafos.
    """
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    for i in range(0, len(parrafos), max_parrafos):
        yield "\n\n".join(parrafos[i:i + max_parrafos])

def resumir_bloque(texto, max_sentencias=3):
    """
    Resume un bloque completo tomando hasta max_sentencias frases en total.
    Mantiene la separación de bloques.
    """
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]

    # Dividir todo el bloque en frases
    todas_las_frases = []
    for parrafo in parrafos:
        frases = [f.strip() for f in parrafo.split(". ") if f.strip()]
        todas_las_frases.extend(frases)

    # Tomar solo las primeras max_sentencias frases
    resumen_frases = todas_las_frases[:max_sentencias]

    # Volver a unir en un texto
    return ". ".join(resumen_frases) + ("." if resumen_frases else "")

def leer_pdf(file):
    reader = PdfReader(file)
    texto = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texto += page_text + "\n\n"
    return texto

def leer_txt(file):
    return file.read().decode("utf-8")

# ---------------------- Inicializar session_state ----------------------
if "texto" not in st.session_state:
    st.session_state.texto = ""
if "resumen" not in st.session_state:
    st.session_state.resumen = ""
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 0

# ---------------------- File uploader ----------------------
uploaded_file = st.file_uploader("Seleccione archivo", type=["pdf", "txt"], key="uploader")

if uploaded_file:
    st.session_state.file_counter += 1
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

    # Generar resumen por bloques
    if st.session_state.texto:
        resumen_total = []
        for bloque in dividir_en_bloques(st.session_state.texto, max_parrafos=50):
            resumen_total.append(resumir_bloque(bloque, max_sentencias=3))  # máximo 3 frases por bloque
        st.session_state.resumen = "\n\n".join(resumen_total)

# ---------------------- Mostrar contenido ----------------------
if st.session_state.texto:
    st.subheader("Texto original")
    st.text_area(
        "Texto completo",
        st.session_state.texto,
        height=300,
        key=f"texto_original_area_{st.session_state.file_counter}"
    )

if st.session_state.resumen:
    st.subheader("Resumen generado")
    st.text_area(
        "Resumen",
        st.session_state.resumen,
        height=400,
        key=f"resumen_area_{st.session_state.file_counter}"
    )
