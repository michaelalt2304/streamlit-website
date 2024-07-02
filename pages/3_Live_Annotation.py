# class Fr:
#     def __init__(self):
#         self.size = 0
from dep import *

# frame = Fr()
st.title("Webcam Live Feed")
st.write("User:", st.session_state.user)

cur_model = kv_select(get_models(st.session_state.user), 'What model would you like to annotate with?', reverse=True)

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

