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

sql_query = 'SELECT product.id FROM product ' \
            'LEFT JOIN product_2_category ON product.id = product_2_category.product_id ' \
            'LEFT JOIN product_category ON product_category.category_id = product_2_category.category_id ' \
            'LEFT JOIN product_brand ON product_brand.id = product.brand_id ' \
            'LEFT JOIN product_balans ON product.id = product_balans.product_id ' \
            'WHERE product_category.name = "Турбины" AND product_balans.quantity > 0'

cursor = connection.cursor()
cursor.execute(sql_query)
product_list = cursor.fetchall()

main_url = 'https://qa.platform.masterservice.company/'

for url in product_list:
    response = requests.get(main_url+str(url['id']))
    if response.status_code != 200:
        print(url['id'])