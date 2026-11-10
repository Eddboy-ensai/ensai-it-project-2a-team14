# Page des stations


import pandas as pd
import pydeck as pdk
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.set_page_config(layout="wide")

logger = get_page_logger("station")

check_authentification()

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


col_choice, col_map = st.columns(2)
with col_choice:
    choice = st.segmented_control(
        "Que souhaitez-vous faire ?",
        options=["Prendre un vélo", "Déposer un vélo"],
        default="Prendre un vélo",
        selection_mode="single",
    )

with col_map:
    st.subheader("Cliquez sur la station à laquelle vous souhaitez accéder")

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
        station = event.selection["objects"]["stations"][0]
        id_station = station["id_station"]
        choice_bool = choice == "Prendre un vélo"
        response = api_client.get(
            f"/station/suggestions/{id_station}", params={"choice_bool": choice_bool}
        )
        if response["status_code"] == 200:
            col = []
            for station in response["data"]:
                col.append(
                {"Station": station["station"]["name"], "Capacité": station["station"]["capacity"], "Score": station["score"]})
            st.dataframe(pd.DataFrame(col), hide_index=True)
        else:
            st.error(f"Erreur {response['status_code']} : {response['data']}")
