import sqlalchemy
import requests
import pymysql
import json

url = sqlalchemy.engine.url.URL("mysql+pymysql", 
                                username="dbuser", password="dbuser", 
                                host="localhost", port="3306", database="lahman2017raw", query=None)

print("URL = ", url)


# Connect
cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2017raw',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



r = requests.get('http://127.0.0.1:5000/api/people/willite01')

print("The greatest hitter of all time is: ", json.dumps(r.json(), indent=2))