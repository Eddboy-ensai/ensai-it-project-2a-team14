# page des stations

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("home")

col1, col2 = st.columns([6, 1])
col1.title("Veloscope")
if col2.button("Compte"):
    st.switch_page("pages/compte.py")

# chercher = st.text_input("Chercher une station")

stations = api_client.get("/station/")

# st.write("Type de response :", type(response))
# st.write("Réponse :", response)

# if response["status_code"] != 200:
#    st.error("Error loading players")
#    st.stop()

df_stations = pd.DataFrame(api_client.get("/station/")["data"])
df_stations["url"] = "/station/" + df_stations["id_station"].astype(str)
st.dataframe(
    df_stations,
    hide_index=True,
    column_config={"url": st.column_config.LinkColumn(label="Informations", display_text="📊")},
)
# dataframe = stations.loc[:, ["name"]]
# dataframe["url"] = "pouet"
# st.dataframe(
#   dataframe,
#   hide_index=True,
#   column_config={"name": st.column_config.LinkColumn(label="Nom", display_text="name")},
# )

# df["url"] = "/player_stats?id_player=" + df["id_player"].astype(str)
# st.dataframe(df, hide_index=True, column_config={"url": st.column_config.LinkColumn(label="Stats", display_text="📊")})
# if chercher:
#    stations = stations[stations["name"].str.contains(chercher, case=False)]

# st.map(stations, latitude="lat", longitude="lon")

# for _, station in stations.iterrows():
#    c1, c2, c3 = st.columns([4, 1, 1])
#    c1.write(station["name"])
#    c2.write(station["capacity"])
#    if c3.button("Ouvrir", key=int(station["id_station"])):
#        st.session_state["id_station"] = int(station["id_station"])
#        st.switch_page("pages/page_station.py")
