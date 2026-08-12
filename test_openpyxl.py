import streamlit as st
import sys

st.set_page_config(
    page_title="Test OpenPyXL",
    page_icon="🔧"
)

st.title("🔧 Test OpenPyXL")

st.write("### Environnement Python")

st.write(
    f"Version Python : `{sys.version}`"
)


# ============================================================
# TEST OPENPYXL
# ============================================================

st.write("### Test du module OpenPyXL")

try:

    import openpyxl

    st.success(
        f"✅ OpenPyXL fonctionne correctement."
    )

    st.info(
        f"Version OpenPyXL : {openpyxl.__version__}"
    )

except ImportError as e:

    st.error(
        f"❌ OpenPyXL n'est pas installé : {e}"
    )

except Exception as e:

    st.error(
        f"❌ Erreur OpenPyXL : {e}"
    )


# ============================================================
# TEST PANDAS
# ============================================================

st.write("### Test Pandas")

try:

    import pandas as pd

    st.success(
        f"✅ Pandas fonctionne."
    )

    st.info(
        f"Version Pandas : {pd.__version__}"
    )

except Exception as e:

    st.error(
        f"❌ Erreur Pandas : {e}"
    )


# ============================================================
# TEST LECTURE EXCEL
# ============================================================

st.write("### Test du moteur Excel")

try:

    import pandas as pd

    moteur = pd.io.excel._util.get_default_engine(
        "test.xlsx",
        mode="reader"
    )

    st.info(
        f"Moteur Excel détecté : `{moteur}`"
    )

except Exception as e:

    st.warning(
        f"⚠️ Impossible de déterminer le moteur Excel : {e}"
    )
