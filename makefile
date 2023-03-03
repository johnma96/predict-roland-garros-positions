# get_data:
# ifdef VAR1
# ifdef VAR2
# 	@echo "VAR1 is defined as $(VAR1) and VAR2 is defined as $(VAR2)"
# 	$(eval VAR3 := $(if $(filter VAR3=%,$(MAKECMDGOALS)), $(patsubst VAR3=%,%,$(filter VAR3=%,$(MAKECMDGOALS))), ))
# 	@echo "VAR3 is defined as $(if $(VAR3),$(VAR3),<not defined>)"
# else
# 	@echo "VAR1 is defined as $(VAR1) but VAR2 is not defined"
# endif
# else ifdef VAR2
# 	@echo "VAR2 is defined as $(VAR2) but VAR1 is not defined"
# else
# 	@echo "Neither VAR1 nor VAR2 is defined"
# endif

# get_data:
# ifdef owner_dataset
# ifdef dataset_name
# 	python main.py data_from_kaggle owner_dataset=$(owner_dataset) dataset_name=$(dataset_name)
# else
# 	@echo "owner_dataset is defined as $(owner_dataset) but dataset_name is not defined"
# endif
# else ifdef dataset_name
# 	@echo "dataset_name is defined as $(dataset_name) but owner_dataset is not defined"
# else
# 	python main.py data_from_kaggle
# endif

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