# Page des stations

import os

import pandas as pd
import requests
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

if "user" not in st.session_state:
    st.session_state["message"] = "Veuillez vous connecter pour accéder aux stations"
    st.switch_page("pages/home.py")

logger = get_page_logger("station")

id_station = st.query_params.get("id_station")

if id_station:  # si on a précisé une id_station en query, par ex adresse station?id_station=5501
    API_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
    station = requests.get(f"{API_URL}/station/{id_station}").json()
    st.json(station)

else:  # affichage de la page sans query
    col1, col2 = st.columns([6, 1])
    col1.title("Veloscope")
    if col2.button("Compte"):
        st.switch_page("pages/account.py")

    stations = api_client.get("/station/")["data"]
    df_stations = pd.DataFrame(stations)

    user_id = st.session_state["user"]["id_ser"]

    favoris_ids = []
    reponse_favs = api_client.get(f"/favorite/{user_id}")
    if "data" in reponse_favs:
        favoris_ids = [fav["id_station"] for fav in reponse_favs["data"]]

    df_stations["Favorite"] = df_stations["id_station"].isin(favoris_ids)

    edited_df = st.data_editor(
        df_stations,
        hide_index=True,
        column_config={
            "Favorite": st.column_config.CheckboxColumn(
                "Favori",
                help="Cocher pour ajouter à vos favoris",
                default=False
            )
        },
        disabled=["id_station", "name", "lat", "lon", "capacity"],
        key="station_editor",
    )

    if st.button("Enregister mes favoris"):
        nouvelles_favorites = edited_df[edited_df["Favorite"]]["id_station"].tolist()

        a_ajouter = set(nouvelles_favorites) - set(favoris_ids)
        a_supprimer = set(favoris_ids) - set(nouvelles_favorites)

        for s_id in a_ajouter:
            api_client.post(f"/favorite/{user_id}", json={"id_station": int(s_id)})

        for s_id in a_supprimer:
            api_client.delete(f"/favorite/{user_id}", json={"id_station": int(s_id)})

        st.success("Favoris mis à jour !")
        st.rerun()
