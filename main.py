import os
import sys
import pickle
from Character import Character
from windows import MainWindow 
from PySide6.QtWidgets import QApplication

cur_path = os.path.dirname(__file__)
file_path = 'characters/ben.dat'
abs_file_path = os.path.join(cur_path, file_path)

def clearscreen():
    os.system('cls')
####################
ben = Character(name="Ben", body_mana_multiplier=4939.519725)

def save():
    with open(abs_file_path, 'wb') as File:
        #print(ben.skills_level.dict_of_skills)
        pickle.dump(ben, File)

def load():
    global info  
    with open(abs_file_path, "rb") as File:
        info = pickle.load(File)
        return info


def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
