import pandas as pd
import pymysql
from pymysql.err import IntegrityError, OperationalError
import os
from PIL import Image
import numpy as np
import supervision as sv
import cv2
import av
from PIL import Image
import shutil as sh
import re
from roboflow import Roboflow
import cv2
from ultralytics import YOLOv10
import wget
from time import time
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import streamlit as st
import io
import string
import random
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
from sqlalchemy.sql import text


temp_folder = os.path.join('.', 'Files_local')
temp_weights = os.path.join(temp_folder, 'Weights')

bba = sv.BoxCornerAnnotator()
la = sv.LabelAnnotator(text_scale = 0.4, text_padding = 1)

db_main = 'test_4'
# cur_name = 'ab'
REPLACE = 'REPLACE'

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = "molten-album-427115-q6:us-central1:oyster1"  # e.g. 'project:region:instance'
    db_user = 'root'  # e.g. 'my-db-user'
    db_pass = 'dbuserdbuser'  # e.g. 'my-db-password'
    db_name = 'test_4'  # e.g. 'my-database'

    ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool
en = connect_with_connector()

def run_sql(prompt: str, write = False):
    if write:
        st.write(prompt)
    with en.connect() as con:
        res = con.execute(text(prompt))
        
        if prompt.lower().find('select') == 0: # is a select statement            
            colnames_arr = list(res.keys())
            res_ls = [row for row in res]      
            pretty_dict = [ {colnames_arr[i] : res_ls[j][i] for i in range(len(colnames_arr))} for j in range(len(res_ls)) ]
            return pretty_dict
        else:
            con.commit()

# sql_conn = pymysql.connect(
#     user="root",
#     password="dbuserdbuser",
#     host="34.46.242.196",
#     port=st.session_state.PORT_NUMBER,
#     database=db_main,
#     cursorclass=pymysql.cursors.DictCursor,
#     autocommit=True)
# cur = sql_conn.cursor()

# conn = st.connection('mysql', type='sql')

# df = conn.query('SELECT Filepath from test_4.raw_files;', ttl=600)

# print(df)

###########################
# GOOGLE HELPER FUNCTIONS #
###########################
import json
def sign_in_storage_g(path_to_cred = '', JSON_file = 'molten-album-427115-q6-cfa4e4aaf3bd.json'):
    f = open(os.path.join(path_to_cred, JSON_file))
    credentials_dict = json.load(f)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)
    client = storage.Client(credentials=credentials, project='molten-album-427115-q6')
    bkt = client.get_bucket('test_bucket_abc123')
    print("Connected to google cloud")
    return bkt, client

b, cl = sign_in_storage_g()

def check_folder_exists_g(folder_to_upload, check_location, disable = False, full = False, bkt = b): # assume full installation
    # assumes if one file is in the right location then they all are
    try:
        if disable:
            return True
        cur_path = folder_to_upload
        path_check_exist_g = check_location
        if not os.path.exists(cur_path):
            return False
        all_items = os.listdir(cur_path)
        for added_item in all_items: # searching for a file
            cur_path = os.path.join(cur_path, added_item)
            path_check_exist_g = os.path.join(path_check_exist_g, added_item)
            cur_exists = False
            if os.path.isfile(cur_path): # if you just want to make sure one file is the same, set full to 
                cur_exists = path_exists_g(path_check_exist_g)
                if not full: 
                    return cur_exists
            elif os.path.isdir(cur_path):
                cur_exists = check_folder_exists_g(cur_path, path_check_exist_g)
            if not cur_exists:
                return False
        return True
    except Exception:
        print(f"Current folder {folder_to_upload} or {check_location} is malformed")
        return False

def upload_file_g(file_to_upload, new_name_with_path_g, bkt = b):
    blob = bkt.blob(new_name_with_path_g)
    blob.upload_from_filename(file_to_upload)
    

