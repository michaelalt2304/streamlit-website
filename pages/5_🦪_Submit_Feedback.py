from dep import *

try_page_setup("Submit Feedback")

MAX_FEEDBACK_TBOX = 2048
st.title("Fill out as many fields as you want, then hit \"Submit\" when you are done")
def get_null_or_val(s: str):
    return "'" + strip_chars(s)  + "'" if s else 'NULL'


def get_rating(msg, cont = st):
    r = cont.slider(msg, min_value = 0, max_value=10, value=0, step=1)
    return r

with st.form("feedback_form"):
    
    st.header("Category Ratings")
    st.subheader("Note - Leaving a score of 0 will make it not count in statistics. The scale is 1-10.")


    overall = get_rating("Overall")
    ui = get_rating("User Interface")
    eou = get_rating("Ease of use")
    app = get_rating("Applicability")
    speed = get_rating("Speed of Features")
    la = get_rating("Live Annotation Page")
    fu = get_rating("File Upload Page")
    af = get_rating("Annotating File Page")
    rg = get_rating("Gallery Page")
    how_use = st.text_area("How did you use this website?", max_chars=MAX_FEEDBACK_TBOX)
    bugs = st.text_area("Bugs to report. Please paste error message or describe what happened where.", max_chars=MAX_FEEDBACK_TBOX)
    comm = st.text_area("Any other comments?", max_chars=MAX_FEEDBACK_TBOX)
    funct = st.text_area("Any additional functionality you would like to see with the website?", max_chars=MAX_FEEDBACK_TBOX)

    arr_ratings = [overall, ui, eou, app, speed, la, fu, af, rg]

    ratings_str = ", ".join([str(x) if x != 0 else "NULL" for x in arr_ratings])

    sub = st.form_submit_button("Submit")
    if sub:
        run_sql(f"""INSERT INTO feedback (Username, Rating_Overall, Rating_UI, Rating_Ease_Of_Use, Rating_Applicability, 
                Rating_Speed, Rating_Live_Annotation, Rating_File_Upload, Rating_Annotating_Files, Rating_Gallery, How_Use, Bugs, 
                Additional_Comments, Additional_Functionality, Timestamp) VALUES ('{st.session_state.user}', {ratings_str}, {get_null_or_val(how_use)}, {get_null_or_val(bugs)}, {get_null_or_val(comm)}, {get_null_or_val(funct)}, 
                CURRENT_TIMESTAMP);""")
        st.write("Form received")
    


st.write("Thanks for your time! We are constantly looking to improve the website, and will be looking at your comments soon.")
