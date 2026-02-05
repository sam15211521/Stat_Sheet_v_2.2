
import sys
from functools import partial
import statsv2
from Characterv2 import Character
from statsv2 import *


from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                               QLabel, QVBoxLayout, QGridLayout)

class Window(QMainWindow):
    def __init__(self, character: SkillStat):
        super().__init__() 
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.subject = character
        self.labels = {}
        self.mastery_label = None
        
        self.skill_level_up_window = Skill_Window(character=character,
                                                  parent=self)
        
        self.add_to_layout()
        self.add_buttons()
        
        self.timer = None
        #self.set_timer()
        self.show()

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
    
    def update_all_labels(self):
        #print(self.subject.__dict__, self.labels, sep= '\n###\n', end='\n####\n')
        for name, label in self.labels.items():
            label.setText(f'{name} | {self.subject.__dict__[name]}')
    
    def add_buttons(self):
        self.close_button = QPushButton('Close')
        self.main_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.increase_level = QPushButton('Increase Skill Levels')
        self.main_layout.addWidget(self.increase_level)
        self.increase_level.clicked.connect(self.skill_level_up_window.show)
    
    def set_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(5000)

class Skill_Window(QMainWindow):
    def __init__(self, character: SkillStat, parent: Window):
        super().__init__() 
        self._parent = parent
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.subject = character
        self.labels = {}
        self.buttons = {}
        self.button_index = 1
        self.skills = {}

        self.exit_button = QPushButton("Close")
        self.exit_button.clicked.connect(self.close)
        
        
        self.add_to_layout()
        self.main_layout.addWidget(self.exit_button, self.button_index,0)

    def close_button(self):
        pass
          

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()

    def add_to_layout(self):
        title = QLabel('skill name | level')
        self.button_index = 1
        self.main_layout.addWidget(title, 0,0)
        for name, skill in self.subject.dict_of_skills.items():
            self.skills[name] = skill
            label = QLabel(f'{name} | {skill.level}')
            button = QPushButton('Increase Level')
            self.buttons[name] = button
            button.clicked.connect(partial(self.increase_skill_level, skill))
            self.labels[name] = label
            self.main_layout.addWidget(label,self.button_index, 0)
            self.main_layout.addWidget(button, self.button_index, 1)
            self.button_index += 1
    
    
    def increase_skill_level(self, skill: Skill):
        skill: Skill
        skill.increase_level()
        self._parent.subject.skill_changed_flag = True
        self.subject.calculate_level()
        self.update_all_labels()
    
    def update_all_labels(self, ):
        for name, label in self.labels.items():
            label:QLabel
            label.setText(f'{name} | {self.skills[name].level}')
            self._parent.update_all_labels()


if __name__ == "__main__":
    app = QApplication()
    
    skill1 = Skill(name='aba')
    skill2 = Skill(name='csds')
    
    print(skill1)
    
    skill_stat = SkillStat()
    skill_stat.dict_of_skills[skill1.name] = skill1
    skill_stat.dict_of_skills[skill2.name] = skill2
    

    window = Window(character=skill_stat)
    sys.exit(app.exec())