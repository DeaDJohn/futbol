from flask import Flask, jsonify
from flask_cors import CORS
from markupsafe import escape
from sqlalchemy import create_engine
import pandas as pd
import numpy as np


# Función para conectarse a la base de datos

host = "localhost"
user = "root"
pwd = "mauFJcuf5dhRMQrjj"
mysql_db = "futbol_bd"

db_connection = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:3306/{mysql_db}')
connection = db_connection.connect




app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/team/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    # show the user profile for that user
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_player where id_team = "'''+ str(team_id) +'''"'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)


@app.route('/player/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    # show the post with the given id, the id is an integer
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_player where id_player = "'''+ str(player_id) +'''"'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)


@app.route('/league/<int:league_id>', methods=['GET'])
def get_teams_by_league_id(league_id):
    # show the post with the given id, the id is an integer
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_teams where id_league = "'''+ str(league_id) +'''"'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)

@app.route('/league/', methods=['GET'])
def get_all_leagues():
    # show the post with the given id, the id is an integer
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_leagues where id_league > 0'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)


@app.route('/country/<int:id_country>', methods=['GET'])
def get_teams_by_id_country(id_country):
    # show the post with the given id, the id is an integer
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_countries where id_country = "'''+ str(id_country) +'''"'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)

@app.route('/stats/<int:player_id>', methods=['GET'])
def get_stats_by_player_id(player_id):
    # show the post with the given id, the id is an integer
    # Consulta SQL para obtener los datos
    query = '''SELECT * FROM tab_stats_player where id_player = "'''+ str(player_id) +'''"'''
    # Cargar los datos en un DataFrame de Pandas
    df = pd.read_sql(query, con=db_connection)
    # Convertir el DataFrame en un diccionario
    data = df.to_dict(orient='records')
    # Devolver los datos en formato JSON
    return jsonify(data)