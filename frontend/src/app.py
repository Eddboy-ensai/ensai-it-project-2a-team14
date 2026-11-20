import streamlit as st

from utils.env_variables import display_values, load_environment_variables
from utils.log_init import initialize_logs

if "logs_initialized" not in st.session_state:
    initialize_logs("Streamlit App")
    load_environment_variables()
    display_values(include_prefix="BACKEND")
    st.session_state["logs_initialized"] = True

# if "user" in st.session_state:
#     st.switch_page("pages/station.py")
# else:
#     st.switch_page("pages/home.py")

logged_in = "user" in st.session_state

pages = [
    st.Page("pages/account.py", title="Mes informations", default=logged_in),
    st.Page("pages/admin.py", title="Administration"),
    st.Page(
        "pages/create_user.py",
        title="Créer un compte",
    ),
    st.Page("pages/home.py", title="Se connecter", default=not logged_in),
    st.Page(
        "pages/station.py",
        title="Informations sur les stations",
    ),
    st.Page(
        "pages/suggestion.py",
        title="Suggestions de stations",
    ),
]

st.navigation(pages).run()
