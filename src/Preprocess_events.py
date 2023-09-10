import csv 
import os
import tqdm
import numpy as np
import pandas as pd
from kloppy import statsbomb
import warnings
warnings.filterwarnings(action='ignore')



def preprocess_event(competition_id, eventtype = None):

    competitions = pd.read_json("https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json")
    competition_dict = {competitions.loc[i, 'competition_id'] : competitions.loc[i, 'competition_name']  for i in range(len(competitions))}
 
    match_dict = {}
    for i in competition_id:
        t_list = []
        if str(i) not in os.listdir('data/matches'):
            continue

        for j in os.listdir('data/matches/{}'.format(i)):
            t_df = pd.read_json('data/matches/{}/{}'.format(i, j))
            if 'match_id' in t_df.columns:
                t_list = t_list + t_df.match_id.to_list()
        match_dict[i] = t_list

    event_list = os.listdir('data/events/')

    event_dict = {}
    for k, v in match_dict.items():
        event_dict[k] = []
        for i in v:
            if str(i) + '.json' in event_list:
                event_dict[k].append(i)


    for k, v in event_dict.items():
        df_list = []
        idx = 0
        for i in tqdm.tqdm(v, desc='{}'.format(competition_dict[k])):
            dataset = statsbomb.load_open_data(str(i), coordinates="statsbomb", event_types=eventtype)
            t_df = dataset.to_df()

            team_dict = {i.team_id : i.name  for i in dataset.metadata.teams}
            player_dict = {i.player_id : i.name for i in dataset.metadata.teams[0].players}
            t_player_dict = {i.player_id : i.name for i in dataset.metadata.teams[1].players}
            player_dict.update(t_player_dict)

            t_df['ball_owning_team'] = [team_dict[i] for i in dataset.to_df()['ball_owning_team']]
            t_df['team_id'] = [team_dict[i] for i in dataset.to_df()['team_id']]
            t_df['player_id'] = [player_dict[i] if i != None else None for i in dataset.to_df()['player_id']]
            df_list.append(t_df)

            if (idx+1) % 100 == 0:
                df = pd.concat(df_list)
                df.to_csv('./data/traindataset/{}_dataset{}.csv'.format(competition_dict[k], (idx+1)//100))
                df_list = []

            idx += 1

        df = pd.concat(df_list)
        df.to_csv('./data/traindataset/{}_dataset{}.csv'.format(competition_dict[k], (idx+1)//100 + 1))
        print('{}_dataset.csv 저장완료'.format(competition_dict[k]))

    
    """            
    fieldnames = ['event_id', 'event_type',
                  'result', 'success', 
                  'period_id', 'timestamp',
                  'end_timestamp', 'ball_state',
                  'ball_owning_team', 'team_id',
                  'player_id', 'coordinates_x',
                  'coordinates_y', 'end_coordinates_x',
                  'end_coordinates_y', 'receiver_player_id',
                  'set_piece_type', 'body_part_type',
                  'pass_type','card_type']
    
    with open('./data/traindataset/dataset.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for k, v in event_dict.items():
        for i in tqdm.tqdm(v, desc='{}'.format(competition_dict[k])):
            dataset = statsbomb.load_open_data(str(i), coordinates="statsbomb", event_types=eventtype)
            t_df = dataset.to_df()

            team_dict = {i.team_id : i.name  for i in dataset.metadata.teams}
            player_dict = {i.player_id : i.name for i in dataset.metadata.teams[0].players}
            t_player_dict = {i.player_id : i.name for i in dataset.metadata.teams[1].players}
            player_dict.update(t_player_dict)

            t_df['ball_owning_team'] = [team_dict[i] for i in dataset.to_df()['ball_owning_team']]
            t_df['team_id'] = [team_dict[i] for i in dataset.to_df()['team_id']]
            t_df['player_id'] = [player_dict[i] if i != None else None for i in dataset.to_df()['player_id']]
            fieldnames = t_df.columns.to_list()

            with open('./data/traindataset/dataset.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for idx in range(len(t_df)):
                    writer.writerow(t_df.iloc[idx].to_dict())
    """

    return