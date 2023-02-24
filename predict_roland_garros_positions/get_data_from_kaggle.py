import os
from utils import AbsPaths
from zipfile import ZipFile
from kaggle.api.kaggle_api_extended import KaggleApi

def restart_dataset(path, dataset_name):
    try:
        zip_file = dataset_name+'.zip'
        zf = ZipFile(file=path+zip_file)
        list_files_zip = zf.namelist()
        zf.close()
        for filename in [*[path+l for l in list_files_zip], path+zip_file]:
            os.remove(filename)
    except: pass
    

def dowload_kaggle_dataset(owner_dataset:str , dataset_name:str , 
                            path_to_save:str = None, uncompress_dataset = True,
                            **kwargs):
    """
    Download a complete dataset or parts of a dataset using the kaggle API. You 
    need to dowload credentials and put it at ~/.kaggle/kaggle.json on Linux, OSX, 
    and other UNIX-based operating systems, and at C:\\Users<Windows-username>.kaggle\\kaggle.json 
    on Windows To get more information about de API please read 
    https://www.kaggle.com/docs/api 

    Parameters
    ----------
    owner_dataset : str
        Kaglee user who owns the dataset
    dataset_name : str
        Name of the dataset to be downloaded
    path_to_save : str, optional
        Path to save the downloaded .zip file, if None the file is downloaded in 
        the same path as the executable., by default None
    """
    
    # Connect to kaggle api. You need to have kaggle credentials in the path 
    # 'C:\Users\<username>\.kaggle\'
    
    
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name='raw')

    # Remove .zip file
    restart_dataset(path=path_to_save, dataset_name=dataset_name)
    
    dataset = owner_dataset + '/' + dataset_name

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset=dataset, path=path_to_save, **kwargs)

    if uncompress_dataset:
        uncompress_zip_file(file_path=path_to_save+dataset_name+'.zip')


def uncompress_zip_file(file_path: str = None):
    """
    Unzip a .zip file

    Parameters
    ----------
    file_path : str, optional
        Absolute path of the file to be decompressed. If None, a filename must 
        be supplied that is found within the repository., by default None
    file_name : str, optional
        File name .zip, by default None
    
    Raises
    ------
    FileNotFoundError
        If no information is provided for unzipping a file
    """
    if (file_path is None):
        msg = 'You must provide a file path or file name'
        raise FileNotFoundError(msg)
    
    folder_file = os.sep.join(file_path.split(os.sep)[:-1])
    
    zf = ZipFile(file=file_path)

    # Extracted data is saved in the same directory of the .zip file
    zf.extractall(path=folder_file)
    zf.close()