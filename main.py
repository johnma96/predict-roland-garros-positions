import os
import sys
import numpy as np
from predict_roland_garros_positions import *


def run_data_from_kaggle(owner_dataset: str = "gmadevs", 
                         dataset_name: str = "atp-matches-dataset",
                         start_year: str = '2000', 
                         end_year: str = '2017', 
                         **kwargs):
    
    # Path to dowload dataset
    try:
        path_to_save = kwargs["path_to_save"]
        kwargs.pop("path_to_save")

        if not (path_to_save[-1] == os.sep):
            path_to_save = path_to_save + os.sep
    except:
        path_to_save = None

    if start_year == '2000' and end_year == '2017':
        dowload_kaggle_dataset(
            owner_dataset=owner_dataset,
            dataset_name=dataset_name,
            path_to_save=path_to_save,
            **kwargs
        )
    else:
        years = np.arange(int(start_year), int(end_year)+1)
        start_name = 'atp_matches_'
        for year in years:
            dowload_kaggle_dataset(
                owner_dataset=owner_dataset,
                dataset_name=dataset_name,
                file_name=f"{start_name}{year}"
                path_to_save=path_to_save,

            )


def run_clean_data():
    pass


def run_make_features():
    pass


def run_full_simulation():
    pass


if __name__ == "__main__":

    process_to_run = {
        "full_simulation": run_full_simulation,
        "data_from_kaggle": run_data_from_kaggle,
        "clean_data": run_clean_data,
        "make_features": run_make_features,
    }

    # Check workflow execution arguments
    if len(sys.argv) < 2:
        msg = "You must pass at least one argument to run the entire simulation or any part of it. Valid arguments are:"  # /
        # "full_simulation, restart_data, data_from_kaggle, clean_data, make_features"
        raise OSError(msg)
    try:
        process = process_to_run[sys.argv[1]]
    except KeyError:
        raise KeyError("This process does not exist")
    

    


    if sys.argv[1] == "full_simulation":
        process()

    elif sys.argv[1] == "data_from_kaggle":
        if len(sys.argv) >= 3:
            arguments = {arg.split("=")[0]: arg.split("=")[1] for arg in sys.argv[2:]}
            process(**arguments)
        else:
            process()

    elif sys.argv[1] == "clean_data":
        print(4)
        process()
    elif sys.argv[1] == "make_features":
        print(5)
        process()
