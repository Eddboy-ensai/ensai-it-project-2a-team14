# page des stations

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("home")

col1, col2 = st.columns([6, 1])
col1.title("Veloscope")
if col2.button("Compte"):
    st.switch_page("pages/compte.py")

stations = api_client.get("/station/")

df_stations = pd.DataFrame(api_client.get("/station/")["data"])
df_stations["url"] = "/station/" + df_stations["id_station"].astype(str)
df_screen = df_stations.loc[:, ["name", "url"]]
st.dataframe(
    df_screen,
    hide_index=True,
    column_config={"url": st.column_config.LinkColumn(label="Informations", display_text="📊")},
)
