import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# IMPORT DATABASE
# ============================================================

from database import (
    get_ordres_mission,
    get_camions,
    get_chauffeurs,
    get_clients,
    statistiques
)

# ============================================================
# CONFIGURATION
# ============================================================

st.title("📊 Rapports")

st.caption(
    "Statistiques et rapports du système TMF LOGISTICS"
)

st.divider()

# ============================================================
# STATISTIQUES
# ============================================================

try:
    stats = statistiques()

    nombre_om = stats.get("ordres_mission", 0)
    nombre_camions = stats.get("camions", 0)
    nombre_chauffeurs = stats.get("chauffeurs", 0)
    nombre_clients = stats.get("clients", 0)

except Exception as e:

    st.error(
        f"Erreur lors du chargement des statistiques : {e}"
    )

    nombre_om = 0
    nombre_camions = 0
    nombre_chauffeurs = 0
    nombre_clients = 0


# ============================================================
# INDICATEURS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )

with col2:
    st.metric(
        "🚚 Camions",
        nombre_camions
    )

with col3:
    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )

with col4:
    st.metric(
        "👥 Clients",
        nombre_clients
    )

st.divider()

# ============================================================
# CHOIX DU RAPPORT
# ============================================================

rapport = st.selectbox(
    "📊 Choisir un rapport",
    [
        "Ordres de Mission",
        "Camions",
        "Chauffeurs",
        "Clients"
    ]
)

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

if rapport == "Ordres de Mission":

    st.subheader("📋 Rapport des Ordres de Mission")

    try:
        df = get_ordres_mission()

    except Exception as e:
        st.error(
            f"Erreur lors du chargement des Ordres de Mission : {e}"
        )
        df = pd.DataFrame()


elif rapport == "Camions":

    st.subheader("🚚 Rapport des Camions")

    try:
        df = get_camions()

    except Exception as e:
        st.error(
            f"Erreur lors du chargement des camions : {e}"
        )
        df = pd.DataFrame()


elif rapport == "Chauffeurs":

    st.subheader("👷 Rapport des Chauffeurs")

    try:
        df = get_chauffeurs()

    except Exception as e:
        st.error(
            f"Erreur lors du chargement des chauffeurs : {e}"
        )
        df = pd.DataFrame()


elif rapport == "Clients":

    st.subheader("👥 Rapport des Clients")

    try:
        df = get_clients()

    except Exception as e:
        st.error(
            f"Erreur lors du chargement des clients : {e}"
        )
        df = pd.DataFrame()


# ============================================================
# RECHERCHE
# ============================================================

if not df.empty:

    recherche = st.text_input(
        "🔍 Rechercher dans le rapport"
    )

    if recherche:

        masque = (
            df.astype(str)
            .apply(
                lambda colonne: colonne.str.contains(
                    recherche,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        )

        df = df[masque]


# ============================================================
# AFFICHAGE
# ============================================================

if df.empty:

    st.info(
        "ℹ️ Aucune donnée disponible."
    )

else:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"**Nombre de lignes : {len(df)}**"
    )

    st.divider()

    # ========================================================
    # EXPORT CSV
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 Télécharger CSV",
            data=csv_data,
            file_name="rapport.csv",
            mime="text/csv"
        )

    # ========================================================
    # EXPORT EXCEL
    # ========================================================

    with col2:

        try:

            buffer = BytesIO()

            # Utilisation de pandas + openpyxl
            with pd.ExcelWriter(
                buffer,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Rapport"
                )

            buffer.seek(0)

            st.download_button(
                label="📊 Télécharger Excel",
                data=buffer.getvalue(),
                file_name="rapport.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        except Exception as e:

            st.error(
                f"Impossible de créer le fichier Excel : {e}"
            )


# ============================================================
# PIED DE PAGE
# ============================================================

st.divider()

st.caption(
    "TMF LOGISTICS — Système de Gestion du Transport — Version 2.0"
)
