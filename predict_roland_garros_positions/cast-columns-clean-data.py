import os
import pandas as pd
import numpy as np
import glob
from utils import LoadData, AbsPaths
from datapackage import Package

def select_columns(file_name = "atp_matches_historic", cols:str=['tourney_id','round','winner_id',
                                                                 'winner_rank', 'winner_rank_points', 'loser_id',
                                                             'loser_rank', 'loser_rank_points','score','minutes'],
                   path_file_name=None, path_to_save = None):
    if path_file_name is None:
        path_file_name=AbsPaths().get_abs_path_folder(folder_name="interim")+ f"{file_name}" + ".csv"
    data=pd.read_csv(path_file_name)
    data=data.loc[:,cols]
    return data

def  tourney_table(file_name:str=None, path_to_save = None):
    data=select_columns(cols=['tourney_id', 'tourney_name', 'surface','tourney_date']).drop_duplicates()
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name='interim')
    if file_name is None:
        file_name= 'TourneyTable'
    data.to_csv(path_to_save + f"{file_name}.csv", index=False)
    
def GetAuxiliarDataHub(link='https://datahub.io/sports-data/atp-world-tour-tennis-data/datapackage.json'):
    package = Package(link)
    return package

def SaveAuxiliarDataHub(path_to_save, table_to_extract):
    package=GetAuxiliarDataHub()
    id_players=package.resource_names.index(table_to_extract)
    Data=pd.DataFrame(package.resources[id_players].read(), columns=package.resources[id_players].headers)
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name='external')
    Data.to_csv(path_to_save + f"{table_to_extract}.csv", index=False)

    
def OpenAuxiliarData(name:str='player_overviews_unindexed', path:str=None):
    if path is None:
        path= AbsPaths().get_abs_path_folder(folder_name='external')
    if not os.path.exists(path+ f"{name}.csv"):
        auxiliarData=SaveAuxiliarDataHub(path, name)
    AuxiliarData=pd.read_csv(path+ f"{name}.csv")
    return AuxiliarData


def PlayerTable(file_name:str=None, path_to_save = None):
    data=select_columns(cols=['tourney_date','winner_id','winner_name','winner_ht','winner_age','winner_ioc']).rename(columns={'winner_id':'id','winner_name':'name','winner_ht':'ht', 'winner_age':'age','winner_ioc':'ioc'})                          
    data2=select_columns(cols=['tourney_date','loser_id','loser_name','loser_ht','loser_age','loser_ioc']).rename(columns={'loser_id':'id','loser_name':'name','loser_ht':'ht', 'loser_age':'age','loser_ioc':'ioc'})
    players=pd.concat([data, data2]).drop_duplicates(subset=['id','name','ht','ioc']).reset_index()    
    for i in players.index:
        players.loc[i,'birthdate']=(pd.to_datetime(players.loc[i,'tourney_date'], format='%Y%m%d')-pd.Timedelta(str(players.loc[i,'age'])+'Y')).strftime('%Y-%m-%d')
    
    players=AddCharacteristic_PlayerTable(players, 'weight_kg')
    players=ReviewHt_PlayerTable(players)
    
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name='interim')
    if file_name is None:
        file_name= 'PlayerTable'
    players.loc[:,['id','name','birthdate','weight_kg','ht','ioc']].to_csv(path_to_save + f"{file_name}.csv", index=False)

def AddCharacteristic_PlayerTable(players, characteristic):
    AuxiliarData=OpenAuxiliarData()
    AuxiliarData.loc[:,'name']=AuxiliarData.loc[:,'first_name'].str.replace('-',' ').str.replace('.','')+' '+AuxiliarData.loc[:,'last_name'].str.replace('-',' ').str.replace('.','').str.title()
    for i in players.index:
        if len(AuxiliarData[AuxiliarData.name==players.loc[i,'name']][AuxiliarData.flag_code==players.loc[i,'ioc']][characteristic])>0:
            players.loc[i, characteristic]=AuxiliarData[AuxiliarData.name==players.loc[i,'name']][AuxiliarData.flag_code==players.loc[i,'ioc']][characteristic].values[0] 
        else:
            try:
                players.loc[i, characteristic]=AuxiliarData[AuxiliarData.name==players.loc[i,'name']][characteristic].values[0] 
            except:pass
    return players

def ReviewHt_PlayerTable(players):
    AuxiliarData=OpenAuxiliarData()
    AuxiliarData.loc[:,'name']=AuxiliarData.loc[:,'first_name'].str.replace('-',' ').str.replace('.','')+' '+AuxiliarData.loc[:,'last_name'].str.replace('-',' ').str.replace('.','').str.title()
    for i in players[players.ht.isna()].index:
        if len(AuxiliarData[AuxiliarData.name==players.loc[i,'name']][AuxiliarData.flag_code==players.loc[i,'ioc']]['height_cm'])>0:
            players.loc[i, 'ht']=AuxiliarData[AuxiliarData.name==players.loc[i,'name']][AuxiliarData.flag_code==players.loc[i,'ioc']]['height_cm'].values[0] 
        else:
            try:
                players.loc[i, 'ht']=AuxiliarData[AuxiliarData.name==players.loc[i,'name']]['height_cm'].values[0] 
            except:pass
    players.loc[players.ht.isna(),'ht']=players.ht.mean()
    return players



def NanColumns(data):
    NanCols=data.keys()[data.isna().sum()>0]
    return NanCols

def CleanNaNData(data, Nan):
    if 'minutes' in Nan:
        data=CleanMinutes(data)
    Nan=Nan.drop('minutes')
    #data=CleanProperties(data, Nan)
    return data

def CleanMinutes(data):
    data.loc[data.score=='W/O','minutes']=0
    data.loc[data.minutes.isna(), 'minutes']=data.loc[data.minutes.isna(),'score'].str.split(' ').apply(lambda x: len(x) * 35)
    return data

def CleanProperties(data, Nan):
    for j in Nan:
        for k in data[data[j].isna()].index:
            if len(data[data[j.split('_')[0]+'_id']==data.loc[k,j.split('_')[0]+'_id']].dropna())>0:
                try:
                    data.loc[k,j]=data.loc[:k-1,:][data[j.split('_')[0]+'_id']==data[data[j].isna()][j.split('_')[0]+'_id'].values[0]].dropna().iloc[-1][j]
                except:
                    data.loc[k,j]=data.loc[k+1:,:][data[j.split('_')[0]+'_id']==data[data[j].isna()][j.split('_')[0]+'_id'].values[0]].dropna().iloc[-1][j]
            else:
                data.loc[k,j]=round(data.loc[:,'loser_rank'].mean(),0)
    return data

def TableMatches(file_name:str=None, path_to_save = None):
    data=select_columns()
    Nan=NanColumns(data)
    data=CleanNaNData(data, Nan)
    data=CleanProperties(data,Nan)
    if path_to_save is None:
        path_to_save = AbsPaths().get_abs_path_folder(folder_name='interim')
    if file_name is None:
        file_name= 'MatchesTable'
    data.to_csv(path_to_save + f"{file_name}.csv", index=False)
    
