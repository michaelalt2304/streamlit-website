from dep import *

st.write("User:", st.session_state.user)

roboflow_info = st.text_area("Import RoboFlow Information Here", value="""rf = Roboflow(api_key="YGXCqFJKogQa7WbavueN")
project = rf.workspace("oyster-pt-3").project("oyt")
version = project.version(7)
dataset = version.download("yolov9")""", height=120)
notes = st.text_input("(Optional) Add notes about this Roboflow to better identify it:", max_chars=NOTES_SIZE_LIMIT)
# st.write(notes)
# print("'" + notes + "'")
# print(notes == None)
val = st.button(label="Download RoboFlow")
if val:
    add_roboflow(st.session_state.user, roboflow_info, load=True, notes = notes)



