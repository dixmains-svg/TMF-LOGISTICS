import streamlit as st
from pathlib import Path
import base64

from database import init_database, statistiques


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)

# ============================================================
# INITIALISER LA BASE
# ============================================================

init_database()


# ============================================================
# ARRIÈRE-PLAN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"

if BACKGROUND_PATH.exists():

    with open(BACKGROUND_PATH, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(255, 255, 255, 0.88),
                    rgba(255, 255, 255, 0.88)
                ),
                url("data:image/jpeg;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "⚠️ Image d'arrière-plan introuvable : "
        "assets/background.jpg"
    )
