import os
import configparser
import pymysql
import pymysql.cursors
import requests

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
cursor.execute("SELECT login, pass FROM client_login_pass")
client_data = cursor.fetchall()

problem_client = {}
url = 'https://api.platform.masterservice.company/api/v1/login'
count = 1
for client in client_data:
    if client['login'].find('@') != -1 or len(client['login']) >= 10 and client['login'].isdigit():
        data = {
            'login': client['login'],
            'password': client['pass']
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(response.status_code)
            print(f'login: {client["login"]} pass: {client["pass"]}')
            problem_client.setdefault(client["login"], client['pass'])
            f = open('problem_clients.txt', 'a', encoding='utf-8')
            f.write(f'{client["login"]}, {client["pass"]}\n')
            f.close()
        print(f'Client {count} from: {len(client_data)}')
        count += 1

for key, val in problem_client.items():
    print(key, val)

