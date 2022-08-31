
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pymysql
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


logging.basicConfig(
    filename="log_stats.txt",
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s', 
    level  = logging.INFO,)

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

host = "localhost"
user = "root"
pwd = "mauFJcuf5dhRMQrjj"
mysql_db = "futbol_bd"

db_connection = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:3306/{mysql_db}')
connection = db_connection.connect
logging.info(db_connection)

def normalize_data(df):
    df = df.replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u")
    return df

def reorder_columns(df, column, pos):
    column_val = df[column]
    df = df.drop(column = column)
    df.insert(loc=pos, column=column, value=column_val)
    return df

#driver = webdriver.Chrome("/usr/local/bin/chromedriver")

# Player (stats)
stats = ['player', "nationality", "position", "squad", "age",  "games", "games_start", "minutes", "goals", "assists"]

# Goalkeepers (stats)
keepers = ["player","nationality","position","age","gk_games","gk_games_starts","gk_minutes","minutes_90s","gk_goals_against","gk_goals_against_per90","gk_shots_on_target_against","gk_saves","gk_save_pct","gk_wins","gk_ties","gk_losses","gk_clean_sheets","gk_clean_sheets_pct","gk_pens_att","gk_pens_allowed","gk_pens_saved","gk_pens_missed","gk_pens_save_pct","matches"]

keepersadv = ["player","nationality","position","age","minutes_90s","gk_goals_against","gk_pens_allowed","gk_free_kick_goals_against","gk_corner_kick_goals_against","gk_own_goals_against","gk_psxg","gk_psnpxg_per_shot_on_target_against","gk_psxg_net","gk_psxg_net_per90","gk_passes_completed_launched","gk_passes_launched","gk_passes_pct_launched","gk_passes","gk_passes_throws","gk_pct_passes_launched","gk_passes_length_avg","gk_goal_kicks","gk_pct_goal_kicks_launched","gk_goal_kick_length_avg","gk_crosses","gk_crosses_stopped","gk_crosses_stopped_pct","gk_def_actions_outside_pen_area","gk_def_actions_outside_pen_area_per90","gk_avg_distance_def_actions","matches"]
keepersadv2 = []

shooting = ["player","nationality","position","age","minutes_90s","goals","shots_total","shots_on_target","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","average_shot_distance","shots_free_kicks","pens_made","pens_att","xg","npxg","npxg_per_shot","xg_net","npxg_net","matches"]

passing = ["player","nationality","position","age","minutes_90s","passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes","matches"]

passing_types2 = ["player","nationality","position","age","minutes_90s","passes","passes_live","passes_dead","passes_free_kicks","through_balls","passes_pressure","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_ground","passes_low","passes_high","passes_left_foot","passes_right_foot","passes_head","throw_ins","passes_other_body","passes_completed","passes_offsides","passes_oob","passes_intercepted","passes_blocked","matches"]

gca = ["player","nationality","position","age","minutes_90s","sca","sca_per90","sca_passes_live","sca_passes_dead","sca_dribbles","sca_shots","sca_fouled","sca_defense","gca","gca_per90","gca_passes_live","gca_passes_dead","gca_dribbles","gca_shots","gca_fouled","gca_defense","matches",]

defense = ["player","nationality","position","age","minutes_90s","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains","pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","tackles_interceptions","clearances","errors","matches"]

possession = ["player","nationality","position","age","minutes_90s","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct","players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","pass_targets","passes_received","passes_received_pct","progressive_passes_received","matches"]

misc = ['player', 'nationality', 'position', 'age', 'minutes_90s', 'cards_yellow', 'cards_red', 'cards_yellow_red', 'fouls', 'fouled', 'offsides', 'crosses', 'interceptions', 'tackles_won', 'pens_won', 'pens_conceded', 'own_goals', 'ball_recoveries', 'aerials_won', 'aerials_lost', 'aerials_won_pct', 'matches']


