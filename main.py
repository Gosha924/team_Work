import urllib3.response

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import sys
import math


class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.spn = [0.02, 0.02]
        self.coords = [30.314997, 59.938784]
        self.maps_server = 'http://static-maps.yandex.ru/1.x/'
        self.geocode_server = 'http://geocode-maps.yandex.ru/1.x/'
        self.setGeometry(20, 20, 600, 450)
        self.setWindowTitle('map')
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.type_map = "map"
        self.update_map()
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)
    def update_map(self):
        #print(f'{self.maps_server}?l=map&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}')
        """self.response = requests.get(f'{self.maps_server}?l=map&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}')"""
        # self.coordinates = requests.get(f'{self.geocode_server}?l=map')
        map_params = {
            'll': str(self.coords[0]) + ',' + str(self.coords[1]),
            'spn': str(self.spn[0]) + ',' + str(self.spn[1]),
            'l': self.type_map}
        self.response = requests.get(self.maps_server, params=map_params)
        with open('map.png', 'wb') as f:
            f.write(self.response.content)
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn[0] *= 2
            self.spn[1] *= 2
        elif event.key() == Qt.Key_PageDown:
            self.spn[0] /= 2
            self.spn[1] /= 2
        elif event.key() == Qt.Key_Left:
            self.coords[0] -= self.spn[0]
        elif event.key() == Qt.Key_Right:
            self.coords[0] += self.spn[0]
        elif event.key() == Qt.Key_Up:
            self.coords[1] += self.spn[1]
        elif event.key() == Qt.Key_Down:
            self.coords[1] -= self.spn[1]
        # при нажатии на W происходит смена слоя карты
        elif event.key() == Qt.Key_W:
            if self.type_map == "map":
                self.type_map = "sat"
            elif self.type_map == "sat":
                self.type_map = "skl"
            elif self.type_map == "skl":
                self.type_map = "map"
        print(self.spn)
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())