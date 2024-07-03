import streamlit as st
st.set_page_config(
    page_title="OddAI",
    page_icon="👋",
)
# st.session_state.PORT_NUMBER = 3311

from dep import *
st.write('# Sign in to access your files')
new_user = st.checkbox("Create Account", value=False)
# print(new_user)

if 'user' not in st.session_state:
    st.session_state['user'] = 'Guest'

user = st.text_input("Username", "")
pwd = st.text_input("Password", "")
# print(username)
# print(st.session_state.Username + "Current username")
st.session_state.user = "Guest"

success = add_user(user, pwd, new_user)
if success:
    st.session_state.user = success
