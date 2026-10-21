# créer un user
import streamlit as st
from utils.api_client import api_client

st.title("Créer un compte")

username = st.text_input("Identifiant")
password = st.text_input("Mot de passe", type="password")

if st.button("Créer"):
    reponse = api_client.post("/user/", json={"username": username, "pwd": password})
    if reponse["status_code"] == 200:
        st.success("Compte créé")
    else:
        st.error(f"Erreur {reponse['status_code']}")

if st.button("Retour au menu"):
    st.switch_page("pages/home.py")