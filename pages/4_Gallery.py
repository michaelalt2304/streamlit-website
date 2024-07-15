from dep import *

reprime_user()
st.title("A place to see all your fantastic files")
left_gal, right_gal = st.columns(2)
raw_files = get_raw_files(st.session_state.user)
left_gal.subheader("Raw")
rf = kv_select(raw_files, container=left_gal, key = generate_random_string(5))
left_gal.write(rf)
# left_gal.image()
right_gal.subheader("Annotated")
af = kv_select(raw_files, container=right_gal, key = generate_random_string(5))
# right_gal.image()


