import json
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QRadioButton, QTextEdit, QPushButton, QCheckBox

Key_W_Rus = 1062
Key_A_Rus = 1060
Key_S_Rus = 1067
Key_D_Rus = 1042


class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.search_active = False
        self.search_point = ''
        self.apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
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
        self.scheme_button.move(20, 455)
        self.scheme_button.toggled.connect(self.change_type_of_map)
        self.satelite_button = QRadioButton("Спутник", self)
        self.satelite_button.move(120, 455)
        self.satelite_button.toggled.connect(self.change_type_of_map)
        self.hybrid_button = QRadioButton("Гибрид", self)
        self.hybrid_button.move(220, 455)
        self.hybrid_button.toggled.connect(self.change_type_of_map)
        self.search_text = QTextEdit(self)
        self.search_text.resize(200, 30)
        self.search_text.move(300, 455)
        self.search_button = QPushButton('Искать', self)
        self.search_button.resize(70, 30)
        self.search_button.move(510, 455)
        self.search_button.clicked.connect(self.search)
        self.reset_button = QPushButton('Сбросить', self)
        self.reset_button.resize(70, 30)
        self.reset_button.move(510, 490)
        self.reset_button.clicked.connect(self.reset)
        self.address_field = QTextEdit(self)
        self.address_field.resize(480, 30)
        self.address_field.move(20, 490)
        self.postcard_index = QCheckBox('Индекс', self)
        self.postcard_index.move(20, 520)
        self.postcard_index.toggled.connect(self.set_index)
        self.write_index = False
        self.address_field.setReadOnly(True)
        self.update_map()

    def set_index(self):
        if self.postcard_index.isChecked():
            self.write_index = True
        else:
            self.write_index = False
        # self.get_address()


    def reset(self):
        self.search_active = False
        self.address_field.setText('')
        self.update_map()

    def get_address(self, toponym):
        print(self.write_index)
        if not self.write_index:
            self.address_field.setText(toponym['metaDataProperty']['GeocoderMetaData']['text'])
        else:
            try:
                toponym_postal = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                address = toponym['metaDataProperty']['GeocoderMetaData']['text']
                self.address_field.setText(f'{address}, {toponym_postal}')
            except KeyError:
                address = toponym['metaDataProperty']['GeocoderMetaData']['text']
                self.address_field.setText(address)

    def get_coords(self):
        self.search_active = True
        req = requests.get(
            f'{self.geocode_server}?apikey={self.apikey}&geocode={self.search_text.toPlainText()}&format=json'
        )
        if not req:
            print(req.status_code, req.reason)
        js = req.json()
        with open('test.json', 'w', encoding='UTF-8') as f:
            json.dump(js, f, ensure_ascii=False)
        toponym = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.get_address(toponym)
        self.coords[0], self.coords[1] = map(float, toponym['Point']['pos'].split())
        self.search_point = list(map(float, toponym['Point']['pos'].split()))

    def search(self):
        if not self.search_active:
            self.get_coords()
        self.response = requests.get(
            f'{self.maps_server}?l={self.type_map}&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}&pt={self.search_point[0]}%2C{self.search_point[1]}'
        )
        self.update_map()

    def change_type_of_map(self):
        if self.scheme_button.isChecked():
            self.type_map = 'map'
        elif self.satelite_button.isChecked():
            self.type_map = 'sat'
        else:  # self.hybrid_button.isChecked():
            self.type_map = 'sat%2Cskl'
            # self.coordinates = requests.get(f'{self.geocode_server}?l=map')
        if self.search_active:
            self.search()
        else:
            self.update_map()

    def update_map(self):
        if not self.search_active:
            self.response = requests.get(
                f'{self.maps_server}?l={self.type_map}&ll={self.coords[0]}%2C{self.coords[1]}&spn={self.spn[0]}%2C{self.spn[1]}'
            )
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
        elif event.key() in [Qt.Key_A, Key_A_Rus]:
            if self.coords[0] - self.spn[0] * 5 <= -180:
                self.coords[0] = -180 + self.spn[0]
            else:
                self.coords[0] -= self.spn[0] * 5
        elif event.key() in [Qt.Key_D, Key_D_Rus]:
            if self.coords[0] + self.spn[0] * 5 >= 180:
                self.coords[0] = 180 - self.spn[0]
            else:
                self.coords[0] += self.spn[0] * 5
        elif event.key() in [Qt.Key_W, Key_W_Rus]:
            if self.coords[1] + self.spn[1] * 1.9 >= 100:
                pass
            else:
                self.coords[1] += self.spn[1] * 1.9
        elif event.key() in [Qt.Key_S, Key_S_Rus]:
            if self.coords[1] - self.spn[1] * 1.9 <= -100:
                pass
            else:
                self.coords[1] -= self.spn[1] * 1.9
        if self.search_active:
            self.search()
        else:
            self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())
