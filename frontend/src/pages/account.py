#compte
import streamlit as st

st.title("Mon compte")

user = st.session_state["user"]
st.write(f"Identifiant : {user['username']}")

st.subheader("Stations favorites")
favoris = []
for nom in favoris:
    col1, col2 = st.columns([4, 1])
    col1.write(nom)
    if col2.button("Supprimer", key=favoris["id_station"]):
        reponse = api_client.delete(f"/favorite/{user['id_user']}", json={"id_station": fav["id_station"]})
        if reponse["status_code"] == 200:
            st.success("Supprimé")
            st.rerun()
        else:
            st.error(f"Erreur {reponse['status_code']}")

if st.button("Se déconnecter"):
    st.session_state.clear()
    st.switch_page("pages/menu.py")