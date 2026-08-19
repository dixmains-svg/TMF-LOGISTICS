import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# EXEMPLE DE CALCULS DES TAUX D'EXPLOITATION ET TRANSPORT
# ============================================================

def calculer_taux_transport(df_om: pd.DataFrame, df_commandes: pd.DataFrame, flotte_totale: int = 20):
    """
    Calcule les différents taux métiers pour le transport
    """
    
    # 1. Taux d'Exploitation
    camions_utilises = df_om["Numero Camion"].replace(["", "nan"], pd.NA).dropna().nunique() if "Numero Camion" in df_om.columns else 0
    taux_exploitation = (camions_utilises / flotte_totale * 100) if flotte_totale > 0 else 0
    
    # 2. Taux de Remplissage (si les colonnes Tonnage et Capacité sont présentables)
    if "Tonnage" in df_commandes.columns and "Capacité Maximale" in df_commandes.columns:
        tonnage_reel = df_commandes["Tonnage"].sum()
        capacite_totale = df_commandes["Capacité Maximale"].sum()
        taux_remplissage = (tonnage_reel / capacite_totale * 100) if capacite_totale > 0 else 0
    else:
        taux_remplissage = None

    # 3. Rendement par Camion
    ca_total = df_commandes["Montant ligne HT"].sum() if "Montant ligne HT" in df_commandes.columns else 0
    ca_par_camion = (ca_total / camions_utilises) if camions_utilises > 0 else 0

    return {
        "Flotte Totale": flotte_totale,
        "Camions Exploités": camions_utilises,
        "Taux d'Exploitation (%)": round(taux_exploitation, 2),
        "CA Total HT (DA)": round(ca_total, 2),
        "CA Moyen / Camion (DA)": round(ca_par_camion, 2),
        "Taux de Remplissage (%)": round(taux_remplissage, 2) if taux_remplissage is not None else "N/A"
    }

# ============================================================
# AFFICHAGE STREAMLIT DE LA TABLE DES TAUX
# ============================================================

st.subheader("📊 Tableau des Taux d'Exploitation et Indicateurs de Performance (KPI)")

# Saisie de la flotte totale dans la sidebar
flotte_saisie = st.sidebar.number_input("🚛 Nombre total de camions dans le parc", min_value=1, value=25)

# Calcul
kpis = calculer_taux_transport(df_analyse, df_croise, flotte_totale=flotte_saisie)

# Affichage sous forme de cartes KPI
c1, c2, c3, c4 = st.columns(4)
c1.metric("🚛 Flotte Totale", f"{kpis['Flotte Totale']} véhicules")
c2.metric("🚚 Camions Exploités", f"{kpis['Camions Exploités']} véhicules")
c3.metric("📈 Taux d'Exploitation", f"{kpis['Taux d\'Exploitation (%)']} %")
c4.metric("💰 CA Moyen / Camion", f"{kpis['CA Moyen / Camion (DA)']:,.2f} DA")

# ============================================================
# TABLEAU DÉTAILLÉ DU TAUX D'EXPLOITATION PAR CAMION / SECTION
# ============================================================

st.markdown("### 📋 Tableau détaillé par Véhicule")

if "Numero Camion" in df_analyse.columns:
    # Agrégation par camion
    df_camion_kpi = df_analyse.groupby("Numero Camion").agg(
        Missions_Effectuees=("Ordre de Mission", "nunique"),
    ).reset_index()

    # Rapprochement du CA par camion si disponible
    if not df_croise.empty and "Numero Camion" in df_croise.columns and "Montant ligne HT" in df_croise.columns:
        df_ca_cam = df_croise.groupby("Numero Camion")["Montant ligne HT"].sum().reset_index()
        df_camion_kpi = pd.merge(df_camion_kpi, df_ca_cam, on="Numero Camion", how="left").fillna(0)
        df_camion_kpi.rename(columns={"Montant ligne HT": "CA Généré (HT)"}, inplace=True)

    # Calcul du taux d'activité relatif (part par rapport à l'ensemble des missions)
    total_missions = df_camion_kpi["Missions_Effectuees"].sum()
    df_camion_kpi["Part de l'Activité (%)"] = (df_camion_kpi["Missions_Effectuees"] / total_missions * 100).round(2)

    st.dataframe(
        df_camion_kpi.sort_values(by="Missions_Effectuees", ascending=False),
        use_container_width=True,
        hide_index=True
    )
