
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


logging.basicConfig(
    filename="log_stats.txt",
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s', 
    level  = logging.INFO,)

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

host = "localhost"
user = "root"
pwd = "mysql1"
mysql_db = "futbol_bd"

db_connection = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:3307/{mysql_db}')
connection = db_connection.connect

def normalize_data(df):
    df = df.replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u")
    return df

def reorder_columns(df, column, pos):
    column_val = df[column]
    df = df.drop(column = column)
    df.insert(loc=pos, column=column, value=column_val)
    return df

driver = webdriver.Chrome("/usr/local/bin/chromedriver")

# Player (stats)
stats = ['player', "nationatily", "position", "squad", "age", "birth_year", "games", "games_start", "minutes", "goals", "assists"]

# Goalkeepers (stats)
keepers = ['player', "nationatily", "position", "squad", "age", "birth_year", "games_gk", "games_start_gk", "minutes_gk", "goals_against", "assists_against"]


def get_tables(url):
    
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    #res = requests.get(url, headers=headers)
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')

    all_tables = soup.find_all("tbody")

    team_table = all_tables[9]
    player_table = all_tables[11]

    return team_table, player_table


def get_frame( features, player_table, is_outfield_player):
    pre_df_player = dict()
    features_wanted_player = features
    row_player = player_table.find_all("tr")
    for row in row_player:

        logging.warning(row)
        if(row.find("th", {"scope": "row"}) != None):
            if( row.find("td", {"data-stat": 'position'}) != None) :
                if((is_outfield_player == True) & (row.find("td", {"data-stat": 'position'}).text.strip() != "GK")):
                    for f in features_wanted_player:
                        cell = row.find("td", {"data-stat": f})
                        if cell:
                            a = cell.text.strip().encode()
                            text = a .decode('utf-8')
                            if (text == "-"):
                                text = 0
                            if ((f != "player") & (f != "nationatily") & (f != "position") & (f != "squad") & (f != "age") & (f != "birth_year")):
                                text = float(text.replace(",", ""))
                            if f in pre_df_player:
                                pre_df_player[f].append(text)
                            else:
                                pre_df_player[f] = [text]
                elif( (is_outfield_player == False) & (row.find("td", {"data-stat": 'position'}).text.strip() != "GK")):
                    for f in features_wanted_player:
                        cell = row.find("td", {"data-stat": f})
                        if cell:
                            a = cell.text.strip().encode()
                            text = a .decode('utf-8')
                            if (text == "-"):
                                text = 0
                            if ((f != "player") & (f != "nationatily") & (f != "position") & (f != "squad") & (f != "age") & (f != "birth_year")):
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

    logging.info(df1)
    df2 = frame_for_category("shooting", top, end, keepers, True)
    logging.info(df2)
    df3 = frame_for_category("passing", top, end, stats, True)
    logging.info(df3)
    df4 = frame_for_category("passing_types", top, end, stats, True)
    logging.info(df4)
    df5 = frame_for_category("gca", top, end, stats, True)
    logging.info(df5)
    df6 = frame_for_category("defense", top, end, stats, True)
    logging.info(df6)
    df7 = frame_for_category("possession", top, end, stats, True)
    logging.info(df7)
    df8 = frame_for_category("misc", top, end, stats, True)
    logging.info(df8)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def get_keeper_data(top, end):
    df1 = frame_for_category("keepers", top, end, stats, False)
    logging.info(df1)
    df2 = frame_for_category("keepersadv", top, end, keepers, False)
    logging.info(df2)
    df = pd.concat([df1, df2], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

df_out_premier_league = get_outfield_data('https://fbref.com/es/comps/22/', '/Estadisticas-de-Major-League-Soccer/')
print(df_out_premier_league)