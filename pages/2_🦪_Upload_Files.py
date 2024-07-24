from dep import *

try_page_setup("Upload Files")

notes_raw = st.text_input("(Optional) Add notes about this file to better identify it:", max_chars=NOTES_SIZE_LIMIT)
notes = strip_chars(notes_raw)
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    split_type = uploaded_file.type.rsplit('/')
    type_file = split_type[0]
    ext = split_type[1]
    # st.write(uploaded_file)
    # st.write(type_file)
    fname = uploaded_file.name
    try:
        if type_file == 'image':
            img = Image.open(io.BytesIO(uploaded_file.getvalue()))

            # img.show()
            st.image(img, caption = "Uploaded image")
            raw_photo_id = add_photo(st.session_state.user, img, fname, notes = notes)
            st.write(f"Added photo with ID = {raw_photo_id}")
        elif type_file == 'video':
            # st.write("Here")
            vid_data = io.BytesIO(uploaded_file.getvalue())
            fpath = os.path.join(temp_folder, generate_random_string(15) + '.' + ext)
            
            with st.spinner('Saving video'):
                with open(fpath, 'wb') as f:
                    f.write(vid_data.getbuffer())
                st.video(fpath)
                id_vid = add_video(st.session_state.user, fpath, fname, notes = notes)
            st.write(f"Added video with ID = {id_vid}")
    except Exception:
        st.write(Exception)
        





        

