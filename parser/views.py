from bs4 import BeautifulSoup
import json
import datetime
import psycopg2
# from models import Branches
# from electronic_queue_management.main.settings import DATABASES

def get_branch():
    with open('index.html', 'r+', encoding='utf-8') as html:
        soup = BeautifulSoup(html, features="html.parser")
        try:
            name = []
            for i in soup.find_all('a'):
                name.append(i.text)
        except:
            name = "пусто"
        try:
            region = "" #Область
        except:
            region = "пусто"
        try:
            address = "" #адрес
        except:
            address = "пусто"
        try:
            phone = "" #телефон
        except:
            phone = "пусто"
        branch_dict = []
        for i in range(0, 849):
            branch = {
                "name":name[i],
                "region":region,
                "address":address,
                "phone":phone
            }
            i -=1
            branch_dict.append(branch)
        return branch_dict

if __name__ == '__main__':
    with open(f"json/branch_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f:
        try:
            json.dump(get_branch(), f, indent=4, ensure_ascii=False)
            print('Филиалы добавлены')
        except:
            print('Филиалы не удалось получить')

connection = psycopg2.connect(
    database="rsk_bank",
    user="aliya",
    password="12345",
    host="127.0.0.1",
    port="5433"
)
cursor = connection.cursor()

with cursor:
    traffic = json.load(open(f"json/branch_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", encoding="utf8"))
    columns = ['name',
                'region',
                'phone']
    for row in traffic:
        keys = tuple(row[c] for c in columns)
        # cursor.execute("""DELETE FROM parser_branches""")
        cursor.execute("""INSERT INTO parser_branches (
                        name,
                        region,
                        phone) VALUES (%s,%s,%s)""",keys)

    connection.commit()
    connection.close()