def upload_folder_g(folder_to_upload, new_name_with_path_g, bkt = b , level = 0, overwrite = False):
    already_uploaded = False
    if level == 0: # check if already uploaded
        already_uploaded = check_folder_exists_g(folder_to_upload, new_name_with_path_g)
        level += 1
    if os.path.exists(folder_to_upload) and (not already_uploaded or overwrite):
        for item in os.listdir(folder_to_upload):
            cur_path = os.path.join(folder_to_upload, item)
            new_path_g = os.path.join(new_name_with_path_g, item)
            if os.path.isfile(cur_path):
                upload_file_g(cur_path, new_path_g)
            elif os.path.isdir(new_path_g):
                upload_folder_g(cur_path, new_path_g, level)

def download_file_g(file_to_download_g, new_name_with_path, bkt = b):
    if not os.path.exists(new_name_with_path):
        blob = bkt.blob(file_to_download_g)
        blob.download_to_filename(new_name_with_path)

def list_blobs_g(folder_base, bkt = b, client = cl):
    """Lists all the blobs in the bucket that begin with the prefix."""
    blobs = bkt.list_blobs(prefix=folder_base)
    return blobs

def download_folder_g(folder_to_download_g, new_name_with_path, overwrite = False, level = 0, file_depth = 3):
    already_uploaded = False
    if level == 0: # check if already downloaded
        already_uploaded = os.path.exists(new_name_with_path)
        level += 1
    if not check_folder_exists_g(new_name_with_path, folder_to_download_g) and (not already_uploaded or overwrite):
        for item in list_blobs_g(folder_to_download_g):
            file_path_g = item.name
            file_name = trim_file_depth(file_path_g, start = file_depth)
            local_path = os.path.join(new_name_with_path, file_name)
            download_file_g(file_path_g, local_path)             


def make_folder_g(folder_name, bkt = b):
    blob = bkt.blob(folder_name + '/')
    blob.upload_from_string('')

def path_exists_g(file, bkt = b):
    blob = bkt.blob(file)
    return blob.exists()
###############################
# LOCAL FILE HELPER FUNCTIONS #
###############################

def get_filename(fpath):
    return fpath.replace('\\', '/').rsplit('/', 1)[-1]

def get_ext(fpath):
    fname = get_filename(fpath)
    per_index = fname.index('.')
    ext = fname[per_index + 1:].lower()
    return ext

def get_id_fname(f_out, fpath, id):
    fname = get_filename(fpath)
    per_index = fname.index('.')
    ext = fname[per_index + 1:].lower()
    return os.path.join(f_out, f"{fname[:per_index]}-{id}.{ext}").replace('\\', '/')

def get_REPLACE_ID(table, column_rep):
    res = run_sql(f"""SELECT ID from {table} where {column_rep} = '{REPLACE}'""")
    # st.write(res, table, column_rep)
    id = res[-1]['ID']
    return id

def get_match(pattern, string):
    matches = re.search(pattern, string)
    if matches:
        return(matches.group(1))
    else:
        raise ValueError(f'Improper string exported, couldn\'t find {pattern} in the given text')



def delete_folder(name, base = "."):
    fpath = os.path.join(base, name)
    if os.path.exists(fpath):
        for item in os.listdir(fpath):
            new_path = os.path.join(fpath, item)
            if os.path.isfile(new_path):
                os.remove(new_path)
            elif os.path.isdir(new_path):
                delete_folder(item, fpath)
        os.rmdir(fpath)
                
def make_folder(fpath, overwrite = False):
    delete_folder(fpath, '.') if overwrite else None
    if not os.path.exists(fpath):
        os.mkdir(fpath)
        
def get_temp_fname(fpath, temp_f = temp_folder):
    fname = fpath.replace('\\', '/').rsplit('/', 1)[-1]
    return os.path.join(temp_folder, fname).replace('\\', '/')

def trim_file_depth(fpath, start = 0, end = 'Unused'):
    split_ls = fpath.rsplit('/')
    if end == 'Unused':
        end = len(split_ls)
    return '/'.join(split_ls[start:end])


