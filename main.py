import os

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import io
import sys
# import pygame
# import os

# mashtab = [0.6, 0.6]
# coords = [57.1, 57.1]
#
# maps_server = 'http://static-maps.yandex.ru/1.x/'
# map_params = {
#     'll': str(coords[0]) + ',' + str(coords[1]),
#     'spn': str(mashtab[0]) + ',' + str(mashtab[1]),
#     'l': 'map'}
# response = requests.get(maps_server, params=map_params)
# with open('map.png', 'wb') as f:
#     f.write(response.content)


class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mashtab = 1
        self.coords = [30.314997, 59.938784]
        # self.maps_server = 'http://static-maps.yandex.ru/1.x/'
        # self.map_params = {
        #     'll': str(self.coords[0]) + ',' + str(self.coords[1]),
        #     'spn': str(self.mashtab) + ',' + str(self.mashtab),
        #     'l': 'map'}
        # self.response = requests.get(self.maps_server, params=self.map_params)
        # with open('map.png', 'wb') as f:
        #     f.write(self.response.content)
        self.setGeometry(20, 20, 600, 450)
        self.setWindowTitle('map')
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.update_map()
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)


    def update_map(self):
        print(self.mashtab)
        self.maps_server = 'http://static-maps.yandex.ru/1.x/'
        self.map_params = {
            'll': str(self.coords[0]) + ',' + str(self.coords[1]),
            'spn': str(self.mashtab) + ',' + str(self.mashtab),
            'l': 'map'}
        self.response = requests.get(self.maps_server, params=self.map_params)
        with open('map.png', 'wb') as f:
            f.write(self.response.content)
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.mashtab += 0.5
        if event.key() == Qt.Key_PageDown:
            self.mashtab -= self.mashtab / 10

        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())