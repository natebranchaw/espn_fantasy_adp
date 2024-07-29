import pandas as pd 
import requests
import json

def get_espn_fantasy_football_adp(year, num_players = 500):
    '''Accesses ESPN's API to retrieve fantasy football player rankings and ADP for PPR leagues
       Takes as input a year which is the year you want data for and num_players which is the number of player you would like to retrieve the default value is 500'''
    
    espn_url = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/1/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info'.format(year)
    ranking_list = []
    
    filters = { "players": { "limit": 500, "sortDraftRanks": { "sortPriority": 100, "sortAsc": True, "value": "PPR" } } }
    headers = {'x-fantasy-filter': json.dumps(filters)}
    
    r = requests.get(espn_url, headers = headers).json()
   
    for player in r['players']:
        player_name = player['player']['fullName']
        position = player['player']['defaultPositionId']
        rank = player['player']['draftRanksByRankType']['PPR']['rank']
        adp = player['player']['ownership']['averageDraftPosition']
        
        if position == 1:
            position = 'QB'
        elif position == 2:
            position = 'RB'
        elif position == 3:
            position = 'WR'
        elif position == 4:
            position = 'TE'
        elif position == 16:
            position = 'D/ST'
        elif position == 5:
            position = 'K'
        else:
            position = 'No Position'
            
        temp_dict = {'Player': player_name, 'Position': position, 'Rank': rank, 'ADP': adp}
        temp_df = pd.DataFrame([temp_dict])
        ranking_list.append(temp_df)
        
    espn_rankings = pd.concat(ranking_list)
    
    return espn_rankings

x = get_espn_fantasy_football_adp(2024)
