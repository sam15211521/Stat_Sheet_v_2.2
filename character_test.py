
import sys
import statsv2
from Characterv2 import Character
from statsv2 import *

from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                               QLabel, QVBoxLayout)

class Window(QMainWindow):
    def __init__(self, character: Character):
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
            if not isinstance(attribute, (Stat, MajorStat, SkillStat)):
                if name[:4] != 'dict':
                    label = QLabel(f'{name} | {attribute}')
                    self.labels[name] = label
                    self.main_layout.addWidget(label)
                
            else:
                label = QLabel(f'{name} | {attribute.level}')
                self.labels[name] = label
                self.main_layout.addWidget(label)
    
    def update_all_labels(self):
        for name, label in self.labels.items():
            if not isinstance(self.subject.__dict__[name], 
                              (Stat, MajorStat, SkillStat)):
                label.setText(f'{name} | {self.subject.__dict__[name]}')
            else:
                label.setText(f'{name} | {self.subject.__dict__[name].level}')
    
    def add_buttons(self):
        self.close_button = QPushButton('Close')
        self.main_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.increase_level_button = QPushButton('Increase Level')
        self.main_layout.addWidget(self.increase_level_button)
        self.increase_level_button.clicked.connect(self.increase_level)
        

        #######self.increase_level.clicked.connect()#########
    
    def increase_level(self):
        self.subject.physical_endurance.increase_level()
        self.update_all_labels()
    
    def set_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(5000)

if __name__ == "__main__":
    app = QApplication()
    
    ben = Character('Ben', 'human')

    window = Window(ben)
    window.show()
    sys.exit(app.exec())