if not path_exists_g('Files/'):
    make_folder_g('Files')
    make_folder_g('Files/Video_raw')
    make_folder_g('Files/Video_ann')
    make_folder_g('Files/Image_raw')
    make_folder_g('Files/Image_ann')
    make_folder_g('Files/Model')
    make_folder_g('Files/Roboflow')
make_folder(temp_folder)

###########################
# SQL/Database Management #
###########################
def insert_user(name, password):
    run_sql(f"INSERT INTO people (Username, Password, Time_Created) VALUES ('{name}', '{password}', CURRENT_TIMESTAMP );")
    st.write('Account created!')
    return name

def add_user(name, password, new_user):
    '''
    Returns: name if query is successful, False if not
    '''
    if not password:
        return False
    res = run_sql(f"SELECT Username, Password FROM people WHERE Username = '{name}'")
    # st.write(res)
    if res:
        res_val = res[-1]
        if new_user:
            if res_val['Password'] == password:
                st.write('Signed in!')
                return name
            else:
                st.write('User with this name already exists.')
                return False
        else:
            if res_val['Password'] == password:
                st.write('Signed in!')
                return name
            else:
                st.write('Wrong password. Please try again.')
                return False
    elif not res:
        if not new_user:
            st.write(f"User is not in database. Please make a new account.")
            return False
        else:
            return insert_user(name, password)


def add_photo(user, im, filename, notes = '', f_out = 'Files/Image_raw'):
    '''
    Returns: Index of added photo if successful, 0 if not
    '''
    # im is a PILLOW image
    width = im.size[0]
    height = im.size[1]
    f_temp = get_temp_fname(filename)

    im.save(f_temp)
    fsize = os.stat(f_temp).st_size
    ext = get_ext(f_temp)
    
    run_sql(f"INSERT INTO raw_files (Username, Filepath, Filename, Local_Path, Size, Type, Extension, Notes, Width, Height, Timestamp) VALUES ('{user}', '{REPLACE}', '{REPLACE}', '{REPLACE}', {fsize}, 'Image', '{ext}', '{notes}', {width}, {height}, CURRENT_TIMESTAMP);")
    id = get_REPLACE_ID(table='raw_files', column_rep='Filepath')

    f_id_name_g = get_id_fname(f_out, f_temp, id)
    temp_fname = get_temp_fname(f_id_name_g)
    fname = get_filename(temp_fname)
    # print(temp_fname)
    upload_file_g(f_temp, f_id_name_g)
    run_sql(f"UPDATE raw_files SET Filepath = '{f_id_name_g}', Local_Path = '{temp_fname}', Filename = '{fname}' WHERE ID = {id};")
    # print(f"\n\n\n\n'{user}', '{f_id_name_g}', '{temp_fname}', {fsize}, 'Image', '{ext}', '{notes}', {width}, {height}")
    return id

def get_files(user):
    res = run_sql(f"SELECT Filepath, Filename, ID FROM raw_files WHERE Username = '{user}';")
    keys = [row['Filename'] for row in res]
    values = [row['ID'] for row in res]
    return keys, values


def get_models(name):
    res = run_sql(f"SELECT * FROM roboflow INNER JOIN models ON roboflow.ID = models.Roboflow_ID WHERE username = '{name}' AND models.Local_Path != '{REPLACE}';")
    # st.write(res)
    mod_names_keys = [f"{row['Model_Type']}v{row['Version']} {row['Width_Training_Images']}x{row['Height_Training_Images']} with {row['Workspace']} {row['Timestamp']}" for row in res]
    all_mods_values = [row['ID'] for row in res]

    return mod_names_keys, all_mods_values

