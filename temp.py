import sqlalchemy
from sqlalchemy import create_engine
import configparser
import pytest
import os
import pymysql.cursors

thisfolder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(thisfolder, 'db.ini')
parser = configparser.ConfigParser()
parser.read(inifile)

HOST = parser.get('db', 'host')
PORT = int(parser.get('db', 'port'))
DB_NAME = parser.get('db', 'db_name')
USER_NAME = parser.get('db', 'user_name')
DB_PASSWORD = parser.get('db', 'db_password')

connection = pymysql.connect(host=HOST,
                             port=PORT,
                             user=USER_NAME,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute('SELECT * FROM customers WHERE phone="0685340262"')
data = cursor.fetchall()
connection.commit()
print(data)