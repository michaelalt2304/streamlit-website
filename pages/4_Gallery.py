from dep import *

def show_file(id: int, table: str, _container = st):
    with st.spinner('Fetching...'):
        if table == 'raw_files':
            res = run_sql(f'SELECT * from {table} WHERE ID = {id}')[-1]
        elif table == 'annotated_files':
            res = run_sql(f"SELECT annotated_files.Filepath as Filepath, annotated_files.Local_Path as Local_Path, raw_files.Type as Type, annotated_files.Confidence_Threshold as ct from annotated_files LEFT JOIN raw_files ON annotated_files.Raw_File_ID = raw_files.ID WHERE annotated_files.ID = {id}")[-1]
        # print("Here\n\n\n\n")
        download_file_g(res['Filepath'], res['Local_Path'])
        if table == 'annotated_files':
            st.write("Confidence Threshold:", str(res['ct']) + '%')
        # st.write(res['Filepath'])
        if res['Type'] == 'Image':
            _container.image(res['Local_Path'], width=500)
        elif res['Type'] == 'Video':
            _container.video(res['Local_Path'])

reprime_user()
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

