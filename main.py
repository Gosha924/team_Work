
import urllib3.response

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QRadioButton
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
        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle('map')
        self.map = QLabel(self)
        self.map.move(0, 0)
        self.map.resize(600, 450)
        self.image = QPixmap('map.png')
        self.type_map = "map"
        self.map.setPixmap(self.image)
        self.scheme_button = QRadioButton("Схема", self)
        self.scheme_button.move(20, 530)
        self.scheme_button.toggled.connect(self.update_map)
        self.satelite_button = QRadioButton("Спутник", self)
        self.satelite_button.move(220, 530)
        self.satelite_button.toggled.connect(self.update_map)
        self.hybrid_button = QRadioButton("Гибрид", self)
        self.hybrid_button.move(420, 530)
        self.hybrid_button.toggled.connect(self.update_map)
        self.update_map()

    def update_map(self):
        if self.scheme_button.isChecked():
            self.type_map = 'map'
        elif self.satelite_button.isChecked():
            self.type_map = 'sat'
        else: # self.hybrid_button.isChecked():
            self.type_map = 'sat%2Cskl'
        # self.coordinates = requests.get(f'{self.geocode_server}?l=map')
        self.response = requests.get(
            f'{self.maps_server}?l={self.type_map}&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}')
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
        elif event.key() == Qt.Key_A:
            if self.coords[0] - self.spn[0] * 5 <= -180:
                self.coords[0] = -180 + self.spn[0]
            else:
                self.coords[0] -= self.spn[0] * 5
        elif event.key() == Qt.Key_D:
            if self.coords[0] + self.spn[0] * 5 >=180:
                self.coords[0] = 180 - self.spn[0]
            else:
                self.coords[0] += self.spn[0] * 5
        elif event.key() == Qt.Key_W:
            if self.coords[1] + self.spn[1] * 1.9 >= 100:
                pass
            else:
                self.coords[1] += self.spn[1] * 1.9
        elif event.key() == Qt.Key_S:
            if self.coords[1] - self.spn[1] * 1.9 <= -100:
                pass
            else:
                self.coords[1] -= self.spn[1] * 1.9
            self.coords[1] -= self.spn[1]
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())
