import pandas as pd
import string
from DBimports import *
from DBconnect import db_connection, cur
from check import checkScore, checkDate

df = pd.read_csv('results.csv', delimiter=',', encoding="utf_8")

cities = df['city'].unique()
countries = df['country'].unique()
concat_teams = pd.Series(list(df['home_team']) + list(df['away_team'])).unique()
tournaments = df['tournament'].unique()


def update():
    # updateCity()
    # updateCountry()
    # updateTeams()
    # updateTournaments()
    # updateGames()
    print("Update")


def updateCity():
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    cur.execute("DELETE FROM city")
    cur.execute('TRUNCATE TABLE city')
    cur.execute('SET FOREIGN_KEY_CHECKS = 1')
    for city in cities:
        tmp = ""
        acc = """ '",{}[].`;: -' ’‘"""
        for x in city:
            if x in string.ascii_letters or x in string.digits or x in acc:
                tmp += x
        cur.execute('INSERT INTO city(city_name) VALUES ("' + tmp + '");')
        db_connection.commit()


def updateCountry():
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    cur.execute("DELETE FROM country")
    cur.execute('TRUNCATE TABLE country')
    cur.execute('SET FOREIGN_KEY_CHECKS = 1')
    for country in countries:
        cur.execute('INSERT INTO country(country_name) VALUES ("' + country + '");')
        db_connection.commit()


def updateTeams():
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    cur.execute("DELETE FROM team")
    cur.execute('TRUNCATE TABLE team')
    cur.execute('SET FOREIGN_KEY_CHECKS = 1')
    for team in concat_teams:
        tmp = ""
        acc = """ '",{}[].`;: - """
        for x in team:
            if x in string.ascii_letters or x in string.digits or x in acc:
                tmp += x
        cur.execute('INSERT INTO team(team_name) VALUES ("' + tmp + '");')
        db_connection.commit()


def updateTournaments():
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    cur.execute("DELETE FROM tournament")
    cur.execute('TRUNCATE TABLE tournament')
    cur.execute('SET FOREIGN_KEY_CHECKS = 1')
    for tournament in tournaments:
        cur.execute('INSERT INTO tournament(tournament_name) VALUES ("' + tournament + '");')
        db_connection.commit()


def updateGames():
    cur.execute('SET FOREIGN_KEY_CHECKS = 0')
    cur.execute("DELETE FROM game")
    cur.execute('TRUNCATE TABLE game')
    cur.execute('SET FOREIGN_KEY_CHECKS = 1')
    imp_cities = list(importCity())
    imp_countries = list(importCountries())
    imp_teams = list(importTeams())
    imp_tournaments = list(importTournament())
    sql = 'INSERT INTO game(game_date, home_team_id, away_team_id, ' \
          'home_score, away_score, tournament_id, city_id, country_id, neutral) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    for index, row in df.iterrows():
        val = (row['date'],
               [item for item in imp_teams if item[1] == row['home_team']][0][0],
               [item for item in imp_teams if item[1] == row['away_team']][0][0],
               checkScore(row['home_score']),
               checkScore(row['away_score']),
               [item for item in imp_tournaments if item[1] == row['tournament']][0][0],
               list(filter(lambda x: x[1] == row['city'], imp_cities))[0][0],
               [item for item in imp_countries if item[1] == row['country']][0][0],
               row['neutral']
               )
        cur.execute(sql, val)
        db_connection.commit()
