"""
Streamlit page for user account registration.

Allows users to create a new user profile with username, password, Elo, email, etc.

Endpoint used:
    POST /player
"""

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Create a user account")
logger = get_page_logger("create_user")

username = st.text_input("Username", max_chars=30)
password = st.text_input("Password", type="password")

is_pwd_long_enough = len(password) >= 5
st.write("✅" if is_pwd_long_enough else "❌", "At least 5 characters")

with st.container(horizontal_alignment="center"):
    if st.button("Create", width=150, disabled=not username or not is_pwd_long_enough):
        logger.info("Create a user")
        user = {
            "username": username,
            "pwd": password,
        }

        response = api_client.post("/user/", json=user)

        if response:
            if response["status_code"] == 200:
                st.success(f"User {username} successfully created! 🎉")
                logger.info("User created successfully")
            else:
                st.error(f"Error: {response['data']}")
                logger.info("Error while creating user")

if st.button("Back to homepage", type="primary"):
    st.switch_page("pages/home.py")
