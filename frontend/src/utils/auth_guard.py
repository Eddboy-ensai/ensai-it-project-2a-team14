import logging
import time

import streamlit as st


def check_authentification():
    """Checks if the user is authenticated.

    If the user is not logged, he is redirected to the home page.
    """
    if not st.session_state.get("access_token"):
        logging.info("Not logged in, return to the home page")
        st.error("Vous devez être connecté pour accéder à cette page. Retour à la page principale")
        time.sleep(3)
        st.switch_page("pages/home.py")


def check_admin():
    """Checks if the user is an administrator.

    If the user is an administrator, he is redirected to the home page.
    """
    if not st.session_state["user"]["admin"]:
        logging.info("Not logged in, return to the home page")
        st.error(
            "Vous devez être administrateur pour accéder à cette page. Retour à la page principale"
        )
        time.sleep(3)
        st.switch_page("pages/home.py")