def ann_img_helper(im: Image, model, label_annotator = la, bounding_box_annotator = bba, verbose = False, conf_level = 0.05, name_labels = False) -> np.ndarray:
    fix_img = im.convert('RGB')
    np_img = np.array(fix_img)
    cont_img = np.asarray(np_img, dtype=np.uint8)
    results = model(cont_img, conf=conf_level, verbose = verbose)[0]
    if name_labels:
        print(results)
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
        scene=annotated_image, detections=detections, labels = used_labels)
    return(annotated_image, num_oysters, tot_time, detections)

def get_model(id: int):
    
    cur_model = run_sql(f"SELECT Filepath, Local_Path FROM models WHERE ID = {id}")[-1]
    download_file_g(cur_model['Filepath'], cur_model['Local_Path'])
    try:
        model = YOLOv10(cur_model['Local_Path'])
        return model
    except RuntimeError:
        get_model(id)
        st.write('Getting model failed')

def get_raw_fpath(id: int) -> str:
    
    cur_file = run_sql(f"SELECT Filepath, Local_Path FROM raw_files WHERE ID = {id}")[-1]
    download_file_g(cur_file['Filepath'], cur_file['Local_Path'])
    return cur_file['Local_Path']


def get_raw_image(id: int) -> Image:
    im = Image.open(get_raw_fpath(id))
    return im



def ann_img(Raw_File_ID, Model_ID, threshold, notes = '', f_out = 'Files/Image_ann'):
    
    res = run_sql(f"SELECT * from annotated_files WHERE Model_ID = {Model_ID} AND Raw_File_ID = {Raw_File_ID} AND Confidence_Threshold = {threshold}")
    if res:
        st.write('Image Already Annotated')
        return res[-1]['ID']
    
    model = get_model(Model_ID)
    im = get_raw_image(Raw_File_ID)
    raw_filepath = get_raw_fpath(Raw_File_ID)

    annot, num_oysters, tot_time, end_ann_data = ann_img_helper(im, model, conf_level = threshold / 100)
    run_sql(f"INSERT INTO annotated_files (Raw_File_ID, Model_ID, Confidence_Threshold, Filepath, Time_to_Annotate, Notes, Timestamp) VALUES ('{Raw_File_ID}', '{Model_ID}', {threshold}, '{REPLACE}', '{tot_time}', '{notes}', CURRENT_TIMESTAMP);")
    id = get_REPLACE_ID(table='annotated_files', column_rep='Filepath')
    f_id_name_g = get_id_fname(f_out, raw_filepath, id)
    f_local = get_temp_fname(f_id_name_g)
    print(f_local)

    im_f = Image.fromarray(annot)
    im_f.save(f_local)



    upload_file_g(f_local, f_id_name_g)


    run_sql(f"UPDATE annotated_files SET Filepath = '{f_id_name_g}', Local_Path = '{f_local}' WHERE ID = {id};")
    run_sql(f"INSERT INTO annotated_photos (Ann_File_ID, Number_of_Oysters) VALUES ({id}, {num_oysters})")

    # coord = end_ann_data.xyxy
    # conf = end_ann_data.confidence
    # names = end_ann_data.data['class_name']
    # class_num = end_ann_data.class_id
    # for idx in range(len(coord)):
    #     coord_cur = coord[idx]
    #     cur.execute(f"INSERT INTO oysters_in_photo (Ann_File_ID, Confidence, X1, Y1, X2, Y2, Class, Class_Index) VALUES ({id}, {conf[idx]}, {coord_cur[0]}, {coord_cur[1]}, {coord_cur[2]}, {coord_cur[3]}, '{names[idx]}', {class_num[idx]});")
    return id

# ann_img(66, 28)

