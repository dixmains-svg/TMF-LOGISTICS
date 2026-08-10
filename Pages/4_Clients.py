import streamlit as st
import pandas as pd
from io import BytesIO

from database.database import (
    get_clients,
    ajouter_client,
    supprimer_client
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("👥 Gestion des Clients")

st.caption(
    "Gestion des clients TMF LOGISTICS"
)

st.divider()


# ============================================================
# CHARGER LES CLIENTS
# ============================================================

df = get_clients()


# ============================================================
# INDICATEURS
# ============================================================

nombre_clients = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Nombre de clients",
        nombre_clients
    )

with col2:
    if not df.empty and "ville" in df.columns:
        nombre_villes = df["ville"].nunique()
    else:
        nombre_villes = 0

    st.metric(
        "📍 Villes",
        nombre_villes
    )

with col3:
    if not df.empty and "client" in df.columns:
        nombre_noms = df["client"].nunique()
    else:
        nombre_noms = 0

    st.metric(
        "🏢 Clients uniques",
        nombre_noms
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher un client",
    placeholder="Code, client, ville, téléphone, contact..."
)


if recherche and not df.empty:

    masque = (
        df.astype(str)
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

    df = df[masque]


# ============================================================
# AJOUTER UN CLIENT
# ============================================================

with st.expander("➕ Ajouter un client"):

    col1, col2 = st.columns(2)

    with col1:

        code_client = st.text_input(
            "🔢 Code client",
            placeholder="CL001"
        )

        client = st.text_input(
            "🏢 Nom du client",
            placeholder="Ex : CEVITAL"
        )

        ville = st.text_input(
            "📍 Ville",
            placeholder="Ex : Béjaïa"
        )

        adresse = st.text_input(
            "🏠 Adresse",
            placeholder="Adresse du client"
        )

    with col2:

        telephone = st.text_input(
            "📞 Téléphone",
            placeholder="0550 00 00 00"
        )

        email = st.text_input(
            "📧 Email",
            placeholder="contact@client.dz"
        )

        contact = st.text_input(
            "👤 Personne à contacter",
            placeholder="Nom du contact"
        )

    if st.button(
        "💾 Ajouter le client",
        type="primary"
    ):

        if not client.strip():

            st.error(
                "⚠️ Veuillez saisir le nom du client."
            )

        else:

            try:

                ajouter_client(
                    code_client=code_client,
                    client=client,
                    ville=ville,
                    adresse=adresse,
                    telephone=telephone,
                    email=email,
                    contact=contact
                )

                st.success(
                    f"✅ Le client {client} a été ajouté."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Erreur : {e}"
                )


# ============================================================
# LISTE DES CLIENTS
# ============================================================

st.subheader("👥 Liste des clients")


if df.empty:

    st.info(
        "Aucun client enregistré dans la base de données."
    )

else:

    df_affichage = df.copy()

    # Renommer les colonnes
    renommage = {
        "id": "ID",
        "code_client": "Code Client",
        "client": "Client",
        "ville": "Ville",
        "adresse": "Adresse",
        "telephone": "Téléphone",
        "email": "Email",
        "contact": "Contact",
        "created_at": "Date création"
    }

    df_affichage.rename(
        columns=renommage,
        inplace=True
    )

    # Ajouter une numérotation
    df_affichage.insert(
        0,
        "N°",
        range(1, len(df_affichage) + 1)
    )

    st.dataframe(
        df_affichage,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT
# ============================================================

st.divider()

if not df.empty:

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # EXPORT EXCEL
    # --------------------------------------------------------

    with col1:

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            df_affichage.to_excel(
                writer,
                index=False,
                sheet_name="Clients"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="clients.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

    # --------------------------------------------------------
    # EXPORT CSV
    # --------------------------------------------------------

    with col2:

        csv = df_affichage.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Exporter en CSV",
            data=csv,
            file_name="clients.csv",
            mime="text/csv"
        )