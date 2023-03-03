from utils import LoadData, AbsPaths
import pandas as pd

def organize_data_type(data: pd.DataFrame, data_type: str):
    df = data.copy()

    cols = [
        "tourney_id",
        "tourney_name",
        "surface",
        "tourney_date",
        f"{data_type}_id",
        f"{data_type}_rank",
        "minutes",
        "round",
    ]

    rounds = df["round"].unique()
    change_round = {
        r: int(r.split("R")[-1])
        if r.startswith("R")
        else 4
        if r.startswith("Q")
        else 2
        if r.startswith("S")
        else 1
        if r.startswith("F")
        else 0
        for r in rounds
    }
    df["round"].replace(change_round, inplace=True)

    rename_cols = {col: col.split("_")[-1] for col in cols if col.startswith(data_type)}
    df["tourney_date"] = pd.to_datetime(df["tourney_date"])

    types = {
        "tourney_id": str,
        "tourney_name": str,
        "surface": str,
        "id": str,
        "rank": float,
        "minutes": float,
    }

    return df.loc[:, cols].rename(columns=rename_cols).astype(types)

def organize_original_data(data):
    original_data = data.copy()

    original_data.tourney_date = pd.to_datetime(
        original_data.tourney_date.astype(int), format="%Y%m%d"
    )

    winner_df = organize_data_type(data=original_data, data_type="winner")
    winner_df["won"] = 1
    loser_df = organize_data_type(data=original_data, data_type="loser")
    loser_df["won"] = 0

    final_df = pd.concat([winner_df, loser_df])
    final_df.set_index("tourney_date", inplace=True)
    return final_df

def calc_historical_features(row, history):
    df = history.loc[
        (history["tourney_name"] == row["tourney_name"])
        & (history["id"] == row["id"]),
        ["tourney_name", "id", "won", "minutes"],
    ].copy()

    agg_dictionary = {"won": ["count", "sum"], "minutes": "sum"}

    df = df.groupby(by=["tourney_name", "id"]).agg(agg_dictionary).reset_index()
    df.columns = df.columns.map(lambda x: "".join(map(str, x)))
    df.rename(
        columns={"woncount": "pj", "wonsum": "pg", "minutessum": "minutes_played"},
        inplace=True,
    )
    df["pp"] = df["pj"] - df["pg"]

    return df


def make_features(data: pd.DataFrame, players:pd.DataFrame, start_year: int = None, end_year: int = None):
    
    # Organize data
    organized_data = organize_original_data(data=data)

    if start_year is None:
        start_year = organized_data.index.year.min()
    if end_year is None:
        end_year = organized_data.index.year.max()

    final_data = pd.DataFrame()

    # Calculate features for each year
    for year in range(start_year, end_year + 1):
        print(year)

        # Current features
        current_tourneys = organized_data.sort_index().loc[str(year)].reset_index()


        unique_cols = [
            "tourney_name",
            "tourney_date",
            "surface",
            "tourney_id",
            "id"
        ]

        group = current_tourneys.groupby(by=unique_cols).agg(
            {"rank": "max", "round": ["min"]}
        )

        current_features = group.reset_index()
        current_features.columns = current_features.columns.droplevel(1)

        # Historical features
        history = organized_data.sort_index().loc[: str(year - 1)]
        historical_features = pd.concat(
            current_features.apply(
                lambda row: calc_historical_features(row, history), axis=1
            ).to_list(),
            ignore_index=True,
        )

        full_features = current_features.merge(historical_features, how="left", on=["tourney_name", "id"])
        full_features = full_features.fillna(
            value={"pj": 0, "pg": 0, "pp": 0, "minutes_played": 0}
        )
        full_features["year"] = year        
        
        

        final_data = pd.concat([final_data, full_features], ignore_index=True)
        
        for i in set(final_data.id):
            final_data.loc[final_data.id == i, "ht"] = players[players.id == float(i)]["ht"].values[0]
            final_data.loc[final_data.id == i, "wg"] = players[players.id == float(i)]["weight_kg"].values[0]
            final_data.loc[final_data.id == i, "birthdate"] = players[players.id == float(i)]["birthdate"].values[0]
        
        final_data.birthdate = pd.to_datetime(final_data.birthdate)
        final_data.loc[:,"age"] = final_data.loc[:,"year"] - final_data.loc[:,"birthdate"].dt.year

        # Sort output data
        out_cols = [
            "tourney_date",
            "tourney_name",
            "surface",
            "id",
            "ht",
            "wg",
            "age",
            "rank",
            "minutes_played",
            "pj",
            "pg",
            "pp",
            "round",
        ]

    processed_path = AbsPaths().get_abs_path_folder(folder_name="processed")

    return final_data.loc[:, out_cols]


def built_rdbms(data, players,
        file_name:str = "operational_rdbms"):
    
    start_year = data['tourney_id'].str.split('-', expand=True)[0].astype(int).min()
    end_year = data['tourney_id'].str.split('-', expand=True)[0].astype(int).max()
    
    file_name = file_name + ".csv"
    processed_path = AbsPaths().get_abs_path_folder(folder_name="processed")
    try:
        data_current_features = pd.read_csv(processed_path + file_name, parse_dates="tourney_date")
        last_year = data_current_features.tourney_date.dt.year.max()
        data_new_features = make_features(data=data, players=players,
            start_year=last_year + 1, end_year = end_year)
        features = pd.concat([data_current_features, data_new_features], ignore_index=True)
    except:
        features = make_features(data=data, players=players,
            start_year=start_year, end_year=end_year)

    print('\n')    
    print(features.head(2))
    print('.................'*10)
    print(features.tail(2))

    features.to_csv(processed_path + "operational_rdbms.csv", index=False)


    



