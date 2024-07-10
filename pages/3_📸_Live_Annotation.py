
from dep import *

st.set_page_config(
    page_title="Live Annotation",
    page_icon="🦪",
)


# st.write('Hello World')
# frame = Fr()
st.title("Webcam Live Feed")
reprime_user()
models = get_models(st.session_state.user)
if models:
    cur_model = kv_select(models, 'What model would you like to annotate with?', reverse=True)
    val = st.button('Start the webcam')
    model = get_model(cur_model)
    if val:
        camera = cv2.VideoCapture(0)
        FRAME_WINDOW = st.image([])
        while True:
            collected_successfully, frame = camera.read()
            if collected_successfully:
                rot_colors = frame[:, :, ::-1]
                pil_frame = Image.fromarray(rot_colors)
                out_np, _, _2, _3 = ann_img_helper(pil_frame, model)
                FRAME_WINDOW.image(out_np)
