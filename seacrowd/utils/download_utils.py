import os
import logging

def download_data_from_gdrive(file_id: str, dataloader_name: str, filename: str="", file_ext: str="zip") -> str:
    '''This Python function downloads data from Google Drive using the `gdown` library and saves it to a
    specified directory. It will be stored on {seacrowd_repo_root_path}/data/{dataloader_name}/{filename}.{file_ext}
    The {seacrowd_repo_root_path}/data is already being ignored in .gitignore
    
    Parameters
    ----------
    file_id : str
        Google Drive file ID, used to construct the download URL.
    dataloader_name : str
        dataloader name which it's used (for target folder path creation).
    filename : str, optional
        file name of the downloaded file. If empty, it will use the args `dataloader_name`
    file_ext : str, optional
        file_ext of the downloaded file, defaults to "zip" (w/o any dot)
    
    Returns
    -------
        local path to the downloaded file.
    
    '''
    try:
        import gdown
    except ImportError:
        raise ImportError("Please install `gdown` to enable downloading data from google drive.")

    # Download from Google drive
    URL = f"https://drive.google.com/uc?id={file_id}"
    output_dir = os.path.join(os.getcwd(), "data", dataloader_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if filename == "" or filename is None:
        filename = dataloader_name
    output_file = output_dir + f"/{filename}.{file_ext}"
    if not os.path.exists(output_file):
        gdown.download(URL, str(output_file), fuzzy=True)
    else:
        logging.info(f"File already downloaded in {str(output_file)}")

    return output_file
