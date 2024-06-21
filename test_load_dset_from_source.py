# %%
import json
from datasets import load_dataset, Audio

# %%
from datasets import DownloadManager as dl_manager

# _URL = "https://abuelkhair.net/corpus/Alittihad_XML_utf_8.rar"
_URL = "https://drive.usercontent.google.com/download?id=1YUYaLAoPBU1HyUy95qY7cWll7-bq_x92&export=download&authuser=0"

# _URLS = {
#       "beta_image" :"https://drive.google.com/uc?export=download&id=1Sdv0pPYS0dwBvJGCKthQIge6IthlEeNo",
#       "beta_anno": "https://drive.google.com/uc?export=download&id=175eCHpbGSaNWqPcFY5f0LlX014MAarXK",
#       "v100_image": "https://drive.google.com/uc?export=download&id=19JIxAjjXWuJ7mEyUl5-xRr2B8uOb-GKk",
#       "v100_anno": "https://drive.google.com/uc?export=download&id=1Xi5ucRUb1e9TUU-nv2rCUYv2ANVsXYDk",
#       "train_data": "https://drive.google.com/uc?export=download&id=1KXf5937l-Xu_sXsGPuQOgFt4zRaXlSJ5",
#       "train_label": "https://drive.google.com/uc?export=download&id=1IbmLg-4l-3BtRhprDWWvZjCp7lqap0Z-",
#       "test_data": "https://drive.google.com/uc?export=download&id=1KSt5AiRIilRryh9GBcxyUUhnbiScdQ-9",
#       "test_label": "https://drive.google.com/uc?export=download&id=1GYcaUInkxtuuQps-qA38u-4zxK7HgrAB",
#    }

# _URLS = "https://bark.phon.ioc.ee/voxlingua107/{identifier}.zip"
# _LANGUAGES = ["ceb", "ind", "jav", "khm", "lao", "zlm", "mya", "sun", "tha", "tgl", "vie", "war"]  # We follow ISO639-3 language code (https://iso639-3.sil.org/code_tables/639/data)

# _LANG_TO_DATASOURCE_LANG = {
#     "ceb": "ceb",
#     "ind": "id",
#     "jav": "jw",
#     "khm": "km",
#     "lao": "lo",
#     "zlm": "ms",
#     "mya": "my",
#     "sun": "su",
#     "tha": "th",
#     "tgl": "tl",
#     "vie": "vi",
#     "war": "war"}

# train_url_list = [_URLS.format(identifier=_LANG_TO_DATASOURCE_LANG[lang_val]) for lang_val in _LANGUAGES]
# train_url = "https://drive.google.com/uc?export=download&id=1Kznkw7YpRiWpdgH4_SVNwp0uGf3j-5e2"
# train_url = "https://drive.usercontent.google.com/download?id=1Kznkw7YpRiWpdgH4_SVNwp0uGf3j-5e2&export=download&authuser=0&confirm=t&at=APZUnTUipgXFddMqufsKfweIjKoj%3A1713711136043"
# local_dl_path = dl_manager().extract(gdown)

