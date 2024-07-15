
from dep import *
from streamlit_webrtc import webrtc_streamer
from streamlit.errors import StreamlitAPIException
import supervision as sv
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

    # val = st.button('Start the webcam')
#     model = get_model(cur_model)
#     if val:
#         camera = cv2.VideoCapture(0)
#         FRAME_WINDOW = st.image([])
#         while True:
#             collected_successfully, frame = camera.read()
#             if collected_successfully:
#                 rot_colors = frame[:, :, ::-1]
#                 pil_frame = Image.fromarray(rot_colors)
#                 out_np, _, _2, _3 = ann_img_helper(pil_frame, model)
                # FRAME_WINDOW.image(out_np)
