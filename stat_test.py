import sys
import statsv2
from Character import Character
from statsv2 import *

from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                               QLabel, QVBoxLayout)

class window(QMainWindow):
    def __init__(self, character: statsv2.Skill):
        super().__init__() 
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.subject = character
        self.labels = {}
        self.mastery_label = None
        
        self.add_to_layout()
        self.add_buttons()
        print(*[key for key in self.subject.__dict__.keys()], sep='\n')
        
        self.timer = None
        #self.set_timer()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()

    def reset_timer(self):
        self.timer.stop()
        self.timer.start(5000)
    def add_to_layout(self):
        for name, attribute in self.subject.__dict__.items():
            label = QLabel(f'{name} | {attribute}')
            self.labels[name] = label
            self.main_layout.addWidget(label)
        
    
    def add_buttons(self):
        self.close_button = QPushButton('Close')
        self.main_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.increase_level = QPushButton('Increase Level')
        self.main_layout.addWidget(self.increase_level)
        self.increase_level.clicked.connect(self.increase_skill_level)
    
    def set_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(5000)
    
    def increase_skill_level(self):
        self.subject : statsv2.Skill
        self.subject.increase_level()
        self.update_all_labels()
        
    def update_all_labels(self):
        for name,label in self.labels.items():
            label : QLabel
            label.setText(f'{name} | {self.subject.__dict__[name]} ')





if __name__ == "__main__":
    import inspect
    a = QApplication()
    stat = Skill(name= 'aba', stat_increase_multiplier=.0008)
    stta = Stat()
    stat.basics = True
    stat.affects_mana_capacity = True
    stat.make_dictionary_of_tagged_stats([stta])
    win = window(character=stat)
    print('###')
    print(*inspect.getmembers(win), sep='\n')

    win.show()
    sys.exit(a.exec())
    
    