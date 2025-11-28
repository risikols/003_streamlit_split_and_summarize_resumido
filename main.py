import streamlit as st
from PyPDF2 import PdfReader

# Configuración de la página
st.set_page_config(page_title="PDF/TXT Summarizer Local", layout="wide")
st.title("📝 Local PDF/TXT Summarizer (Simulado)")

# Carga de archivo
uploaded_file = st.file_uploader("Sube tu PDF o TXT aquí", type=["pdf", "txt"])

def summarize_text(text: str, max_lines: int = 5) -> str:
    """
    Genera un resumen simulado: toma la primera frase de cada párrafo
    y limita el resumen a `max_lines` líneas.
    """
    lines = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if paragraph:
            # Tomamos solo la primera frase de cada párrafo
            first_sentence = paragraph.split(".")[0].strip()
            if first_sentence:
                lines.append(first_sentence + ".")
        if len(lines) >= max_lines:
            break
    return "\n".join(lines)

if uploaded_file:
    # Lectura del archivo según tipo
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    else:
        text = uploaded_file.getvalue().decode("utf-8")

    st.subheader("Texto extraído")
    st.text_area("Contenido del archivo", text, height=300)

    if st.button("Generar resumen"):
        if not text.strip():
            st.error("No se encontró texto en el archivo.")
        else:
            with st.spinner("Generando resumen..."):
                summary = summarize_text(text, max_lines=5)  # ≤5 líneas
                st.subheader("Resumen generado")
                st.write(summary)
