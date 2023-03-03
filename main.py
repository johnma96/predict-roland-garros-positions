import os
import sys
import warnings
import numpy as np
from utils import LoadData, AbsPaths
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
            print(year)
            dowload_kaggle_dataset(
                owner_dataset=owner_dataset,
                dataset_name=dataset_name,
                file_name=f"{start_name}{year}",
                path_to_save=path_to_save,

            )

    warnings.filterwarnings('ignore')


def run_clean_data(start_year="2000", end_year="2017"):
    # Join tables
    join_tables(start_year = start_year, end_year=end_year)

    # Clean data
    PlayerTable()
    TableMatches()
    warnings.filterwarnings('ignore')

def run_make_features(clean_data='MatchesTable.csv', clean_dataplayers='PlayerTable.csv'):

    # Load data
    df = LoadData().from_csv(file_name=clean_data)
    players=LoadData().from_csv(file_name=clean_dataplayers)

    # Built features
    built_rdbms(data=df, players=players)
    warnings.filterwarnings('ignore')


def run_full_simulation(start_year: str = '2000', end_year: str = '2017'):
    run_data_from_kaggle(start_year=start_year, end_year=end_year)
    run_clean_data(start_year=start_year, end_year=end_year)
    run_make_features()
    warnings.filterwarnings('ignore')


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
        if len(sys.argv) >= 3:
            arguments = {arg.split("=")[0]: arg.split("=")[1] for arg in sys.argv[2:]}
            
            if "end_year" in arguments.keys():
                end_year = arguments['end_year']

                if int(end_year) > 2017:
                    arguments['end_year'] = str(2017)
                    warnings.warn(message="Available data just to 2017")
            
            if "start_year" in arguments.keys():
                start_year = arguments['start_year']
                if int(start_year) < 2000:
                    arguments['start_year'] = str(2000)
                    warnings.warn(message="Available data just since 2000")

            process(**arguments)
        else:
            process()

    elif sys.argv[1] == "data_from_kaggle":
        if len(sys.argv) >= 3:
            arguments = {arg.split("=")[0]: arg.split("=")[1] for arg in sys.argv[2:]}
            
            if "end_year" in arguments.keys():
                end_year = arguments['end_year']

                if int(end_year) > 2017:
                    arguments['end_year'] = str(2017)
                    warnings.warn(message="Available data just to 2017")
            
            if "start_year" in arguments.keys():
                start_year = arguments['start_year']
                if int(start_year) < 2000:
                    arguments['start_year'] = str(2000)
                    warnings.warn(message="Available data just since 2000")

            process(**arguments)
        else:
            process()

    elif sys.argv[1] == "clean_data":
        
        if len(sys.argv) >= 3:
            arguments = {arg.split("=")[0]: arg.split("=")[1] for arg in sys.argv[2:]}
            
            if "end_year" in arguments.keys():
                end_year = arguments['end_year']

                if int(end_year) > 2017:
                    arguments['end_year'] = str(2017)
                    warnings.warn(message="Available data just to 2017")
            
            if "start_year" in arguments.keys():
                start_year = arguments['start_year']
                if int(start_year) < 2000:
                    arguments['start_year'] = str(2000)
                    warnings.warn(message="Available data just since 2000")

            process(**arguments)
        else:
            process()

    elif sys.argv[1] == "make_features":
       process()