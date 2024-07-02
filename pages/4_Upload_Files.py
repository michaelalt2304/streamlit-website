from dep import *




# if 'user' not in st.session_state:
#     print("Lost variable")
#     st.session_state['user'] = 'a'

st.write("User:", st.session_state.user)

# st.write("Upload files here")

# st.write("User:", st.session_state.user)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    split_type = uploaded_file.type.rsplit('/')
    type_file = split_type[0]
    ext = split_type[1]
    # st.write(uploaded_file)
    # st.write(type_file)
    fname = uploaded_file.name
    if type_file == 'image':
        
        # print('Here')
        img = Image.open(io.BytesIO(uploaded_file.getvalue()))

        # img.show()
        st.image(img, caption = "Uploaded image")
        raw_photo_id = add_photo(st.session_state.user, img, fname)
        st.write(f"Added photo with ID = {raw_photo_id}")
    elif type_file == 'video':
        # st.write("Here")
        vid_data = io.BytesIO(uploaded_file.getvalue())
        fpath = os.path.join(temp_folder, generate_random_string(15) + '.' + ext)
        
        with st.spinner('Saving video'):
            with open(fpath, 'wb') as f:
                f.write(vid_data.getbuffer())
            st.video(fpath)
            id_vid = add_video(st.session_state.user, fpath, fname)
        st.write(f"Added video with ID = {id_vid}")
        





        

