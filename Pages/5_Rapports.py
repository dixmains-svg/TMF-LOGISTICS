import streamlit as st
import pandas as pd
from io import BytesIO

from database.database import (
    get_ordres_mission,
    get_camions,
    get_chauffeurs,
    get_clients
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("📊 Rapports & Statistiques")

st.caption(
    "Tableau de suivi et analyse de l'activité TMF LOGISTICS"
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = get_ordres_mission()
df_camions = get_camions()
df_chauffeurs = get_chauffeurs()
df_clients = get_clients()


# ============================================================
# INDICATEURS PRINCIPAUX
# ============================================================

nombre_om = len(df_om)
nombre_camions = len(df_camions)
nombre_chauffeurs = len(df_chauffeurs)
nombre_clients = len(df_clients)


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
# RAPPORT DES STATUTS
# ============================================================

st.subheader("📌 État des Ordres de Mission")

if not df_om.empty and "statut" in df_om.columns:

    statuts = (
        df_om["statut"]
        .fillna("Non renseigné")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    statuts.columns = [
        "Statut",
        "Nombre"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.dataframe(
            statuts,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        st.bar_chart(
            statuts.set_index("Statut")
        )

else:

    st.info(
        "Aucun Ordre de Mission disponible."
    )


st.divider()


# ============================================================
# OM PAR CLIENT
# ============================================================

st.subheader("👥 Ordres de Mission par Client")

if not df_om.empty and "client" in df_om.columns:

    om_client = (
        df_om["client"]
        .fillna("Non renseigné")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    om_client.columns = [
        "Client",
        "Nombre OM"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.dataframe(
            om_client,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        st.bar_chart(
            om_client.set_index("Client")
        )

else:

    st.info(
        "Aucune donnée client disponible."
    )


st.divider()


# ============================================================
# OM PAR CAMION
# ============================================================

st.subheader("🚚 Ordres de Mission par Camion")

if not df_om.empty and "camion" in df_om.columns:

    om_camion = (
        df_om["camion"]
        .fillna("Non renseigné")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    om_camion.columns = [
        "Camion",
        "Nombre OM"
    ]

    st.dataframe(
        om_camion,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Aucune donnée camion disponible."
    )


st.divider()


# ============================================================
# OM PAR CHAUFFEUR
# ============================================================

st.subheader("👷 Ordres de Mission par Chauffeur")

if not df_om.empty and "chauffeur" in df_om.columns:

    om_chauffeur = (
        df_om["chauffeur"]
        .fillna("Non renseigné")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    om_chauffeur.columns = [
        "Chauffeur",
        "Nombre OM"
    ]

    st.dataframe(
        om_chauffeur,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Aucune donnée chauffeur disponible."
    )


st.divider()


# ============================================================
# KILOMÉTRAGE
# ============================================================

st.subheader("🛣️ Kilométrage")

if not df_om.empty and "km_parcourus" in df_om.columns:

    km = pd.to_numeric(
        df_om["km_parcourus"],
        errors="coerce"
    ).fillna(0)

    total_km = km.sum()

    moyenne_km = km.mean() if len(km) > 0 else 0

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🛣️ Kilométrage total",
            f"{total_km:,.0f} km"
        )

    with col2:

        st.metric(
            "📏 Moyenne par OM",
            f"{moyenne_km:,.0f} km"
        )

else:

    st.info(
        "Aucune donnée de kilométrage disponible."
    )


st.divider()


# ============================================================
# TABLEAU RÉCAPITULATIF
# ============================================================

st.subheader("📋 Synthèse de l'activité")

synthese = pd.DataFrame({
    "Indicateur": [
        "Ordres de Mission",
        "Camions",
        "Chauffeurs",
        "Clients"
    ],

    "Nombre": [
        nombre_om,
        nombre_camions,
        nombre_chauffeurs,
        nombre_clients
    ]
})

st.dataframe(
    synthese,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXPORT DU RAPPORT
# ============================================================

st.divider()

st.subheader("📥 Exporter le rapport")


buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    # Feuille synthèse
    synthese.to_excel(
        writer,
        index=False,
        sheet_name="Synthèse"
    )

    # Feuille OM
    if not df_om.empty:

        df_om.to_excel(
            writer,
            index=False,
            sheet_name="Ordres de Mission"
        )

    # OM par client
    if not df_om.empty and "client" in df_om.columns:

        om_client.to_excel(
            writer,
            index=False,
            sheet_name="OM par Client"
        )

    # OM par camion
    if not df_om.empty and "camion" in df_om.columns:

        om_camion.to_excel(
            writer,
            index=False,
            sheet_name="OM par Camion"
        )

    # OM par chauffeur
    if not df_om.empty and "chauffeur" in df_om.columns:

        om_chauffeur.to_excel(
            writer,
            index=False,
            sheet_name="OM par Chauffeur"
        )

    # Statuts
    if not df_om.empty and "statut" in df_om.columns:

        statuts.to_excel(
            writer,
            index=False,
            sheet_name="OM par Statut"
        )


buffer.seek(0)


st.download_button(
    label="📥 Télécharger le rapport Excel",
    data=buffer,
    file_name="rapport_tmf_logistics.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)