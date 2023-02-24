advance:
ifdef n_weeks
	python3 advance.py $(n_weeks)
else
	python3 advance.py
endif


restart:
ifdef restart_date
	python3 restart.py $(restart_date)
else
	python3 restart.py 
endif


all: restart_data get_data_kaglee clean_data generate_features

get_data:
ifdef dataset_name
ifdef owner_dataset
	python get_data_from_kaggle.py 


restart_data:
