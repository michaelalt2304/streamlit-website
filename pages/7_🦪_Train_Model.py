# TO ACCESS THESE PAGES, ON A COMPUTER WITH GPU:
# 1. Navigate to oddai_website on terminal
# 2. Run $ pip install -r requirements.txt
# 3. Run $ streamlit run Sign_In.py
# 4. On the opening page, enter username = Public, password = Franklin2304!
# Go to Add Roboflow and Train Model tabs that appear on sidebar

from dep import *

try_page_setup("Train Model")

roboflow_IDs = get_roboflow(st.session_state.user)
# print(roboflow_IDs)
if roboflow_IDs:
    MODEL_SIZE_ARRAY = ['n', 's', 'm', 'b', 'l', 'x']
    MODEL_SIZE_DESC_ARRAY = ['Nano', 'Small', 'Medium', 'Big', 'Large', 'X-tra Large']

    roboflow_ID = kv_select(roboflow_IDs, label = 'What roboflow model do you want to use?', reverse=True)
    model_size = kv_select((MODEL_SIZE_DESC_ARRAY, MODEL_SIZE_ARRAY), label = 'What size do you want your model to be?', reverse = False)

    epoch_st = st.slider('Epochs', min_value=1, max_value=150, value=75, step=1)
    batch_st = st.select_slider('Batch Size', options = [2**i for i in range(0, 4 + 1)], value = 8)
    notes_raw = st.text_input("(Optional) Add notes about this model to better identify it:", max_chars=NOTES_SIZE_LIMIT)
    notes = strip_chars(notes_raw)
    val = st.button(label="Train")
    if val:
        id_model = add_model(st.session_state.user, roboflow_ID, size_mod = model_size, epochs = epoch_st, batch = batch_st, notes = notes)
        st.write(f"Added model with ID {id_model}")