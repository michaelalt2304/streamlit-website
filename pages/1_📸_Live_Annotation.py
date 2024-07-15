
from dep import *

try:
    st.set_page_config(
        page_title="Live Annotation",
        page_icon="🦪",
    )
except StreamlitAPIException:
    print("Couldn't label page")
# from https://github.com/whitphx/streamlit-webrtc/?tab=readme-ov-file

# st.write('Hello World')
# frame = Fr()

st.title("Webcam Live Feed")
reprime_user()
def modify_arr(arr):
    return arr
models = get_models(st.session_state.user)
if models:
    cur_model = kv_select(models, 'What model would you like to annotate with?', reverse=True)
    # print(cur_model)
    model_YOLO = get_model(cur_model)
    def vfc(frame: av.VideoFrame):
        img = frame.to_ndarray(format="bgr24")
        np_flip = img[:,::-1,:]
        
        img_pil = Image.fromarray(np_flip)
        final_np, _, _, _ = ann_img_helper(img_pil, model_YOLO)
        return av.VideoFrame.from_ndarray(final_np, format="bgr24")
    webrtc_streamer(key="example", video_frame_callback=vfc)