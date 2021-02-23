from DBconnect import cur


def importCity():
    cur.execute('SELECT  * FROM CITY')
    return cur.fetchall()


def importCountries():
    cur.execute('SELECT  * FROM COUNTRY')
    return cur.fetchall()


def importTeams():
    cur.execute('SELECT  * FROM TEAM')
    return cur.fetchall()


def importTournament():
    cur.execute('SELECT  * FROM TOURNAMENT')
    return cur.fetchall()


def importGames():
    cur.execute('SELECT  * FROM GAME')
    return cur.fetchall()


def getGoals():
    cur.execute('SELECT home_score,away_score FROM GAME')
    return cur.fetchall()
