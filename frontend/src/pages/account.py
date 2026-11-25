# Compte

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("account")

st.set_page_config(page_title="Mon compte")

if "user" not in st.session_state:
    st.switch_page("pages/home.py")

user = st.session_state["user"]
id_user = user["id_user"]

st.html(
    """
    <style>
        [class*="st-key-container_even_"] {background-color: #dcecf5;
        border: 2px solid #000000;}
    </style>
    """
)

st.title("Mon compte")

top_cell = st.container(
        key="container_even_1", border=True, height="stretch", vertical_alignment="center"
    )
with top_cell:
    st.write(f"Identifiant : {user['username']}")

st.subheader("Stations favorites")

mid_cell = st.container(
        key="container_even_2", border=True, height="stretch", vertical_alignment="center"
    )

with mid_cell:

    res_fav = api_client.get("/favorite/")
    favoris = res_fav["data"]["favorites"] if res_fav["status_code"] == 200 else []

    if not favoris:
        st.info("Aucune station en favoris")

    for fav in favoris:
        col1, col2 = st.columns([4, 1])
        data_latest_record = api_client.get(f"/station/{fav['id_station']}/latest")["data"]
        col1.write(
            f"{fav['name']} : nombres de vélos disponibes : {data_latest_record['nb_available_bikes']}, nombres d'emplacements libres : {data_latest_record['nb_available_spaces']}"
        )
        if col2.button("Supprimer", key=f"{fav['id_station']}"):
            api_client.delete(f"/favorite/{id_user}", json={"id_station": fav["id_station"]})
            st.rerun()

st.divider()

st.subheader("Modifier son profil")

bot_cell = st.container(
        key="container_even_3", border=True, height="stretch", vertical_alignment="center"
    )

with bot_cell:

    current_password = st.text_input("Mot de passe actuel", type="password")
    username = st.text_input("Nouvel identifiant")
    password = st.text_input("Nouveau mot de passe", type="password")

    if st.button("Modifier"):
        response = api_client.put(
            "/user/me",
            json={"current_pwd": current_password, "new_username": username, "new_pwd": password},
            headers={"X-Auth-Token": st.session_state["user"]["access_token"]},
        )
        if response["status_code"] == 200:
            st.success("Compte modifié")
        else:
            st.error(f"Erreur {response['status_code']}")

if st.button("Se déconnecter"):
    st.session_state.clear()
    st.switch_page("pages/home.py")

if st.button("Retour"):
    st.switch_page("pages/station.py")
