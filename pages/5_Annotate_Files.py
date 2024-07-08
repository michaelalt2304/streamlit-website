
from dep import *

st.write("User:", st.session_state.user)
all_user_files = get_files(st.session_state.user, public_user = True)
models = get_models(st.session_state.user, public_user = True)
if all_user_files and models:
    cur_file = kv_select(all_user_files, 'What file would you like to annotate?', reverse=True)
    st.write('You selected:', cur_file)
    f_type = get_type_file(cur_file)
    st.write(f_type)
    
    cur_model = kv_select(models, 'What model would you like to annotate with?', reverse=True)
    st.write('You selected:', cur_model)
    name_labels = kv_select([['Names', 'Confidence Scores'], [True, False]], 'What would you like to see on the annotations?')
    threshold = st.slider('Minimum Confidence Score (%)', min_value=5, max_value=50, value=20, step=5)


    val = st.button(label="Annotate")
    if val:
        with st.spinner('Annotating...'):
            if f_type == 'Image':
                id_ann_img = ann_img(cur_file, cur_model, threshold = threshold, name_labels = name_labels)
                fpath_ann = get_fpath_ann(id_ann_img)
                im = Image.open(fpath_ann)
                st.image(im)
            elif f_type == 'Video':
                id_ann_vid = ann_video(cur_file, cur_model, threshold = threshold, name_labels = name_labels)
                fpath_ann = get_fpath_ann(id_ann_vid)
                st.video(fpath_ann)

        