
# def order_by_tstamp(arr, order_ls):
#     ARR_CP = arr[:]
#     def sort_fun(el):
#         return order_ls[ARR_CP.index(el)]
#     arr.sort(key=sort_fun)
#     return arr
# arr =      ["list", "to", "swap", "around", "this", "time"]
# order_ls = [4,      5,    0,      3,        1,      2     ]
# order_by_tstamp(arr, order_ls)
# print(arr)

# def strip_chars(start: str, chrs_to_rem = [',', '\\', '"', '\'']):
#     for ch in chrs_to_rem:
#         start = start.replace(ch, '')
#     return start

# # print('<',strip_chars("''''''''"),'>', sep = '')

# ILLEGAL_STRING_CHARS = [',', '\\', '"', '\'', ';']

# print(' '.join(ILLEGAL_STRING_CHARS))
import supervision as sv
import numpy as np
import PIL.Image as Image
from ultralytics import YOLOv10
def ann_label_live(im: Image, model, label_annotator = sv.LabelAnnotator(text_scale = 0.4, text_padding = 1), bounding_box_annotator = sv.BoxCornerAnnotator(), verbose = False, conf_level = 0.05, name_labels = True):
    fix_img = im.convert('RGB')
    np_img = np.array(fix_img)
    cont_img = np.asarray(np_img, dtype=np.uint8)
    results = model(cont_img, conf=conf_level, verbose = verbose)[0]
    if name_labels:
        used_labels = np.array(results.boxes.conf.cpu())
    else:
        conf_array = np.array(results.boxes.conf.cpu())
        used_labels = [str(round(x * 100)) + '%' for x in conf_array]
    
    tot_time = sum([x for x in results.speed.values()])
    
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(
        scene=np_img, detections=detections)
    num_oysters = detections.xyxy.shape[0]
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels = used_labels if not name_labels else None)
    return(annotated_image, num_oysters, tot_time, detections)
fpath = "C:/Users/micha/Desktop/oddai_website/Files_local/oyster_test-111.jpg"
mod_path = "C:/Users/micha/Desktop/oddai_website/Files_local/58.pt"
img = frame.to_image(format="bgr24")
final_np, _, _, _ = ann_img_helper(img, model_YOLO)
# return av.VideoFrame.from_ndarray(final_np, format="rgb24")

np_im = Image.open(fpath)
mod = YOLOv10(mod_path)
ann_label_live(np_im, mod)