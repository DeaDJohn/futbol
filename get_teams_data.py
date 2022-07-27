from this import d
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
pwd = "mysql1"
mysql_db = "futbol_bd"

db_connection = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:3307/{mysql_db}')
connection = db_connection.connect
logging.info(db_connection)
logging.info("Empezando a obtener los datos de los equipos")

def remove_accents(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

"""
comps_url = [
    'https://www.transfermarkt.es/laliga/startseite/wettbewerb/ES1',
    'https://www.transfermarkt.es/premier-league/startseite/wettbewerb/GB1',
    'https://www.transfermarkt.es/serie-a/startseite/wettbewerb/IT1',
    'https://www.transfermarkt.es/1-bundesliga/startseite/wettbewerb/L1',
    'https://www.transfermarkt.es/ligue-1/startseite/wettbewerb/FR1'
]


columns_names = ["team_name", "team_image", "team_profile"]
df_teams = pd.DataFrame(columns = columns_names)

for comp_url in comps_url:
    response_obj = requests.get(comp_url, headers=headers)
    page_bs = BeautifulSoup(response_obj.content, 'html.parser')
    teams = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
    for team in teams:
        team_name = team.find_all("td", {"class": "hauptlink"})[0].find("a").text.strip()
        team_image = team.find_all("td", {"class": "zentriert"})[0].find("img").get("src").replace("tiny", "head")
        team_profile = "https://www.transfermarkt.es" + team.find_all("td", {"class": "hauptlink"})[0].find("a").get("href") + "plus/1"
        df_teams.loc[len(df_teams)] = [team_name, team_image, team_profile]
print(df_teams)
teams_saved = df_teams.to_sql("tab_teams", con=db_connection, if_exists="append", index=False, chunksize=1000)
logging.info("Total equipos guardados: {}".format(teams_saved))


df_teams = pd.read_sql("SELECT * FROM tab_teams", con=db_connection)
df_teams = df_teams.reset_index()
logging.info("Empezando a obtener los datos de los paises")

country_column_names = ["country_name", "country_image"]
# df_countries = pd.DataFrame(columns=country_column_names)

for index, row in df_teams.iterrows():
    logging.info("Equipo {}".format(row["team_name"]))
    url = row["team_profile"]
    response_obj = requests.get(url, headers=headers)
    page_bs = BeautifulSoup(response_obj.content, 'html.parser')
    players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
    
    for player in players :
        player_image_element = player.find_all("td", {"class": "zentriert"})[2].find("img")
        player_country = player_image_element.get("title")
        if not any( df_countries['country_name'] == player_country) :
            logging.info("País encontrado {}".format(player_country))
            player_country_img = player_image_element.get("src").replace("verysmall", "head")
            df_countries.loc[len(df_countries)] = [player_country, player_country_img]
countries_saved = df_countries.to_sql("tab_countries", con=db_connection, if_exists="append", index=False, chunksize=1000)
logging.info("Total paises guardados: {}".format(countries_saved))

"""
df_teams = pd.read_sql("SELECT * FROM tab_teams", con=db_connection)
df_teams = df_teams.reset_index()
logging.info("Empezando a obtener los datos de los jugadores")
player_column_names = ["player_name", "player_birth", "player_age", "player_height", "player_pref_foot", "player_position", "player_sing_date", "player_end_contract", "player_market_value", "player_img", "player_country"]
df_players = pd.DataFrame(columns=player_column_names)


for index, row in df_teams.iterrows():
    logging.info("Equipo {}".format(row["team_name"]))
    url = row["team_profile"]
    response_obj = requests.get(url, headers=headers)
    page_bs = BeautifulSoup(response_obj.content, 'html.parser')
    players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})

    for player in players :
        player_name = player.find("td", {"class": "posrela"}).find("table").find("tr").find("td").find("img").get("title")
        
        player_name = remove_accents(player_name)
        player_position = player.find_all( "td", {"class": "posrela"})[2].find("table").find_all("tr")[1].find("td").text.strip()
        player_birth = player.find_all("td", {"class": "zentriert"})[1].text
        player_age = player_birth.split("(")[1].split(")")[0]
        player_birth = player_birth.split("(")[0]
        player_height = player.find_all("td", {"class": "zentriert"})[3].text
        player_foot = player.find_all("td", {"class": "zentriert"})[4].text
        player_sing_date = player.find_all("td", {"class": "zentriert"})[5].text
        player_end_contract = player.find_all("td", {"class": "zentriert"})[7].text
        player_market_value = player.find("td", {"class": "rechts hauptlink"}).text
        player_img = player.find("td", {"class": "posrela"})[2].find("table").find("tr").find("td").find("img").get("data-src")
        player_country = player.find("td", {"class": "zentriert"})[2].find("img").get("title")
        logging.info("Jugador {} - {} - {}".format(player_name, player_position, player_end_contract))
        # id_country = countries[player_country]
        df_players.loc[len(df_players)] = [player_name, player_birth, player_age, player_height, player_foot, player_position, player_sing_date, player_end_contract, player_market_value, player_img, player_country]
for column in df_players :
    df_players.loc[((df_players[column].isnull()) | (df_players[column] == "") | (df_players[column] == "-")), column] = np.nan

df_players['player_birth'] = df_players['player_birth'].astype('datetime64[ns]')
df_players['player_end_contract'] = df_players['player_end_contract'].astype('datetime64[ns]')

player_saved = df_players.to_sql("tab_players", con=db_connection, if_exists="append", index=False, chunksize=1000)
print(player.prettify())