import streamlit as st
# to deploy - https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe
st.set_page_config(
    page_title="OddAI",
    page_icon="🦪",
)
from dep import *

st.title('Welcome to OddAI: Oyster Development Detection Artificial Intelligence :oyster:')
st.subheader('Uses a YOLOv10 Backend with support for live detection, video, and image annotation')


st.session_state.user = GUEST # default is guest
show_specific_pages(st.session_state.user == PUBLIC_USER)


new_user = st.checkbox("Create Account", value=False)

user = st.text_input("Username", "",  max_chars=USERNAME_PWD_SIZE_LIMIT)
pwd = st.text_input("Password", "",  max_chars=USERNAME_PWD_SIZE_LIMIT)

success = add_user(user, pwd, new_user)
if success:
    st.session_state.user = success
show_specific_pages(st.session_state.user == PUBLIC_USER)

left, center, right = st.columns([250, 200, 233])

left.subheader('\n')
center.subheader("Supported by:")
right.subheader('\n')
left.image("logos/Salisbury_logo.png", width=233)
center.image("logos/USDA_logo.png", width = 200)
right.image('logos/nsf.png', width = 233)
