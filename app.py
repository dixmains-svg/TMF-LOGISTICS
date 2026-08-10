import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 TMF LOGISTICS")

st.write("### 🔎 Vérification des fichiers")

base = Path(__file__).parent

st.write("Dossier de l'application :")
st.code(str(base))

st.write("### Fichiers présents")

for fichier in base.rglob("*"):
    if fichier.is_file():
        st.write(str(fichier.relative_to(base)))
