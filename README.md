# predict-roland-garros-positions

By: John Montoya (jmmontoyaz@unal.edu.co), Sthepany Cordoba (scordobay@unal.edu.co), Camilo Cabrera (cacabreram@unal.edu.co), Yuliany Rojas (yrojasl@unal.edu.co) and Mateo Ramirez (anramirezlo@unal.edu.co)

End to end model to predict the positions of the most important ATP clay court tournament. This model is develop within the framework of the course "Productos de datos" offered in the Analytics Specialization of the Universidad Nacional de Colombia - Sede Medellín.

# About the structure

This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/) and [reproducible-model](https://github.com/cmawer/reproducible-model) repository.

Check this [post](https://www.jeremyjordan.me/ml-projects-guide/) by Jeremy Jordan for get guidelines on managing ML projects.

Other resources.
- Books
    - [Clean Machine Learning Code](https://leanpub.com/cleanmachinelearningcode)

## Repo structure 

```
├── LICENSE
|
├── README.md                        <- You are here
|
├── credentials/                     <- Folder to store credentials files
|
├── data/                            <- Folder that contains data used or generated
│   ├── external/                    <- Data from third parties (external to the core company of the project)
│   ├── interim/                     <- Data in an intermediate state of processing
│   ├── processed/                   <- Data fully processed and ready to be used in modeling
│   └── raw/                         <- The original, immutable data dump
|
├── docs/                            <- A default Sphinx project; see sphinx-doc.org for details
|
├── models/                          <- Trained and serialized models, model predictions, or model summaries
|
├── notebooks/                       <- Jupyter notebooks. Naming convention is a number (for ordering),
│   |                                   the creator's initials, and a short `-` delimited description, e.g.
│   |                                   `1.0-jqp-initial-data-exploration`.
│   ├── delivered/                   <- Notebooks delivered by third parties (external to the core company of the project)
│   └── develop/                     <- Noteboos for EDA development, modeling, configuration, etc.
|
├── references/                      <- Data dictionaries, manuals, and all other explanatory materials.
|
├── reports/                         <- Generated analysis as HTML, PDF, LaTeX, etc.
│   ├── figures/                     <- Generated graphics and figures to be used in reporting
│   ├── pdfs/                        <- PDF files for reporting
│   └── power_bi/                    <- Reports and dashboards using the power bi tool
|
├── src/                             <- Source code for use in this project.
│   ├── __init__.py                  <- Makes src a Python module
│   ├── archive/
│   ├── evaluate_model.py            <- Scripts to evaluate the performance of models
│   ├── generate_features.py         <- Scripts to turn raw data into features for modeling
│   ├── postprocess.py               <- Scripts to turn raw data into features for modeling
│   └── predict_model.py             <- Scripts to use trained models to make predictions
│   ├── score_model.py               <- Script to calculate metrics from the trained model
│   ├── sql/                         <- Folder to store .sql files used at some point in the modeling process                            
│   └── train_model.py               <- Scripts to train models 
|
├── utils/
│   ├── __init__.py
│   ├── absolute_paths.py            <- Module for handling absolute path
│   ├── auditory.py                  <- Module for process audit management. The processes are audited in a MariaDB type database
│   └── load_data.py                 <- Module for reading data from different RDBMS
|
├── environment.yml                  <- The environment file for reproducing the analysis environment, e.g.
│                                        generated with `conda env export --from-history --file environment.yml`
|
├── main.py                          <- Main file to orchestrate re-trains and execution of source code stored in src folder
|
├── requirements.txt                 <- The requirements file for reproducing the analysis environment, e.g.
│                                        generated with `pip freeze > requirements.txt`
|
├── .gitignore                       <- Gitignore file 
```

references folder: Place here pdf files or other bibliographic sources that have allowed to reach the selection of the model or the understanding of some algorithm that you want to keep.

Consider ignoring some files when they are binary or large

noteboosk folder: This folder is intended to store all the notebooks you create to explore, test, train, etc. models and code in general. Naming convention is the suggest by [Cookiecutter](https://drivendata.github.io/cookiecutter-data-science/#directory-structure): 
- A number (for ordering), the creator's initials, and a short `-` delimited description, e.g. `1.0-jqp-initial-data-exploration`.

models folder: Trained and serialized models, model predictions, or model summaries

docs folder: A default Sphinx project; see sphinx-doc.org for details.

data folder: Use this folder to store your data. Here there's a python's file for get absolute path of this folder.
Currently there are 5 folders for store data: raw (for raw data from the company), interim (for data with some modification but not completly), processed (for manipulated data in final version) and external(data from third parties).

# Run data simulation

Commands to run stages or full simulation to get data, clean it and use it to make features that will be used to train models

## Just get data
In the root of the repository use 
```bash
make get_data
```
Or one level before the repo use
```bash
make -C predict-roland-garros-positions/ get_data
```

## Clean data dowloaded
In the root of the repository use
```bash 
make clean_data
```
Or one level before the repo use
```bash
make -C predict-roland-garros-positions/ clean_data
```

## Make features to train models using clean data
In the root of the repository use
```bash 
make make_features
```
Or one level before the repo use
```bash
make -C predict-roland-garros-positions/ make_features
```

## Run full simulation (dowload data, clean data and make features)
In the root of the repository use
```bash 
make full_simulation
```
Or one level before the repo use
```bash
make -C predict-roland-garros-positions/ full_simulation
```
