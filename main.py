
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import io
import sys
import pygame
import os

mashtab = [0.6, 0.6]
coords = [57.1, 57.1]

maps_server = 'http://static-maps.yandex.ru/1.x/'
map_params = {
    'll': str(coords[0]) + ',' + str(coords[1]),
    'spn': str(mashtab[0]) + ',' + str(mashtab[1]),
    'l': 'map'}
response = requests.get(maps_server, params=map_params)
with open('map.png', 'wb') as f:
    f.write(response.content)


class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(20, 20, 600, 450)
        self.setWindowTitle('map')
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())