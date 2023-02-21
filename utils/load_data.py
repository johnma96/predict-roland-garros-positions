import warnings
import pandas as pd

from .make_connection import MakeConnection
from .read_sql_file import read_sql


class LoadData(MakeConnection):
    """
    Class to load data in a Pythonic way, this from different information
    sources:
        - Data in the data subfolder.
        - Called from some RBDM such as BigQuery, MySQL, Postgres, etc.

    Attributes
    ----------
    file_credentials_path: str
        Absolute path to the .json credentials file to BigQuery. Only if the
        with_gbq() method is used. Inherited from MakeConnection class
    credentials_bq: service_account
        Connection object to BigQuery using a service account. Only if the
        with_gbq() method is used. Inherited from MakeConnection class
    max_level: int
        Maximum level of depth within the package, in which it seeks to establish
        the absolute paths. Inherited from the AbsPaths class

    Methods
    -------
    from_BigQuery(query, path_credentials=None, name_file=None,
                project_id='dolphin-prod')
        Read data directly from GCP BigQuery Service
    from_csv(path=None, type=None, name_file=None, **kwargs)
        Read .csv files from sub-subfolders within data subfolder
    from_excel(path=None, type=None, name_file=None, **kwargs)
        Read excel files from sub-subfolders within data subfolder
    """

    def __init__(
        self,
        file_credentials_path: str = None,
        file_credentials_name="credentials_bq.json",
        type_rdbms: str = "bigquery",
        max_level: int = 5,
    ) -> None:

        # Set max depth to handle routes
        super().__init__(max_level=max_level)

    def from_mysql(self): pass 

    def from_psql(self): pass

    def from_csv(
        self,
        file_path: str = None,
        data_type: str = None,
        file_name: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Call data using pandas.read_csv method. To get data directly from data
        folder just select the type_data of folder and set file's name.

        You can pass all arguments of pandas native method.

        Parameters
        ----------
        file_path : str, optional
            File path, by default None. If None, the file is expected to be in
            the data subfolder
        data_type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default
            None. Keep None if you provide a path to the file
        file_name : str, optional
            Name of the file to be searched within the data folder, by default
            None
        **kwargs :
            Additional keywords passed to pandas.read_excel() method

        Returns
        -------
        pd.DataFrame
            Dataframe with loaded data
        """

        file_path = self.__build_path(
            file_path=file_path, data_type=data_type, file_name=file_name
        )

        return pd.read_csv(filepath_or_buffer=file_path, **kwargs)

    def from_excel(
        self,
        file_path: str = None,
        data_type: str = None,
        file_name: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Call data using pandas.read_excel method. To get data directly from data
        folder just select the type of folder and set file's name.

        You can pass all arguments of pandas native method.

        Parameters
        ----------
        file_path : str, optional
            File path, by default None. If None, the file is expected to be in
            the data subfolder
        data_type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default
            None. Keep None if you provide a path to the file
        file_name : str, optional
            Name of the file to be searched within the data folder, by default
            None
        **kwargs :
            Additional keywords passed to pandas.read_excel() method

        Returns
        -------
        pd.DataFrame
            Dataframe with loaded data
        """

        file_path = self.__build_path(
            file_path=file_path, data_type=data_type, file_name=file_name
        )

        return pd.read_excel(io=file_path, **kwargs)

    def __build_path(
        self, file_path: str = None, data_type: str = None, file_name: str = None
    ) -> str:
        """
        Build the path to find the file in which the data to be loaded is
        located.

        Parameters
        ----------
        file_path : str, optional
            File path, by default None. If None, the file is expected to be in
            the data subfolder
        data_type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default
            None. None indicates to look for the file in any data subfolder
        file_name : str, optional
            Name of the file to be searched within the data folder, by default
            None

        Returns
        -------
        str
            File path passed by the user or absolute file path within the data
            subfolder

        Raises
        ------
        FileNotFoundError
            if the requested file exists in a different path than the data_type
            passed
        """
        
        if file_path is None:
            file_path = self.get_abs_path_file(file_name=file_name)

            # Case in which are multiple files with same name in the package
            if isinstance(file_path, list):
                try:
                    file_path_end = [path for path in file_path if data_type in path][0]
                except:
                    msg = """File wasn't found within {} folder. Was found in other paths: \n{}""".format(
                        data_type, "\n".join(file_path)
                    )
                    raise FileNotFoundError(msg)

                file_path = file_path_end

            # The file isn't within the data_type folder gave
            if (data_type is not None) and (not(data_type in file_path)):
                    print(data_type)
                    msg = """File wasn't found within {} folder. Was found in other paths: \n{}""".format(
                        data_type, file_path
                    )
                    raise FileNotFoundError(msg)
        
        return file_path