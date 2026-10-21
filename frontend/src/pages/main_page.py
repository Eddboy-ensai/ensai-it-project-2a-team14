#page_principal

import pandas as pd
import streamlit as st
from utils.api_client import api_client

col1, col2 = st.columns([6, 1])
col1.title("Veloscope")
if col2.button("Compte"):
    st.switch_page("pages/compte.py")

chercher = st.text_input("Chercher une station")

stations = pd.DataFrame(api_client.get("/station/")["data"])
if chercher:
    stations = stations[stations["name"].str.contains(chercher, case=False)]

st.map(stations, latitude="lat", longitude="lon")

for _, station in stations.iterrows():
    c1, c2, c3 = st.columns([4, 1, 1])
    c1.write(station["name"])
    c2.write(station["capacity"])
    if c3.button("Ouvrir", key=int(station["id_station"])):
        st.session_state["id_station"] = int(station["id_station"])
        st.switch_page("pages/page_station.py")
