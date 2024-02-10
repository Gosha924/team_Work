from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import io
import sys

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1200</width>
    <height>700</height>
   </rect>
  </property>
  <property name="maximumSize">
   <size>
    <width>1200</width>
    <height>700</height>
   </size>
  </property>
  <property name="font">
   <font>
    <pointsize>28</pointsize>
   </font>
  </property>
  <property name="cursor">
   <cursorShape>WaitCursor</cursorShape>
  </property>
  <property name="contextMenuPolicy">
   <enum>Qt::NoContextMenu</enum>
  </property>
  <property name="windowTitle">
   <string>Map</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>-10</y>
     <width>1200</width>
     <height>720</height>
    </rect>
   </property>
   <property name="font">
    <font>
     <pointsize>1</pointsize>
    </font>
   </property>
   <property name="text">
    <string>TextLabel</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""


class SignIn(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignIn()
    ex.show()
    sys.exit(app.exec_())
