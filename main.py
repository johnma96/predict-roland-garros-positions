# Simplifies the execution of one or more of the predict-roland-garros-positions scripts
# For instace, here we are reading different types of source data

from utils import LoadData

load = LoadData()

# Read excel in raw folder within data folder
data_excel = load.from_excel(data_type='raw', file_name='dummy_data2.xlsx')

# Read csv in data folder
data_csv = load.from_csv(file_name="dummy_data.csv")

print('\n'+'-'*10+' Data from excel '+'-'*10)
print(data_excel.head())
print('\n'+'-'*10+' Data from csv '+'-'*10)
print(data_csv.head())