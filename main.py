
import requests
import PyQt5


cords = [50, 50]
mashtab = [0.3, 0.3]


map_server = 'http://static-maps.yandex.ru/1.x/'
map_params = {'map': str(cords[0]) + ',' + str(cords[1]),
              "mash": str(mashtab[0]) + ',' + str(cords[1]),
              '1': "map"
              }
response = requests.get(map_server, params=map_params)
with open('map.png', 'wb') as file:
    file.write(response.content)
