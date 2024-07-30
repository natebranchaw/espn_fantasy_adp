import pandas as pd 
import requests
import json

def get_espn_fantasy_football_adp(year, league_type = 'PPR', num_players = 500):
    '''Accesses ESPN's API to retrieve fantasy football player rankings and ADP for PPR leagues
       Takes as input a year which is the year you want data for and num_players which is the number of player you would like to retrieve the default value is 500'''
    league_type = league_type.upper()
    
    if league_type not in ['PPR', 'STANDARD']:
        raise ValueError('Please select PPR or STANDARD as League Type')
        
    espn_url = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/1/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info'.format(year)
    ranking_list = []
    
    filters = { "players": { "limit": num_players, "sortDraftRanks": { "sortPriority": 100, "sortAsc": True, "value": league_type } } }
    headers = {'x-fantasy-filter': json.dumps(filters)}
    
    r = requests.get(espn_url, headers = headers).json()
   
    for player in r['players']:
        player_name = player['player']['fullName']
        position = player['player']['defaultPositionId']
        adp = player['player']['ownership']['averageDraftPosition']
        
        if league_type == 'PPR':
            rank = player['player']['draftRanksByRankType']['PPR']['rank']
        else:
            rank = player['player']['dratRanksByRankType']['STANDARD']['rank']
        
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

def get_football_league_draft_history(league_id, year, login_file, league_type = 'PPR'):
    '''get_football_draft history takes as input a league_id and a year as well as a csv that contains the swid and espn_2 cookies '''
    
    players = []
    draft_picks = []
    teams = []
    
    #Read ESPN swid and espn_s2 cookies from login csv file
    credentials = pd.read_csv('espn_login.csv').to_dict('records')
    creds = credentials[0]
    cookies = {'swid': creds['swid'],
               'espn_s2': creds['espn_s2']}
    
    draft_url = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav'.format(year, league_id)
    r = requests.get(draft_url, cookies = cookies)  
    draft_data = r.json()
    
    draft_detail = draft_data['draftDetail']
    team_data = draft_data['teams']
    
    for team in team_data:
        team_name = team['name']
        abrev = team['abbrev']
        team_id = team['id']
        
        temp_team_dict = {'Team': team_name, 'ABR': abrev, 'Team_Id': team_id}
        temp_team_df = pd.DataFrame([temp_team_dict])
        teams.append(temp_team_df)
    
    team_data = pd.concat(teams)
        
    for pick in draft_detail['picks']:
        player_id = pick['playerId']
        overall_pick = pick['overallPickNumber']
        team = pick['teamId']
        
        temp_draft_dict = {'Player_ID': player_id, 'Overall_Pick': overall_pick, 'Team': team}
        temp_draft_df = pd.DataFrame([temp_draft_dict])
        draft_picks.append(temp_draft_df)
        
    all_picks = pd.concat(draft_picks)
    
    #Read in the player data for the top 1000 players for the given year and league type - PPR or STANDARD
    player_data = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?view=kona_player_info'.format(year, league_id)
    filters = { "players": { "limit": 1000, "sortDraftRanks": { "sortPriority": 100, "sortAsc": True, "value": league_type } } }
    p_headers = {'x-fantasy-filter': json.dumps(filters)}
    
    p_data = requests.get(player_data, headers = p_headers, cookies = cookies).json()
    
    for player in p_data['players']:
        name = player['player']['fullName']
        p_id = player['player']['id']
        
        temp_p_dict = {'Player': name, 'ID': p_id}
        temp_p_df = pd.DataFrame([temp_p_dict])
        
        players.append(temp_p_df)
    
    all_players = pd.concat(players)
    
    draft_teams = all_picks.merge(team_data, left_on = 'Team', right_on = 'Team_Id')
    
    draft_history = draft_teams.merge(all_players, how = 'left', left_on = 'Player_ID', right_on = 'ID')
    
    draft_history = draft_history.drop(['Team_x', 'Team_Id', 'ID', 'Player_ID'], axis = 1)
    draft_history.columns = ['Pick', 'Team', 'Abrev', 'Player']
    
    return draft_history
    
def get_espn_fantasy_basketball_adp(year, league_type = 'STANDARD', num_players = 500):
    '''Accesses ESPN's API to retrieve fantasy football player rankings and ADP for PPR leagues
       Takes as input a year which is the year you want data for and num_players which is the number of player you would like to retrieve the default value is 500'''
    league_type = league_type.upper()
    
    if league_type not in ['ROTO', 'STANDARD']:
        raise ValueError('Please select ROTO or STANDARD as League Type')
    year=2024
    espn_url = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/fba/seasons/{}/segments/1/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info'.format(year)
    ranking_list = []
    
    filters = { "players": { "limit": num_players, "sortDraftRanks": { "sortPriority": 100, "sortAsc": True, "value": league_type } } }
    headers = {'x-fantasy-filter': json.dumps(filters)}
    
    r = requests.get(espn_url, headers = headers).json()
   
    for player in r['players']:
        player_name = player['player']['fullName']
        position = player['player']['defaultPositionId']
        
        adp = player['player']['ownership']['averageDraftPosition']
        
        if league_type == 'STANDARD':
            rank = player['player']['draftRanksByRankType']['STANDARD']['rank']
        else:
            rank = player['player']['draftRanksByRankType']['ROTO']['rank']
        
        if position == 1:
            position = 'PG'
        elif position == 2:
            position = 'SG'
        elif position == 3:
            position = 'SF'
        elif position == 4:
            position = 'PF'
        elif position == 5:
            position = 'C'
        else:
            position = 'No Position'
            
        temp_dict = {'Player': player_name, 'Position': position, 'Rank': rank, 'ADP': adp}
        print(temp_dict)
        temp_df = pd.DataFrame([temp_dict])
        ranking_list.append(temp_df)
        
    espn_rankings = pd.concat(ranking_list)
    
    return espn_rankings