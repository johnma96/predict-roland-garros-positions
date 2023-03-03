full_simulation:
ifdef start_year
ifdef end_year
	python main.py full_simulation start_year=$(start_year) end_year=$(end_year)
else
	python main.py full_simulation start_year=$(start_year)
endif
else ifdef end_year
	python main.py full_simulation end_year=$(end_year)
else
	python main.py full_simulation
endif

get_data:
ifdef start_year
ifdef end_year
	python main.py data_from_kaggle start_year=$(start_year) end_year=$(end_year)
else
	python main.py full_simulation start_year=$(start_year)
endif
else ifdef end_year
	python main.py data_from_kaggle end_year=$(end_year)
else
	python main.py data_from_kaggle
endif
