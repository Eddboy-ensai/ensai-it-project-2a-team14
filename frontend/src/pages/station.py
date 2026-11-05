# Page des stations

import os

import pandas as pd
import requests
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

logger = get_page_logger("station")

check_authentification()

id_station = st.query_params.get("id_station")

if id_station:  # si on a précisé une id_station en query, par ex adresse station?id_station=5501
    API_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
    station = requests.get(f"{API_URL}/station/{id_station}").json()
    st.json(station)
    if st.button("Retour"):
        st.query_params.clear()
        st.rerun()

else:  # affichage de la page sans query
    col1, col2 = st.columns([6, 1])
    col1.title("Veloscope")

    if "message_fav" in st.session_state:
        st.success(st.session_state.pop("message_fav"))

    if col2.button("Compte"):
        st.switch_page("pages/account.py")

    res = api_client.get("/station/")

    if res["status_code"] != 200:
        st.error(f"Erreur {res['status_code']} : {res['data']}")
        st.stop()
    stations = res["data"]

    if not stations:
        st.info("Aucune information à afficher")
        st.stop()

    df_stations = pd.DataFrame(stations)

    user_id = st.session_state["user"]["id_user"]

    favoris_ids = []
    res_user = api_client.get(f"/user/{user_id}")
    st.write(res_user)
    res_favorites = api_client.get("/favorite")
    st.write(res_favorites)
    # if res_user["status_code"] == 200:
    #     favoris_ids = [fav["id_station"] for fav in res_user["data"]["favorites"]]

    # df_stations["Favorite"] = df_stations["id_station"].isin(favoris_ids)

    # edited_df = st.data_editor(
    #     df_stations,
    #     hide_index=True,
    #     column_config={
    #         "Favorite": st.column_config.CheckboxColumn(
    #             "Favori", help="Cocher pour ajouter à vos favoris", default=False
    #         )
    #     },
    #     disabled=["id_station", "name", "lat", "lon", "capacity"],
    #     key="station_editor",
    # )

    # if st.button("Enregister mes favoris"):
    #     nouvelles_favorites = edited_df[edited_df["Favorite"]]["id_station"].tolist()

    #     to_add = set(nouvelles_favorites) - set(favoris_ids)
    #     to_delete = set(favoris_ids) - set(nouvelles_favorites)

    #     for s_id in to_add:
    #         api_client.post("/favorite/", json={"id_user": user_id, "id_station": int(s_id)})

    #     for s_id in to_delete:
    #         api_client.delete(f"/favorite/{user_id}", json={"id_station": int(s_id)})

    #     st.session_state["message_fav"] = "Votre liste de favoris a bien été mise à jour"
    #     st.rerun()
