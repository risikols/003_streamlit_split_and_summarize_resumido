import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="PDF/TXT Summarizer (Simulado)", layout="wide")
st.title("📝 Summarizador de textos (Simulado)")

# Cargar archivo
uploaded_file = st.file_uploader("Sube tu PDF o TXT aquí", type=["pdf", "txt"])
text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")

    if not text.strip():
        st.error("No se encontró texto en el archivo.")
    else:
        st.subheader("Texto extraído")
        st.text_area("Contenido", text, height=300)

        if st.button("Generar resumen"):
            with st.spinner("Generando resumen simulado..."):
                # Dividir el texto en bloques por párrafos
                blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
                summaries = []

                for block in blocks:
                    # Simulación: tomar las primeras 2 líneas de cada bloque
                    lines = block.splitlines()
                    summaries.append("\n".join(lines[:2]))

                final_summary = "\n\n".join(summaries)
                st.subheader("Resumen simulado")
                st.write(final_summary)
