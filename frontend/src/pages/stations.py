# page des stations

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("home")

col1, col2 = st.columns([6, 1])
col1.title("Veloscope")
if col2.button("Compte"):
    st.switch_page("pages/compte.py")

# chercher = st.text_input("Chercher une station")

response = api_client.get("/stations/")

st.write("Type de response :", type(response))
st.write("Réponse :", response)

if response["status_code"] != 200:
    st.error("Error loading players")
    st.stop()

stations = api_client.get("/stations/")["data"]
st.write(stations)
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
