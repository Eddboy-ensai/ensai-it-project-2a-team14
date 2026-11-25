# Page des stations

import os

import pandas as pd
import requests
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

logger = get_page_logger("station")

st.set_page_config(page_title="Informations sur les stations", layout="wide")

check_authentification()

id_station = st.query_params.get("id_station")

# Couleur des containers
st.html(
    """
    <style>
        [class*="st-key-container_even_"] {background-color: #dcecf5;
        border: 2px solid #000000;}

        [class*="st-key-container_odd_"] {background-color: #c5d9e3;
        border: 2px solid #000000;}
    </style>
    """
)

if id_station:  # display of the page with a query "id_station"
    API_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
    if st.query_params.get("selected_range"):
        range = int(st.query_params.get("selected_range"))
    else:
        range = 7
    station = requests.get(f"{API_URL}/station/{id_station}", params={"range": range}).json()
    st.title(f"Informations concernant la station {station['name']}")

    st.subheader("Informations en direct")

    top_cell = st.container(
        key="container_even_1", border=True, height="stretch", vertical_alignment="center"
    )
    # status of the station
    with top_cell:
        if station["status"] == "IN_SERVICE":
            st.write("Statut actuel de la station : en service")
        else:
            st.write("Statut actuel de la station : hors service")
        st.write(f"Score de fiabilité de la station : {station['score']} / 100")
        # Current availability : we get the latest record of the station in 'availability_bikes/spaces' which is a list of dict
        st.write(
            f"Nombre de vélos actuellement disponibles : {list(station['availability_bikes'][-1].values())[0]}"
        )
        st.write(
            f"Nombre d'emplacements actuellement disponibles : {list(station['availability_spaces'][-1].values())[0]}"
        )
        st.write(f"Taux de remplissage de la station : {round(station['fill_rate'] * 100)}%")
        st.write(
            f"Nombre de vélos disponibles estimé dans une heure : {station['prediction_bikes']}"
        )
        st.write(
            f"Nombre d'emplacements disponibles estimé dans une heure : {station['prediction_spaces']}"
        )

    st.subheader("Evolutions temporelles des disponibilités")

    mid_cell = st.container(
        key="container_even_2", border=True, height="stretch", vertical_alignment="center"
    )
    with mid_cell:
        range = None
        selected_range = st.selectbox(
            "Veuillez choisir une période",
            ["1 jour", "7 jours", "30 jours"],
            index=None,
            placeholder="Choisir une période",
        )
        if selected_range:
            if selected_range == "1 jour":
                range = "1"
            elif selected_range == "7 jours":
                range = "7"
            else:
                range = "30"
            if st.query_params.get("selected_range") != range:
                st.query_params["selected_range"] = range
                st.rerun()

        top_mid_cell = st.container(
            key="container_odd_1", border=True, height="stretch", vertical_alignment="center"
        )
        with top_mid_cell:
            st.write(
                "Evolution temporelle du nombre d'emplacements libres disponibles dans la station"
            )

            spaces = [
                {"date": date, "places disponibles": nb}
                for element in station.get("availability_spaces")
                for date, nb in element.items()
            ]

            if spaces:
                df = pd.DataFrame(spaces)
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date")
                st.line_chart(df, x="date", y="places disponibles")
            else:
                st.info("Pas d'informations disponible")

        bot_mid_cell = st.container(
            key="container_odd_2", border=True, height="stretch", vertical_alignment="center"
        )
        with bot_mid_cell:
            st.write("Evolution temporelle du nombre de vélos disponibles dans la station")
            bikes = [
                {"date": date, "vélos disponibles": nb}
                for element in station.get("availability_bikes")
                for date, nb in element.items()
            ]

            if bikes:
                df = pd.DataFrame(bikes)
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date")
                st.line_chart(df, x="date", y="vélos disponibles")
            else:
                st.info("Pas d'informations disponible")

        if st.button("Retour"):
            st.query_params.clear()
            st.rerun()

else:  # display the page without query
    col1, col2 = st.columns([6, 1])
    col1.title("Veloscope")

    if "message_fav" in st.session_state:
        st.success(st.session_state["message_fav"])
        del st.session_state["message_fav"]

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

    user_id = st.session_state["user"]["id_user"]

    # dataframe for the map
    df_stations = pd.DataFrame(stations)

    df_stations["lat"] = pd.to_numeric(df_stations["lat"])
    df_stations["lon"] = pd.to_numeric(df_stations["lon"])

    # information about favorites
    favoris_ids = []
    res_fav = api_client.get("/favorite")

    if res_fav["status_code"] == 200:
        favoris_ids = [fav["id_station"] for fav in res_fav["data"]["favorites"]]

    df_stations["Favorite"] = df_stations["id_station"].isin(favoris_ids)

    col_carte, col_tableau = st.columns(2)

    with col_carte:
        st.subheader("Carte des stations")

        left_cell = st.container(
        key="container_even_3", border=True, height="stretch", vertical_alignment="center"
    )
        with left_cell:

            liste_noms = ["Toutes les stations"] + df_stations["name"].tolist()
            station_recherchee = st.selectbox("Trouver une station :", liste_noms)

            if station_recherchee == "Toutes les stations":
                df_stations["marker_color"] = "#1f77b4"
            else:
                df_stations["marker_color"] = df_stations["name"].apply(
                    lambda x: "#ff4b4b" if x == station_recherchee else "#1f77b4"
                )

            st.map(
                df_stations,
                latitude="lat",
                longitude="lon",
                size="capacity",
                color="marker_color",
            )

    with col_tableau:
        st.subheader("Informations sur les stations")

        right_cell = st.container(
        key="container_even_4", border=True, height="stretch", vertical_alignment="center"
    )
        with right_cell:

            stations_names = [station["name"] for station in stations]
            selected_station = st.selectbox(
                "Choisissez une station pour plus d'informations",
                stations_names,
                index=None,
                placeholder="Choisir votre station",
            )
            if selected_station:
                for station in stations:
                    if station["name"] == selected_station:
                        id_station_selected = str(station["id_station"])
                        break
                if id_station != id_station_selected:
                    st.query_params["id_station"] = id_station_selected
                    st.rerun()

            edited_df = st.data_editor(
                df_stations,
                hide_index=True,
                column_order=["name", "Favorite"],
                column_config={
                    "name": "Nom",
                    "capacity": "Capacité",
                    "Favorite": st.column_config.CheckboxColumn(
                        "Favori", help="Cocher pour ajouter à vos favoris", default=False
                    ),
                },
                disabled=["id_station", "name", "lat", "lon", "capacity"],
                key="station_editor",
            )

            if st.button("Enregister mes favoris"):
                nouvelles_favorites = edited_df[edited_df["Favorite"]]["id_station"].tolist()

                to_add = set(nouvelles_favorites) - set(favoris_ids)
                to_delete = set(favoris_ids) - set(nouvelles_favorites)

                for s_id in to_add:
                    api_client.post("/favorite/", json={"id_user": user_id, "id_station": s_id})

                for s_id in to_delete:
                    api_client.delete(f"/favorite/{user_id}", json={"id_station": s_id})

                st.session_state["message_fav"] = "Votre liste de favoris a bien été mise à jour"
                st.rerun()
