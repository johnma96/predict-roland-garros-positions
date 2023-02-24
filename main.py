import os
import sys
from predict_roland_garros_positions import *


def run_data_from_kaggle(
    owner_dataset: str = "gmadevs", dataset_name: str = "atp-matches-dataset", **kwargs
):
    try:
        path_to_save = kwargs["path_to_save"]
        kwargs.pop("path_to_save")

        if not(path_to_save[-1] == os.sep):
            path_to_save = path_to_save + os.sep

    except:
        path_to_save = None
    dowload_kaggle_dataset(
        owner_dataset=owner_dataset,
        dataset_name=dataset_name,
        path_to_save=path_to_save,
        **kwargs
    )


def run_clean_data():
    pass


def run_make_features():
    pass


def run_all():
    pass


if __name__ == "__main__":
    process_to_run = {
        "full_simulation": run_all,
        "data_from_kaggle": run_data_from_kaggle,
        "clean_data": run_clean_data,
        "make_features": run_make_features,
    }

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
    elif sys.argv[1] == "restart_data":
        print(2)
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
