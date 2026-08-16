import streamlit as st

st.title("🚛 TMF LOGISTICS")

st.subheader(
    "Système de Gestion du Transport et des Ordres de Mission"
)

st.divider()

st.markdown("## 📊 Tableau de bord")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Ordres de Mission", "—")

with col2:
    st.metric("🚚 Camions", "—")

with col3:
    st.metric("👷 Chauffeurs", "—")

with col4:
    st.metric("👥 Clients", "—")

st.divider()

st.markdown(
    """
    ## Azul Felawen dans TMF LOGISTICS 👋

    Cette application permet de gérer les principales opérations
    de transport de TMF LOGISTICS.

    ### 📋 Ordres de Mission
    Gestion des missions, camions, chauffeurs, clients,
    dates et kilométrages.

    ### 🚚 Gestion du parc
    Suivi des camions, remorques, chauffeurs et affectations.

    ### 👷 Gestion des Chauffeurs
    Gestion des badges, fonctions, affectations et superviseurs.

    ### 👥 Gestion des Clients
    Gestion des clients, coordonnées, contacts et informations commerciales.
    """
)

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px;
        color:#666;
        line-height:1.6;
    ">
        <b style="font-size:18px; color:#1f4e79;">
            TMF LOGISTICS
        </b>
        <br>
        Système de Gestion du Transport
        <br>
        <span style="font-size:12px;">
            Version 1.0 — By H.Redjdal
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
