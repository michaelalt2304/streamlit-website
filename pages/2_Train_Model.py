from dep import *

st.write("User:", st.session_state.user)

roboflow_IDs = get_roboflow(st.session_state.user)
if roboflow_IDs:
    MODEL_SIZE_ARRAY = ['n', 's', 'm', 'b', 'l', 'x']
    MODEL_SIZE_DESC_ARRAY = ['Nano', 'Small', 'Medium', 'Big', 'Large', 'X-tra Large']
    MODEL_SIZE_DICT = dict(zip(MODEL_SIZE_DESC_ARRAY, MODEL_SIZE_ARRAY))

    roboflow_ID = kv_select(roboflow_IDs, label = 'What roboflow model do you want to use?', reverse=True)
    model_size = kv_select((MODEL_SIZE_DESC_ARRAY, MODEL_SIZE_ARRAY), label = 'What size do you want your model to be?', reverse = False)

    epoch_st = st.slider('Epochs', min_value=1, max_value=20, value=2, step=1) #FIXME - Default should be higher, low for testing
    batch_st = st.select_slider('Batch Size', options = [2**i for i in range(0, 4 + 1)], value = 8)
    val = st.button(label="Train")
    if val:
        id_model = add_model(roboflow_ID, size_mod = model_size, epochs = epoch_st, batch = batch_st)
        st.write(f"Added model with ID {id_model}")
else:
    st.write("No Roboflow models added yet. Please do so on the left panel to continue")