def ann_video(Raw_File_ID, Model_ID, notes = '', f_out = 'Files/Video_ann', threshold = 30):
    res = run_sql(f"SELECT * from annotated_files WHERE Model_ID = {Model_ID} AND Raw_File_ID = {Raw_File_ID} AND Confidence_Threshold = {threshold}")
    if res:
        st.write('Video already annotated')
        return res[-1]['ID']
    

    model = get_model(Model_ID)

    raw_filepath = get_raw_fpath(Raw_File_ID)

    avg_oysters, time_s, out_path, ann_rate = ann_video_helper(raw_filepath, model, out_location = temp_folder, conf_level = threshold / 100)

    run_sql(f"INSERT INTO annotated_files (Raw_File_ID, Model_ID, Filepath, Time_to_Annotate, Notes, Confidence_Threshold, Timestamp, Local_Path) VALUES ('{Raw_File_ID}', '{Model_ID}', '{REPLACE}', '{time_s * 1000}', '{notes}', {threshold}, CURRENT_TIMESTAMP, '{REPLACE}');")

    id = get_REPLACE_ID(table='annotated_files', column_rep='Filepath')

    f_id_name_g = get_id_fname(f_out, raw_filepath, id)
    
    f_local = get_temp_fname(f_id_name_g)
    
    os.rename(out_path, f_local)

    run_sql(f"UPDATE annotated_files SET Filepath = '{f_id_name_g}', Local_Path = '{f_local}' WHERE ID = {id};")

    run_sql(f"INSERT INTO annotated_videos (ID, Annotation_Rate, Tracing, Average_Number_of_Oysters) VALUES ({id}, {ann_rate}, 0, {avg_oysters})")

    upload_file_g(f_local, f_id_name_g)
    
    return id


