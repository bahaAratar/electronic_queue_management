import json

with open('points.json', 'r') as file:
    data = json.load(file)
    print(data[0]['ServicePoint'][0]['Translation'])
    for i in range(100):
        print(data[i]['ServicePoint'][i]['Translation'])
