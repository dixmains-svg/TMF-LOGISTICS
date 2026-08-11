import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Camions - TMF LOGISTICS",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Gestion des Camions")

st.caption("TMF LOGISTICS — Parc véhicules")


# ============================================================
# DONNÉES CAMIONS
# ============================================================

# Pour le moment, lecture depuis la base SQLite
try:
    from database import get_connection

    conn = get_connection()

    df_camions = pd.read_sql_query(
        """
        SELECT
            id,
            camion,
            remorque,
            chauffeur,
            statut,
            client,
            mission
        FROM camions
        ORDER BY id
        """,
        conn
    )

    conn.close()

except Exception as e:

    st.error("Impossible de charger les camions.")

    st.code(str(e))

    df_camions = pd.DataFrame(
        columns=[
            "id",
            "camion",
            "remorque",
            "chauffeur",
            "statut",
            "client",
            "mission"
        ]
    )


# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔎 Rechercher un camion",
    placeholder="Camion, chauffeur, client..."
)


if recherche:

    masque = (
        df_camions.astype(str)
        .apply(
            lambda colonne:
            colonne.str.contains(
                recherche,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    df_camions = df_camions[masque]


# ============================================================
# AFFICHAGE
# ============================================================

if df_camions.empty:

    st.info("🚚 Aucun camion trouvé.")

else:

    st.dataframe(
        df_camions,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# STATISTIQUES
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🚚 Nombre de camions",
        df_camions["camion"].nunique()
    )

with col2:
    st.metric(
        "📋 Camions affichés",
        len(df_camions)
    )
