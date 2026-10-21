#page_station 

import pandas as pd
import streamlit as st
from utils.api_client import api_client

id_station = st.session_state["id_station"]
station = api_client.get(f"/station/{id_station}")["data"]
stats = api_client.get(f"/station/{id_station}/stats")["data"]

col1, col2 = st.columns([6, 1])
col1.title(station["name"])
if col2.button("Retour"):
    st.switch_page("pages/menu.py")

if st.button("Ajouter aux favoris"):
    user = st.session_state["user"]
    reponse = api_client.post("/favorite/", json={"id_user": user["id_user"], "id_station": id_station})
    if reponse["status_code"] == 200:
        st.success("Ajouté")
        
st.map(pd.DataFrame({"lat": [station["lat"]], "lon": [station["lon"]]}), zoom=15)

#a finir