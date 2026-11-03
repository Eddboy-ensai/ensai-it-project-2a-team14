# Compte

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("account")

if "user" not in st.session_state:
    st.switch_page("pages/home.py")

user = st.session_state["user"]
user_id = user["id_user"]

st.title("Mon compte")
st.write(f"Identifiant : {user['username']}")

st.subheader("Stations favorites")

reponse_favs = api_client.get(f"/favorite/{user_id}")
favoris = reponse_favs.get("data", [])

if not favoris:
    st.info("Aucune station en favoris")
else:
    for fav in favoris:
        col1, col2 = st.columns([4, 1])
        col1.write(fav.get("name", f"Station {fav['id_station']}"))
    if col2.button("Supprimer", key=f"del_{fav['id_station']}"):
        reponse = api_client.delete(
            f"/favorite/{user_id}",
            json={"id_station": fav["id_station"]},
        )
        st.rerun()

st.divider()

if st.button("Se déconnecter"):
    st.session_state.clear()
    st.switch_page("pages/home.py")

if st.button("Retour"):
    st.switch_page("pages/station.py")