def add_video(name, fpath, fname, notes = '', f_out = 'Files/Video_raw'):
    '''
    Returns: Index of added video if successful, 0 if not
    '''
    cap = cv2.VideoCapture(fpath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fsize = os.stat(fpath).st_size
    ext = get_ext(fpath)
        
    run_sql(f"INSERT INTO raw_files (Username, Filepath, Filename, Local_Path, Size, Type, Extension, Notes, Width, Height, Timestamp) VALUES ('{name}', '{REPLACE}', '{REPLACE}', '{REPLACE}', {fsize}, 'Video', '{ext}', '{notes}', {width}, {height}, CURRENT_TIMESTAMP);")
    id = get_REPLACE_ID(table='raw_files', column_rep='Filepath')
    f_id_name_g = get_id_fname(f_out, fname, id)
    # print(f_id_name_g)
    temp_path = get_temp_fname(f_id_name_g)
    # print(temp_path)
    upload_file_g(fpath, f_id_name_g)
    
    os.rename(fpath, temp_path)

    fname = get_filename(temp_path)
    run_sql(f"UPDATE raw_files SET Filepath = '{f_id_name_g}', Local_Path = '{temp_path}', Filename = '{fname}' WHERE ID = {id};")

    fps = cap.get(cv2.CAP_PROP_FPS)
    color_order = 'RGB' # FIXME - cant figure out how to extract from cv2 object
    
    

    cur.execute(f"INSERT INTO videos (Raw_File_ID, FPS, Color_Order) VALUES ('{id}', '{fps}', '{color_order}');")

    return id



def get_fpath_ann(ann_id):
    res = run_sql(f"SELECT Local_Path, Filepath from annotated_files WHERE ID = {ann_id}")[-1]
    download_file_g(res['Filepath'], res['Local_Path'])
    return res['Local_Path']
# ann_photo_id = ann_img(id_raw_photo, id_mod)

def download_roboflow(api_key, workspace, project, version, download, location):
    # if not os.path.exists(folder_roboflow):
    with st.spinner(f"Loading RoboFlow data from {workspace}"):
        rf = Roboflow(api_key = api_key)
        project = rf.workspace(workspace).project(project)
        version = project.version(version)
        dat = version.download(download, location = location)
        
        fpath = os.path.join(location, 'data.yaml')
        
        with open(fpath) as f1:
            lines = f1.readlines()
        with open(fpath, 'w') as f2:
            f2.writelines(lines[:-4])
            f2.write("test: ../test/images\ntrain: ../train/images\nval: ../valid/images\n\n")

def add_roboflow(name, export_string, f_out = 'Files/Roboflow', f_weights = "Files/Weights", load = False):
    
    '''
    Returns: Index of added roboflow if successful, 0 if not
    '''
    pattern_api = r'api_key\s*=\s*"([^"]+)"'
    api_key_lab = get_match(pattern_api, export_string)

    pattern_workspace = r'rf\.workspace\("([^"]+)"\)'
    workspace_lab = get_match(pattern_workspace, export_string)

    pattern_project = r'project\("([^"]+)"\)'
    project_lab = get_match(pattern_project, export_string)

    pattern_version = r'version\((\d+)\)'
    version_lab = get_match(pattern_version, export_string)

    pattern_download = r'\bdownload\("([^"]+)"\)'
    download_lab = get_match(pattern_download, export_string)
    
#     f_temp = get_temp_fname(f_out)
    folder_name = f'{workspace_lab}_{project_lab}_{version_lab}_{download_lab}'
    f_temp = os.path.join(temp_folder, folder_name)
    
    folder_g = os.path.join(f_out, folder_name)
#     folder_roboflow = f"{f_out}/{workspace_lab}_{project_lab}_{version_lab}_{download_lab}"
    # print(api_key_lab, workspace_lab, project_lab, version_lab, download_lab, f_temp)
    if load:
        download_roboflow(api_key_lab, workspace_lab, project_lab, version_lab, download_lab, f_temp)
    
    upload_folder_g(f_temp, folder_g)
    
    run_sql(f"INSERT INTO roboflow (Api_Key, Workspace, Project, Version, Download, Local_Path, Username, Timestamp) VALUES ('{REPLACE}', '{workspace_lab}', '{project_lab}', '{version_lab}', '{download_lab}', '{f_temp}', '{name}', CURRENT_TIMESTAMP);")
    
    id = get_REPLACE_ID(table='roboflow', column_rep='Api_Key')
    
    run_sql(f"UPDATE roboflow SET Api_Key = '{api_key_lab}' WHERE ID = {id};")
    
    st.write("All done!")
    return id

def download_weight(path, ver): # one of ['n', 's', 'm', 'b', 'x', 'l']
    with st.spinner("Getting Pre-Trained Weights File"):
        valid_ver = ['n', 's', 'm', 'b', 'l', 'x']
        if ver not in valid_ver:
            assert ValueError('Invalid version selected. Must be one of: n, s, m, b, l, x,  for nano, small, medium, big, large, extra large respectively')
        prefix = "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10"
        suffix = ".pt"
        fname = 'yolov10' + ver + suffix
        web_path = prefix + ver + suffix
        computer_path = os.path.join(path, fname)
        
        if not os.path.exists(computer_path):
            wget.download(web_path, out = path)
        return computer_path

def get_roboflow(user):
    res = run_sql(f"SELECT ID, Project, Workspace, Version FROM roboflow WHERE Username = '{user}'")

    return [f"{row['Workspace']}, {row['Project']} v{row['Version']} ({row['ID']})" for row in res], [row['ID'] for row in res]


def add_model(roboflow_ID, size_mod = 'n', epochs = 10, batch = 32, f_out = "Files/Model"):
    
    weights_path = download_weight(temp_folder, size_mod)
    
    
   
    res = run_sql(f"SELECT * FROM roboflow WHERE ID = {roboflow_ID}")[-1]
    print(res)

    download_roboflow(res['Api_Key'], res['Workspace'], res['Project'], res['Version'], res['Download'], res['Local_Path'])
    
    pt = os.path.join(os.getcwd(), res['Local_Path'], 'data.yaml')

    samp_photo = os.path.join(res['Local_Path'], 'test', 'images')
    first_photo = os.listdir(samp_photo)[0]
    im = Image.open(os.path.join(samp_photo, first_photo))
    width = im.size[0]
    height = im.size[1]
                                                               
    run_sql(f"""INSERT INTO models (Timestamp, Filepath, Local_Path, Version, 
                 Hyperparams, Epoch, Batch, Model_Type, Width_Training_Images, Height_Training_Images, 
                 Size, Roboflow_ID) values (CURRENT_TIMESTAMP, '{REPLACE}', '{REPLACE}', 10, NULL, {epochs}, {batch}, 
                 'YOLO', {width}, {height}, '{size_mod}', {roboflow_ID})
                 """)
    
    id_mod = get_REPLACE_ID(table='models', column_rep='Filepath')
    pts_name = f'{id_mod}.pt'
    model_path_g = os.path.join(f_out, pts_name)
    # 
    pts_save_path = os.path.join(temp_folder, pts_name)
    temp_train_path = f"Run_{id_mod}"


    with st.spinner('Training model...'):
        os.system(f"yolo task=detect mode=train epochs={epochs} batch={batch} plots=False model={weights_path} data={pt} name={temp_train_path}")

    orig_pts_path = os.path.join('runs', 'detect', temp_train_path, 'weights', 'best.pt')
    upload_file_g(orig_pts_path, model_path_g)
    os.rename(orig_pts_path, pts_save_path) # for later inference, on computer because people will likely want the model then
    
    run_sql(f"UPDATE models SET Filepath = '{model_path_g}', Local_Path = '{pts_save_path}' WHERE ID = {id_mod};")

    delete_folder('runs')
    return id_mod




# id_mod = add_model(id_rob,epochs=1, size_mod = 'n')

def kv_select(kvlist, label = "", reverse = False):
    KEYS = 0
    VALUES = 1
    # print(kvlist)
    if kvlist != ([], []):
        selected = st.selectbox(
            label,
            kvlist[KEYS][::-1] if reverse else kvlist[KEYS])
        return kvlist[VALUES][kvlist[KEYS].index(selected)]
    else:
        st.write('No values found')

def generate_random_string(length):

  letters = string.ascii_letters + string.digits
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

def get_type_file(ID):
    # st.write(ID)
    res = run_sql(f"SELECT Type FROM raw_files WHERE ID = {ID}")[-1]
    return res['Type']

def ann_video_helper(input_vid, model, conf_level, out_location = '.', im_width = 416, im_height = 416):
    tot_oysters = 0
    tot_frame = 0
    
    bba = sv.BoundingBoxAnnotator()
    la = sv.LabelAnnotator()

    container = av.open(input_vid)
    stream_vid = container.streams.video[0]
    fname = input_vid.rsplit('/', 1)[-1]
    per_index = fname.index('.')
    out_path = os.path.join(out_location, f'{fname[:per_index]}_annotated.mp4')
    outp = av.open(out_path, 'w')
    codec_name = stream_vid.codec_context.name
    fps = stream_vid.codec_context.rate
    output_stream = outp.add_stream(codec_name, str(fps))
    output_stream.width = im_width
    output_stream.height = im_height
    output_stream.pix_fmt = stream_vid.codec_context.pix_fmt
    start = time()
    for index, frame in enumerate(container.decode(stream_vid)):
        pil_img = frame.to_image()
        np_img = np.array(pil_img)
        np_img_resize = cv2.resize(np_img, (im_width, im_height))
        np_rot = np_img_resize[:, :, ::-1]
        small_pil_img = Image.fromarray(np_rot)
        # np_image_2 = np.array(small_pil_img)
        an_mg, num_oysters, _, _2z = ann_img_helper(small_pil_img, model, conf_level = conf_level)
        tot_oysters += num_oysters
        frame_out = av.VideoFrame.from_ndarray(an_mg, format='bgr24')
        pkt = output_stream.encode(frame_out)
        outp.mux(pkt)
    end = time()
    net_time = end - start
    container.close()
    outp.close()
    ann_rate = (index / fps) / net_time # ratio of time to annotate versus length of video
    return tot_oysters / index, net_time, out_path, ann_rate

