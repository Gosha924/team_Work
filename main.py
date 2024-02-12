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
        self.spn = [0.64, 0.64]
        self.coords = [30.314997, 59.938784]
        self.maps_server = 'http://static-maps.yandex.ru/1.x/'
        self.geocode_server = 'http://geocode-maps.yandex.ru/1.x/'
        self.setGeometry(20, 20, 600, 450)
        self.setWindowTitle('map')
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.update_map()
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)

    def update_map(self):
        print(f'{self.maps_server}?l=map&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}')
        self.response = requests.get(f'{self.maps_server}?l=map&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}')
        # self.coordinates = requests.get(f'{self.geocode_server}?l=map')
        with open('map.png', 'wb') as f:
            f.write(self.response.content)
        self.image = QPixmap('map.png')
        self.map.setPixmap(self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.spn[0] * 2 >= 100:
                pass
            else:
                self.spn[0] *= 2
                self.spn[1] *= 2
        if event.key() == Qt.Key_PageDown:
            if self.spn[0] / 2 <= 0:
                pass
            else:
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
        print(self.spn)
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())