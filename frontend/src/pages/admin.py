# Page des administrateurs

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

id_user = st.query_params.get("id_user")

if "user" not in st.session_state:
    st.session_state["message"] = "Veuillez vous connecter pour accéder à cette page"
    st.switch_page("pages/home.py")

logger = get_page_logger("admin")

if not st.session_state["user"]["admin"]:
    st.session_state["message"] = "Page réservée aux administrateurs"
    st.switch_page("pages/home.py")

result = api_client.get("/user/")
if result["status_code"] == 200:
    users = result["data"]
usernames = [user["username"] for user in users]
selected_username = st.selectbox(
    "Choisir un utilisateur à modifier",
    usernames,
    index=None,
    placeholder="Choisir votre utilisateur",
)
if selected_username:
    for user in users:
        if user["username"] == selected_username:
            id_user_selected = str(user["id_user"])
            break
    if id_user != id_user_selected:
        st.query_params["id_user"] = id_user_selected
        st.rerun()

if id_user:
    username = st.text_input("Nouvel identifiant")
    password = st.text_input("Nouveau mot de passe", type="password")
    if st.button("Modifier"):
        reponse = api_client.post("/user/", json={"username": username, "pwd": password})
        if reponse["status_code"] == 200:
            st.success("Compte créé")
        else:
            st.error(f"Erreur {reponse['status_code']}")
