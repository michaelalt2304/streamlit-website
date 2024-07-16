
from dep import *

from twilio.rest import Client

account_sid = 'AC96566f955b99b80802ecb8a9fc4762c9' # os.environ['TWILIO_ACCOUNT_SID']
auth_token = '66f99cdad98de8a2a9aab410fe8c1efc' # os.environ['TWILIO_AUTH_TOKEN']
twil_client = Client(account_sid, auth_token)
token = twil_client.tokens.create()
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
    webrtc_streamer(key="example", video_frame_callback=vfc, rtc_configuration={"iceServers": token.ice_servers})
    # webrtc_streamer(key="abc123", rtc_configuration={"iceServers": token.ice_servers}) # COMMENT OUT THIS LINE, UNCOMMENT ABOVE
