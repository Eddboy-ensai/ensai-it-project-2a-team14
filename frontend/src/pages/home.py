# Menu/Accueil/Menu

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("home")

if "message" in st.session_state:
    st.success(st.session_state["message"])
    del st.session_state["message"]

st.title("Veloscope")

username = st.text_input("Identifiant")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    reponse = api_client.post("/login", json={"username": username, "pwd": password})
    if reponse["status_code"] == 200:
        st.session_state["user"] = reponse["data"]
        st.session_state["access_token"] = reponse["data"]["access_token"]
        st.switch_page("pages/station.py")
    else:
        st.error(f"Erreur {reponse['status_code']} : {reponse['data']}")

if st.button("Créer un compte"):
    st.switch_page("pages/create_user.py")
