from dep import *

try_page_setup("Gallery")

st.title("A place to see all your fantastic files")

raw_files = get_raw_files(st.session_state.user, public_user=True)
st.subheader("Raw")
rf = kv_select(raw_files, container=st, reverse = True)
show_file(rf, 'raw_files', st)

st.subheader("Annotated")
ann_files = get_ann_files(st.session_state.user, public_user = True)
af = kv_select(ann_files, container=st, reverse = True)
show_file(af, 'annotated_files', st)
# right_gal.subheader("Annotated")
# af = kv_select(raw_files, container=right_gal, key = generate_random_string(5))
# show_file(af, 'Annotated_Files', right_gal)