import requests

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('NID'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()

    init_response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(init_response)

    if token:
        print(token)
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

    return destination, init_response

# _URL = "https://drive.google.com/uc?id=1YUYaLAoPBU1HyUy95qY7cWll7-bq_x92&export=download&confirm=t"
_URL = "https://www.googleapis.com/drive/v3/files/1YUYaLAoPBU1HyUy95qY7cWll7-bq_x92?alt=media&key=AIzaSyDVCNpmfKmJ0gPeyZ8YWMca9ZOKz0CWdgs"

local_dl_path = dl_manager().extract("/Users/salsabil.akbar/Downloads/bbcindonesia.zip")
# local_dl_path = dl_manager().download_and_extract(_URL)
# local_dl_path, *dump = download_file_from_google_drive("1YUYaLAoPBU1HyUy95qY7cWll7-bq_x92", "/Users/Salsabil.Akbar/.Cache/Huggingface/Datasets/Downloads/9791A8F977D9Dc519F8Ac8Bc87507E8399112Dad42714Fbd396Ecf072822Ea79")
# %%
path = "/Users/salsabil.akbar/.cache/huggingface/datasets/downloads/extracted/242e0fe43d225085958e3bda2e83a5dc774b3c31aea14d2ee7408b7f5f331c6b/EnViCorpora-master/wiki-alt/data.en"
with open(path, "r") as f:
    print(f.read())
# import io

# import google.auth
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaIoBaseDownload


# def download_file(real_file_id):
#   """Downloads a file
#   Args:
#       real_file_id: ID of the file to download
#   Returns : IO object with location.

#   Load pre-authorized user credentials from the environment.
#   TODO(developer) - See https://developers.google.com/identity
#   for guides on implementing OAuth2 for the application.
#   """
#   creds, _ = google.auth.default()

#   try:
#     # create drive api client
#     service = build("drive", "v3", credentials=creds)

#     file_id = real_file_id

#     # pylint: disable=maybe-no-member
#     request = service.files().get_media(fileId=file_id)
#     file = io.BytesIO()
#     downloader = MediaIoBaseDownload(file, request)
#     done = False
#     while done is False:
#       status, done = downloader.next_chunk()
#       print(f"Download {int(status.progress() * 100)}.")

#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     file = None

#   return file.getvalue()

# %%
import pandas as pd
from collections.abc import Iterable

def read_text_files(path: str, init_lines_to_skip:int=0, remove_empty_line: bool=True, strip_trailing_whitespace: bool=True):
    with open(path, "r") as f:
        data = [line.strip() for line in f.readlines()]

    # pre-processing steps based on args
    if init_lines_to_skip>0:
        data = data[init_lines_to_skip:]
    if remove_empty_line:
        data = [_data for _data in data if len(_data.strip()) != 0]
    if strip_trailing_whitespace:
        data = [_data.strip() for _data in data]
    
    return data

def strip_text_iterables(input: Iterable):
    if not isinstance(input, str):
        return list(map(str.strip, input))
    else:
        return input.strip()

def preprocess_cc_lab_file(cc_lab_file: str):
    if not cc_lab_file.endswith(".lab"):
        raise ValueError("The file isn't a .lab!")

    meta = ["start", "end", "phonemes"]
    raw_data = read_text_files(cc_lab_file)

    # final_data = []
    # for idx, line in enumerate(raw_data, start=1):
    #     data = line.split(" ")
    #     data_iter = strip_text_iterables(data)
    #     if data_iter is None:
    #         print(f"Missing lines found in {cc_lab_file} line {idx}!")
    #     else:
    #         final_data.append(dict(zip(meta, data_iter)))

    # data = pd.DataFrame(final_data).to_dict(orient="list")
    data = pd.DataFrame([dict(zip(meta, strip_text_iterables(_data.split(" ")))) for _data in raw_data]).to_dict(orient="list")
    return data

def folder_walk_file_grabber(folder_dir: str, ext: str=""):
    all_files = []
    for child_dir in os.listdir(folder_dir):
        _full_path = os.path.join(folder_dir, child_dir)
        if os.path.isdir(_full_path):
            all_files.extend(folder_walk_file_grabber(_full_path, ext))
        elif _full_path.endswith(ext):
            all_files.append(_full_path)
    
    return all_files

config_choices_folder_path = [
    ("PD", "U", "Clean"),
    ("PD", "U", "Office"),
    ("PD", "C", "Clean"),
    ("PD", "C", "Office")]

cnt_all = 1
cnt_occ = 0

for subfolder_path in config_choices_folder_path:
    root_path = "/Users/salsabil.akbar/Documents/lotus_folder_all_github"

    _lab_foldername = subfolder_path[1][0].upper() + subfolder_path[2][0].upper() + "lab"
    audio_all_paths = folder_walk_file_grabber(os.path.join(root_path, os.path.join(*subfolder_path), "Wav"), ".wav")
    cc_lab_folder = os.path.join(root_path, os.path.join(*subfolder_path), _lab_foldername)
    
    for audio_path in audio_all_paths:
        cnt_all += 1
        audio_id = audio_path.split("/")[-1][:-4]
        all_endtime = preprocess_cc_lab_file(os.path.join(cc_lab_folder, audio_id + ".lab"))["end"]
        lab_last_endtime = int(all_endtime[-1])
        # except ValueError as e:
        #     print(f"path: {os.path.join(cc_lab_folder, audio_id + '.lab')}, all endtime: {all_endtime}")
        #     raise e

        audio_class = Audio(sampling_rate=16000)
        dict_to_decode = audio_class.encode_example(audio_path)
        decoded_audio_ftr = audio_class.decode_example(dict_to_decode)

        if round(lab_last_endtime/len(decoded_audio_ftr["array"])) != 625:
            cnt_occ += 1
            _val = lab_last_endtime/len(decoded_audio_ftr["array"])
            print(f"File {audio_path} has annotated {_lab_foldername} ratio of {_val}")

print(f"Percentage occ: {cnt_occ/cnt_all*100}%")

# %%
from collections import Counter

def lotus_index_generator(root_folder: str):
    index_raw_data = read_text_files(f"{root_folder}/index.txt", init_lines_to_skip=5)

    # since in the index file we have many-to-one audio recording to the same identifier of sentence values in PDsen.txt
    # we will filter such occurrences (for now)
    _index_candidates = [data.split("\t")[2] for data in index_raw_data]
    valid_idx = [idx for idx, val in Counter(_index_candidates).items() if val == 1]

    # contains triplets of ("dataset number", "sequence number", "text identifier")
    metadata = ("dataset_number", "sequence_number")
    text_index_data = {
        data.split("\t")[2].strip():
            dict(zip(metadata, strip_text_iterables(data.split("\t")[:2])))
        for data in index_raw_data if data.split("\t")[2] in valid_idx}

    audio_index_data = {
        "_".join(values.values()): key for key, values in text_index_data.items()
    }

    return text_index_data, audio_index_data


id_1, id_2 = lotus_index_generator("/Users/salsabil.akbar/Documents/lotus_folder_all_github/Supplement")
# %%
from datasets import load_dataset
dset = load_dataset("audiofolder", data_dir = os.path.join(local_dl_path[0], "ceb"))
# %%
path = local_dl_path[0]

for child_path in os.listdir(path):
    print(child_path)
    print(any([not p.endswith(".wav") for p in os.listdir(os.path.join(path, child_path))]))

# %%
import os
def get_size(start_path = '.'):
    total_size = 0

    if not os.path.isdir(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

    return total_size

# sum_of_size = 0
# for key, file in local_dl_path.items():
#     size_per_dir = get_size(file)
#     sum_of_size += size_per_dir
#     print(f"total file size of {key}: {size_per_dir} byte(s)")

# print(f"total file size: {sum_of_size} byte(s)")

# %%
