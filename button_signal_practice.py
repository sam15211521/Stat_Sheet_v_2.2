import sys
import os
import pickle

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from stats import Stat, MajorStat, Skill
from Character import Character


class MainScreen(QMainWindow):
    def __init__(self,):
        super().__init__()
        button = Button("Push Me", "this")
        button.pressed.connect(lambda signal = button.info: self.print_this(signal))

        self.setCentralWidget(button)
    
    def print_this(self, this):
        print(this)

class Button(QPushButton):
    def __init__(self, name, text):
        super().__init__()
        self.info = text
        self.setText(name)

app = QApplication()
window = MainScreen()

window.show()

app.exec()