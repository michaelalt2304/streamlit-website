# TO ACCESS THESE PAGES, ON A COMPUTER WITH GPU:
# 1. Navigate to oddai_website on terminal
# 2. Run $ pip install -r requirements.txt
# 3. Run $ streamlit run Sign_In.py
# 4. On the opening page, use username = Public, password = Franklin2304!
# Go to Add Roboflow and Train Models tabs that appear on sidebar

from dep import *
try_page_setup("Add Roboflow")

st.title('Import Roboflow Data')
st.image('logos/Roboflow_logo.png')
expander = st.expander('Need help:question:')
expander.subheader('Instructions:')
expander.markdown(""" Skip the first two steps if you already have a project in mind
1. Go to [Roboflow Universe](https://universe.roboflow.com) and enter keywords for the type of detection you would like to perform
2. Click on the project you are interested in, and go to the 'Download Dataset tab' for the most recent version of the project and YOLO
3. Once the popup dialog appears, select 'Show Download Code'
4. Use the Jupyter tab, and copy all the code with the double square icon in the corner
5. Paste into the below dialog box and click 'Download Roboflow'            
""")
roboflow_info = st.text_area("Import RoboFlow Information Here", value="""rf = Roboflow(api_key="YGXCqFJKogQa7WbavueN")
project = rf.workspace("oyster-pt-3").project("oyt")
version = project.version(7)
dataset = version.download("yolov9")""", height=120)
notes_raw = st.text_input("(Optional) Add notes about this Roboflow to better identify it:", max_chars=NOTES_SIZE_LIMIT)
notes = strip_chars(notes_raw)
# st.write(notes)
# print("'" + notes + "'")
# print(notes == None)
val = st.button(label="Download RoboFlow")
if val:
    add_roboflow(st.session_state.user, roboflow_info, load=True, notes = notes)



