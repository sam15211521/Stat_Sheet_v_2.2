import os
import random
from sys import exit as sys_exit
import pickle
#from characters.ben import ben, cat
from Character import Character
from stats import Skill, Stat, SkillStat
from windows import MainWindow 
from PySide6.QtWidgets import QApplication
from datetime import datetime
cur_path = os.path.dirname(__file__)
file_path = 'characters/ben.dat'
abs_file_path = os.path.join(cur_path, file_path)

def clearscreen():
    os.system('cls')
####################
ben = Character(name="Ben", body_mana_multiplier=4939.519725)

#print(ben.skills_level.dict_of_skills)
#ben.add_skill(Skill('Energy Circulation',
#                    stat_increase_multiplier=0.0003,
#                    tagged_stats=[ben.magical_strength,
#                                  ben.energy_potential,
#                                  ben.mana_regen]))
ben.add_condensed_mana(50)
#ben.add_skill(Skill('Energy Conversion', stat_increase_multiplier=0.0003))
#ben.add_skill(Skill('Mana Shot'))
#ben.add_skill(Skill('Energy Channeling', stat_increase_multiplier=0.0002))
#ben.add_skill(Skill('Mana Condensing'))
#ben.add_skill(Skill('Fast Thought'))
#ben.add_skill(Skill('Acrobatics'))
#ben.add_skill(Skill('Sprinting'))


#print(ben.dict_of_skills)

#info = Character()
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
    #clearscreen()
    #app = QApplication()
    #window = MainWindow('ex')
    #window.show()
    #sys_exit(app.exec())
    save()
    person = load()
    a = datetime.now()
    a_string = f"{a.year}_{a.month}_{a.day}_{a.hour}_{a.minute}_{a.second}"
    print(a_string)
    #print(person)
    #for stat in ben.dict_of_stats.values():
    #    stat : Stat
    #    if not isinstance(stat,SkillStat):
    #        print(stat.name, stat.level, stat.effective_level, sep=' | ')
    #print(ben.dict_of_skills['Energy Circulation'].tagged_stats)
    #print(person.skills_level.dict_of_skills)


if __name__ == "__main__":
    main()
