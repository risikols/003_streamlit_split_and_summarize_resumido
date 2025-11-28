import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import Counter
import numpy as np

# Configuración
st.set_page_config(page_title="Resumidor PDF/TXT", page_icon="📝")
st.title("Resumidor Automático Realista")

# Subida de archivo
uploaded_file = st.file_uploader("Sube un archivo PDF o TXT", type=["pdf", "txt"])

# Funciones de procesamiento
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # reemplaza espacios múltiples por uno solo
    return text.strip()

def get_sentences(text):
    # Separa el texto en oraciones simples
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

def summarize(text, num_sentences=3):
    stopwords = set([
        "de","la","que","el","en","y","a","los","del","se","las","por","un",
        "para","con","no","una","su","al","lo","como","más","pero","sus","le",
        "ya","o","este","sí","porque","esta","entre","cuando","muy","sin",
        "sobre","también","me","hasta","hay","donde","quien","desde","todo"
    ])
    
    sentences = get_sentences(text)
    if len(sentences) <= num_sentences:
        return " ".join(sentences)
    
    # Contar palabras relevantes
    words = [w.lower() for w in re.findall(r'\w+', text) if w.lower() not in stopwords]
    freq = Counter(words)
    
    # Puntuación de cada oración
    sentence_scores = []
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r'\w+', s))
        sentence_scores.append((score, s))
    
    # Seleccionar las oraciones top
    top_sentences = [s for _, s in sorted(sentence_scores, reverse=True)[:num_sentences]]
    
    return " ".join(top_sentences)

# Extracción de texto
if uploaded_file:
    text = ""
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.error(f"Error leyendo PDF: {e}")
    elif uploaded_file.type == "text/plain":
        try:
            text = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error leyendo TXT: {e}")

    if text:
        text = clean_text(text)
        st.subheader("Texto original (primeros 1000 caracteres):")
        st.write(text[:1000])

        # Generar resumen
        summary = summarize(text, num_sentences=3)
        st.subheader("Resumen automático:")
        st.write(summary)
    else:
        st.warning("No se pudo extraer texto del archivo.")
