from utils import AbsPaths
import os
import pandas as pd
import glob
import re


def get_list_files(start_file_name = "atp_matches", path = None) -> list:
    if path is None:
        path = AbsPaths().get_abs_path_folder(folder_name="raw")

    return sorted(glob.glob(path + f"{start_file_name}" + "*.csv"))

def validate_year(list_files, year:str, index):
    if index not in [0,-1]:
        raise IndexError("You need provide 0 (start) or -1 (end)")
    if year is None:
        file = list_files[index]
        year = "/".join(re.findall(r"\d+",file.split(os.sep)[-1]))

    else:
        file = [f for f in list_files if year in f]

        if len(file) == 0:
            raise FileNotFoundError("You need provide an available start year")
        
        else:
            file = file[0]

    return file, year

def join_tables(start_year:str = None, start_file_name: str = "atp_matches", end_year:str = None, 
                path_read:str = None, path_to_save:str = None):
    if path_read is None:
        path_read = AbsPaths().get_abs_path_folder(folder_name="raw")
    list_files = get_list_files(start_file_name = start_file_name, path = path_read)

    start_file, start_year = validate_year(list_files=list_files, year=start_year, index = 0)
    end_year = validate_year(list_files=list_files, year=end_year, index = -1)[1]

    cols = pd.read_csv(start_file,sep=",", nrows=1).columns
    data = pd.read_csv(start_file,sep=",", usecols=cols)

    for file in list_files:
        if file == start_file:
            pass
        year_file = "/".join(re.findall(r"\d+",file.split(os.sep)[-1]))
        # print(start_year, end_year, year_file)
        if (year_file > start_year) and (year_file <= end_year):

            cols_df = pd.read_csv(file,sep=",", nrows=1).columns
            df = pd.read_csv(file, sep=',', usecols=cols_df)
            data = pd.concat([data, df],ignore_index=True)
        
        data = data[data["tourney_level"] == "G"].reset_index(drop=True)
        
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name="interim")
    
    data.to_csv(path_to_save + f"{start_file_name}_historic.csv", index=False)

    # return data

    