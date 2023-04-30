from pickle import TRUE
from this import d
from tkinter import FALSE
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import pymysql
import unicodedata
from sqlalchemy import create_engine

import logging

logging.basicConfig(
    filename="log.txt",
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


def remove_accents(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s
def get_teams_from_web() :
    '''Obtener los equipos de las 5 principales ligas de futbol.'''

    comps_url = [
        'https://www.transfermarkt.es/laliga/startseite/wettbewerb/ES1',
        'https://www.transfermarkt.es/premier-league/startseite/wettbewerb/GB1',
        'https://www.transfermarkt.es/serie-a/startseite/wettbewerb/IT1',
        'https://www.transfermarkt.es/1-bundesliga/startseite/wettbewerb/L1',
        'https://www.transfermarkt.es/ligue-1/startseite/wettbewerb/FR1'
    ]
    df_leagues = pd.read_sql("SELECT * FROM tab_leagues", con=db_connection)
    df_leagues = df_leagues.reset_index()
    logging.info("Empezando a obtener los datos de los equipos")
    columns_names = ["team_name", "team_image", "team_profile", "id_league"]
    df_teams = pd.DataFrame(columns = columns_names)

    for index, row  in df_leagues.iterrows():
        comp_url = row["league_transfermarket"]
        response_obj = requests.get(comp_url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        teams = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
        for team in teams:
            id_league = row["id_league"]
            team_name = team.find_all("td", {"class": "hauptlink"})[0].find("a").text.strip()
            team_image = team.find_all("td", {"class": "zentriert"})[0].find("img").get("src").replace("tiny", "head")
            team_profile = "https://www.transfermarkt.es" + team.find_all("td", {"class": "hauptlink"})[0].find("a").get("href").replace('startseite','kader') + "/plus/1"
            df_teams.loc[len(df_teams)] = [team_name, team_image, team_profile, id_league]
    print(df_teams)
    teams_saved = df_teams.to_sql("tab_teams", con=db_connection, if_exists="append", index=False, chunksize=1000)
    logging.info("Total equipos guardados: {}".format(teams_saved))



def get_countries_from_web():
    '''Obtener los paises recorriendo las url de los equipos obtenidos de la tabla tab_teams de la bbdd.'''
    df_teams = pd.read_sql("SELECT * FROM tab_teams", con=db_connection)
    df_teams = df_teams.reset_index()
    logging.info("Empezando a obtener los datos de los paises")

    country_column_names = ["name_country", "name_country_img"]
    df_countries = pd.DataFrame(columns=country_column_names)

    for index, row in df_teams.iterrows():
        logging.info("Equipo {}".format(row["team_name"]))
        url = row["team_profile"]
        response_obj = requests.get(url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
        
        for player in players :
            player_image_element = player.find_all("td", {"class": "zentriert"})[2].find("img")
            name_country = player_image_element.get("title")
            if not any( df_countries['name_country'] == name_country) :
                logging.info("País encontrado {}".format(name_country))
                name_country_img = player_image_element.get("src").replace("verysmall", "head")
                df_countries.loc[len(df_countries)] = [name_country, name_country_img]
    countries_saved = df_countries.to_sql("tab_countries", con=db_connection, if_exists="append", index=False,  chunksize=1000)
    logging.info("Total paises guardados: {}".format(countries_saved))

def get_players_from_web():
    '''Obtener todos los jugadores de los equipos que esten almacenados en la bbdd en la tabla tab_teams.'''
    df_teams = pd.read_sql("SELECT * FROM tab_teams", con=db_connection)
    df_teams = df_teams.reset_index()

    countries = pd.read_sql("SELECT * FROM tab_countries", con=db_connection)
    #countries = countries.reset_index()

    logging.info("Empezando a obtener los datos de los jugadores")
    player_column_names = ["player_name", "player_birth", "player_age", "player_height", "player_foot", "player_position", "player_sing_date", "player_end_contract", "player_market_value", "player_img", "player_country", 'id_team', 'id_country', 'id_league', 'player_slug', 'id_season']
    df_players = pd.DataFrame(columns=player_column_names)


    for index, row in df_teams.iterrows():
        logging.info("Equipo {}".format(row["team_name"]))
        print("Equipo {}".format(row["team_name"]))
        url = row["team_profile"]
        id_team = row['id_team']
        id_league = row['id_league']
        response_obj = requests.get(url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})

        for player in players :
            player_name = player.find("td", {"class": "posrela"}).find("table").find("tr").find("td").find("img").get("title")
            
            player_name = player_name
            player_slug = slugify(player_name)
            player_position = player.find( "td", {"class": "posrela"}).find("table").find_all("tr")[1].find("td").text.strip()
            player_birth = player.find_all("td", {"class": "zentriert"})[1].text
            player_age = player_birth.split("(")[1].split(")")[0]
            player_birth = player_birth.split("(")[0]
            player_height = player.find_all("td", {"class": "zentriert"})[3].text
            player_foot = player.find_all("td", {"class": "zentriert"})[4].text
            player_sing_date = player.find_all("td", {"class": "zentriert"})[5].text
            player_end_contract = player.find_all("td", {"class": "zentriert"})[7].text
            player_market_value = player.find("td", {"class": "rechts hauptlink"}).text
            player_img = player.find("td", {"class": "posrela"}).find("table").find("tr").find("td").find("img").get("data-src")
            player_country = player.find_all("td", {"class": "zentriert"})[2].find("img").get("title")
            logging.info("Jugador {} - {} - {}".format(player_name, player_position, player_end_contract))
            id_country = countries.loc[countries['name_country'] == player_country]['id_country'].values[0]
            id_season = 1
            
            df_players.loc[len(df_players)] = [player_name,player_birth, player_age, player_height, player_foot, player_position, player_sing_date, player_end_contract, player_market_value, player_img, player_country, id_team, id_country, id_league,player_slug, id_season]

    for column in df_players :
        df_players.loc[( (df_players[column] == " ") | (df_players[column] == "-")), column] = np.nan

        df_players['player_birth'] = pd.to_datetime(df_players['player_birth'], infer_datetime_format=True, utc=True, errors='ignore')
        df_players['player_sing_date'] = pd.to_datetime(df_players['player_sing_date'], infer_datetime_format=True, utc=True, errors='ignore')
        df_players['player_end_contract'] = pd.to_datetime(df_players['player_end_contract'], infer_datetime_format=True, utc=True, errors='ignore')


    player_saved = df_players.to_sql("tab_player", con=db_connection, if_exists="append", index=False, chunksize=1000)
    logging.info("Total jugadores guardados: {}".format(player_saved))


#get_teams_from_web()
#get_countries_from_web()
get_players_from_web()