def get_tables(url):
    
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    #res = requests.get(url, headers=headers)
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')

    all_tables = soup.find_all("tbody")

    if(all_tables[8]) :
        team_table = all_tables[8]
    if(all_tables[11]) :
        player_table = all_tables[11]

    return player_table,team_table 


def get_frame( features, player_table, is_outfield_player):
    pre_df_player = dict()
    features_wanted_player = features
    row_player = player_table.find_all("tr")
    for row in row_player:
        if row.find(class_='thead'):
            continue
        logging.info(row)
        if(row.find("th", {"scope": "row"}) != None ):
            if( row.find("td", {"data-stat": 'position'}) != None) :
                if((is_outfield_player == True) & (row.find("td", {"data-stat": 'position'}).text.strip() != "GK")):
                    for f in features_wanted_player:
                        cell = row.find("td", {"data-stat": f})
                        if cell:
                            a = cell.text.strip().encode()
                            text = a .decode('utf-8')
                            if (text == ""):
                                text = 0
                            if (text == "-"):
                                text = 0
                            if( f == 'matches' and text == 'Partidos'):
                                continue
                            if (f == 'nationality'):
                                # Dejar el codigo internacional
                                text = text[-3:]
                            if (f == 'age'):
                                # Dejar solo la edad.
                                text = text[0:2]
                            if ((f != "player") & (f != 'nationality') & (f != "position") & (f != "squad") & (f != "age") & (f != "birth_year") ) :
                                if( type(text) == str ):
                                    text = float(text.replace(",", ""))
                            if f in pre_df_player:
                                pre_df_player[f].append(text)
                            else:
                                pre_df_player[f] = [text]
                            
                            pre_df_player['id_season'] = 1
                elif( (is_outfield_player == False) & (row.find("td", {"data-stat": 'position'}).text.strip() != "GK")):
                    for f in features_wanted_player:
                        cell = row.find("td", {"data-stat": f})
                        if cell:
                            a = cell.text.strip().encode()
                            text = a .decode('utf-8')
                            if (text == "-"):
                                text = 0
                            if ((f != "player") & (f != "nationality") & (f != "position") & (f != "squad") & (f != "age") & (f != "birth_year")):
                                text = float(text.replace(",", ""))
                            if f in pre_df_player:
                                pre_df_player[f].append(text)
                            else:
                                pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player
            


def frame_for_category(category, top, end, features, is_outfield_player):
    url = (top + category + end)
    player_table, team_table = get_tables(url)

    df_player = get_frame(features, player_table, is_outfield_player)
    return df_player


def get_outfield_data(top, end):
    df1 = frame_for_category("stats", top, end, stats, True)
    df2 = frame_for_category("shooting", top, end, shooting, True)
    df3 = frame_for_category("passing", top, end, passing, True)
    df4 = frame_for_category("passing_types", top, end, passing_types2, True)
    df5 = frame_for_category("gca", top, end, gca, True)
    df6 = frame_for_category("defense", top, end, defense, True)
    df7 = frame_for_category("possession", top, end, possession, True)
    df8 = frame_for_category("misc", top, end, misc, True)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    logging.info(df)
    return df

def get_keeper_data(top, end):
    df1 = frame_for_category("keepers", top, end, keepers, False)
    df2 = frame_for_category("keepersadv", top, end, keepersadv, False)
    df = pd.concat([df1, df2], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    logging.info(df)
    return df

df_out_premier_league = get_outfield_data('https://fbref.com/es/comps/9/', '/Estadisticas-de-Premier-League/')
df_out_premier_league.to_excel('mls.xlsx')
#try:
#    #this will fail if there is a new column
#    player_saved = df_out_premier_league.to_sql(name='tab_stats_player', con=db_connection, if_exists = 'append', index=False)
#except:
#    data = pd.read_sql('SELECT * FROM tab_stats_player', db_connection)
#    df_out_premier_league2 = pd.concat([data,df_out_premier_league])
#    player_saved = df_out_premier_league2.to_sql(name='tab_stats_player', con=db_connection, if_exists = 'replace', index=False)
#
logging.info("Total jugadores guardados: {}".format(player_saved))
print(df_out_premier_league)