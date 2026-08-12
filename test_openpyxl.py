import streamlit as st
import sys

st.title("🔧 Test environnement TMF LOGISTICS")

st.write("Version Python :", sys.version)

try:
    import openpyxl

    st.success(
        f"✅ openpyxl est installé : version {openpyxl.__version__}"
    )

except Exception as e:

    st.error(
        f"❌ openpyxl n'est PAS disponible : {e}"
    )

try:
    import pandas

    st.success(
        f"✅ pandas est installé : version {pandas.__version__}"
    )

except Exception as e:

    st.error(
        f"❌ pandas : {e}"
    )