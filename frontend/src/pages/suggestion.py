# Page des stations


import pandas as pd
import pydeck as pdk
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.set_page_config(layout="wide")

logger = get_page_logger("station")

st.set_page_config(page_title="Suggestions de stations")

check_authentification()

st.html(
    """
    <style>
        [class*="st-key-container_even_"] {background-color: #dcecf5;
        border: 2px solid #000000;}
    </style>
    """
)

col1, col2 = st.columns([6, 1])
col1.title("Suggestion de stations")

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

user_id = st.session_state["user"]["id_user"]

# infos de la carte
df_stations = pd.DataFrame(stations)

df_stations["lat"] = pd.to_numeric(df_stations["lat"])
df_stations["lon"] = pd.to_numeric(df_stations["lon"])


st.subheader("1 - Que souhaitez-vous faire ?")

top_cell = st.container(
        key="container_even_1", border=True, height="stretch", vertical_alignment="center"
    )
with top_cell:
    choice = st.segmented_control(
        label="Choisissez l'option adéquate",
        options=["Prendre un vélo", "Déposer un vélo"],
        default="Prendre un vélo",
        selection_mode="single",
    )

st.subheader("2 - Choix de la station d'intérêt :")

text_cell = st.container(
        key="container_even_2", border=True, height="stretch", vertical_alignment="center"
    )

with text_cell:
    st.write(
    "Cliquez sur la carte sur la station qui vous intéresse. Si seule la station demandée apparait, c'est qu'elle est disponible. Sinon, une liste de station vous sera recommandé pour répondre à votre besoin."
)

mid_cell = st.container(
        key="container_even_3", border=True, height="stretch", vertical_alignment="center"
    )

with mid_cell:
    layer = pdk.Layer(
        "ScatterplotLayer",
        id="stations",
        data=df_stations,
        get_position="[lon, lat]",
        get_radius="capacity * 3",
        get_fill_color="marker_color",
        get_line_color=[255, 255, 255],
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=df_stations["lat"].mean(),
        longitude=df_stations["lon"].mean(),
        zoom=12,
        pitch=0,
    )

    tooltip = {
        "html": """
        <b>{name}</b><br/>
        Capacité : {capacity}<br/>
        """,
        "style": {"backgroundColor": "#222", "color": "white"},
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="light",
    )

    event = st.pydeck_chart(
        deck,
        on_select="rerun",
        selection_mode="single-object",
    )

if event.selection and event.selection["objects"].get("stations"):

    st.subheader("3 - Recommandation de station(s) :")

    bot_cell = st.container(
        key="container_even_4", border=True, height="stretch", vertical_alignment="center"
    )
    with bot_cell:
        station = event.selection["objects"]["stations"][0]
        id_station = station["id_station"]
        choice_bool = choice == "Prendre un vélo"
        response = api_client.get(
            f"/station/suggestions/{id_station}", params={"choice_bool": choice_bool}
        )
        if response["status_code"] == 200:
            col = []
            for station in response["data"]:
                latest_record = api_client.get(
                    f"/station/{station['station']['id_station']}/latest"
                )
                col.append({
                    "Station": station["station"]["name"],
                    "Score de fiabilité": station["score"],
                    "Vélos dispo": latest_record["data"]["nb_available_bikes"],
                    "Emplacements libres": latest_record["data"]["nb_available_spaces"],
                })

            st.dataframe(pd.DataFrame(col), hide_index=True)
        else:
            st.error(f"Erreur {response['status_code']} : {response['data']}")

if st.button("Retour"):
    st.switch_page("pages/station.py")