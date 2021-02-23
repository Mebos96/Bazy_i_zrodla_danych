from DBconnect import db_connection
from DBupdate import update

update()
db_connection.close()
