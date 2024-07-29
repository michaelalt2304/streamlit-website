
from dep import *
try_page_setup("Annotate Files")

all_user_files = get_raw_files(st.session_state.user, public_user = True)
models = get_models(st.session_state.user, public_user = True)
if all_user_files and models:
    cur_file = kv_select(all_user_files, 'What file would you like to annotate?', reverse=True)
    f_type = get_type_file(cur_file)

    cur_model = kv_select(models, 'What model would you like to annotate with?', reverse=True)
    name_labels = kv_select([['Names', 'Confidence Scores'], TF], 'What would you like to see as the annotations?')
    threshold = st.slider('Minimum Confidence Score (%)', min_value=5, max_value=50, value=20, step=5)

    notes_raw = st.text_input("(Optional) Add notes about this file to better identify it:", max_chars=NOTES_SIZE_LIMIT)
    notes = strip_chars(notes_raw)
    if f_type == VIDEO:
        fast_ann = st.checkbox('Reduce frame rate for faster annotation?', value = True)
    val = st.button(label="Annotate")
    if val:
        with st.spinner('Annotating...'):
            if f_type == IMAGE:
                id_ann_img = ann_img(cur_file, cur_model, threshold = threshold, name_labels = name_labels, notes=notes)
                fpath_ann = get_fpath_ann(id_ann_img)
                im = Image.open(fpath_ann)
                st.image(im)
            elif f_type == VIDEO:
                id_ann_vid = ann_video(cur_file, cur_model, threshold = threshold, name_labels = name_labels, notes=notes, fast_ann=fast_ann)
                fpath_ann = get_fpath_ann(id_ann_vid)
                st.video(fpath_ann)

        