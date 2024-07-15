import streamlit as st
from st_pages import hide_pages, show_pages, Page
# to deploy - https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe
st.set_page_config(
    page_title="OddAI",
    page_icon="🦪",
)
from dep import *



st.title('Welcome to OddAI: Oyster Development Detection Artificial Intelligence :oyster:')
st.subheader('Uses a YOLOv10 Backend with support for live detection, video, and image annotation, as well as customized models')
def show_specific_pages(is_public: bool):
    used_pages = [
            Page("app.py", "Sign In", "🔑"),
            Page("pages/1_📸_Live_Annotation.py", "Live Annotation", "📸"),
            Page("pages/2_⬆️_Upload_Files.py", "Upload Files", "⬆️"),
            Page("pages/3_📝_Annotate_Files.py", "Annotate Files", "📝"),
            Page("pages/4_🤖_Add_Roboflow.py", "Add Roboflow", "🤖") if is_public else None,
            Page("pages/5_🏃‍♂️_Train_Model.py", "Train Model", "🏃‍♂️") if is_public else None
                 ]

    show_pages([page for page in used_pages if page != None])
show_specific_pages(False)
st.session_state.user = GUEST # default is guest



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
