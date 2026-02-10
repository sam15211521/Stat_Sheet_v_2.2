from math import ceil, log10
from timeit import default_timer as timer
from colorama import Fore, Back

class stat():
    def __init__(self, level):
        self._level= level
        self.previous_level = 0
        self.mana_requirement = 1
        self.total_mana = 0
    
    def __ge__(self, other):
        return self.level >= other.level
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self,level):
        self.previous_level = self.level
        self._level = level
        self.total_mana += self.mana_requirement
        self.calculate_next_mana_requirement()
    
    def increase_level(self):
        self.level += 1
        self.calculate_next_mana_requirement()
    
    def calculate_next_mana_requirement(self):
        rate = 1.008
        self.mana_requirement = ceil(rate ** self.level)
    

class con_mana(stat):
    def __init__(self, level):
        super().__init__(level)



class character():
    def __init__(self):
        self.level = stat(0)
        self.mana = stat(0)

        self.str = stat(0)
    
    def increase_level(self):
        self.level.level += 1
    
    def add_mana(self, ammount):
        self.mana += ammount
    
    def increas_stat_level(self, stat : stat):
        current_mana = self.mana.level
        level_up_requirement = stat.mana_requirement
        if current_mana >= level_up_requirement:
            stat.increase_level()
        else:
            print('cannot increase level')

    
    

ben = character()
ben.level = 5

kevin = character()
kevin.level = 5

print(ben.level == kevin.level)
#ben.increas_stat_level(ben.str)



