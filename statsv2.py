from statistics import mean
from math import floor, ceil, log
from mastery import basic, beginner, intermediate, expert, master

class Attribute():
    _attribute_dictionary = {}
    def __init__(self, name='', 
                 description= '', 
                 mana_multiplier =1,
                 mana_capacity_flag = False,
                 level =0):
        self.name = name
        self._level = level
        self.previous_level = 0
        self.effective_level = 0 #the level that will be shown on the screen
        
        self.mana_to_next_level = 1
        self.actual_mana_to_next_level =1
        self.total_mana_used = 0
        self.description = description

        self._base_power = 1
        
        self.mana_capacity_multiplier = mana_multiplier

        self._attribute_dictionary[self.name] = self
        self._affects_mana_capacity = mana_capacity_flag
        self.original_mana_multiplier = self.mana_capacity_multiplier
    
    
    #getter and setter function of _level
    @property
    def level(self):
        return self._level
   
    @level.setter
    def level(self, level):
        self.previous_level = self._level
        self._level = level
        self.calculate_base_power()
        self.calculate_capacity_multiplier()
        self.increase_total_mana_used()
        self.calculate_next_level_requirement()


    @property
    def affects_mana_capacity(self):
        return self._affects_mana_capacity

    @affects_mana_capacity.setter
    def affects_mana_capacity(self, flag):
        if isinstance(flag, bool):
            self._affects_mana_capacity = flag

    
    def calculate_capacity_multiplier(self):
        if self.affects_mana_capacity:
            self.mana_capacity_multiplier= round(
                self.original_mana_multiplier * 1.01 ** self.level,
                4)
    
    def increase_total_mana_used(self):
        self.total_mana_used += self.mana_to_next_level
    
    def calculate_next_level_requirement(self):
        self.actual_mana_to_next_level = self.actual_mana_to_next_level * (1.008) 
        self.mana_to_next_level = ceil(self.actual_mana_to_next_level)
    
    def calculate_base_power(self):
        self._base_power = round(1.01 ** self.level,2)
    
    def increase_level(self):
        self.level += 1
    
    def decrease_level(self):
        self.level -= 1

class Stat(Attribute):
    def __init__(self, 
                 name='', 
                 description='', 
                 mana_multiplier=1, 
                 mana_capacity_flag=False, 
                 level=0,
                 affects_character_level = False,
                 is_taggable = False,
                 is_parent= False,
                 child_stats={},
                 ):
        super().__init__(name, description, 
                         mana_multiplier, mana_capacity_flag, level)

        self.is_taggable = is_taggable
        self.affects_character_level = affects_character_level
        self._is_parent = is_parent
        self.child_stats = {}
        self._parent_stat : Stat = None
    
    
    @property
    def is_parent(self):
        return self._is_parent
    
    @is_parent.setter
    def is_parent(self, stat):
        if isinstance(stat, bool):
            self._is_parent = stat
        else:
              print(f'ERROR: {self.name}.is_parent Must be type <bool>')


    @property
    def parent_stat(self):
        return self._parent_stat
    
    @parent_stat.setter
    def parent_stat(self, parent):
        if isinstance(parent, Stat):
            self._parent_stat = parent
        else:
            print("ERROR parent stat needs to be class <Stat>")

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, level: int):
        self.previous_level = self.level
        if not self.is_parent:
            self._level = level
            if isinstance(self.parent_stat, Stat):
                self.calculate_parent_stat_level()
        else:
            self._level = floor(self.average_child_stat_levels())
            if isinstance(self.parent_stat, Stat):
                self.parent_stat.calculate_parent_stat_level()

        self.calculate_capacity_multiplier()
        self.calculate_base_power()

    def average_child_stat_levels(self):
        levels = [stat.level for stat in self.child_stats.values()]
        return mean(levels)

    
    def calculate_parent_stat_level(self):
        self.parent_stat.level = self.parent_stat.average_child_stat_levels()
    
    def add_child_stat(self, child_stat):
        if isinstance(child_stat, Stat):
            self.is_parent = True
            child_stat.parent_stat = self
            self.child_stats[child_stat.name] = child_stat
        else:
            print(f'\nThe added instance <{child_stat}> is not a class Stat\n')
    
class MajorStat(Attribute):
    def __init__(self, name='', discription='', mana_multiplier= 1, mana_capacity_flag=False):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag)
        self._mana_unit = None
    @property
    def mana_unit(self):
        return self._mana_unit
    @mana_unit.setter
    def mana_unit(self, unit):
        self._mana_unit = unit
    def __str__(self):
        if self.name == "Max Mana" or self.name == "Mana":
            return f"{self.name}: {self.level:,} {self.mana_unit}"
        else:
            return super().__str__()
    
class HiddenManaStat(Attribute):
    def __init__(self, name='', discription='', mana_multiplier=1, mana_capacity_flag=False):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag)
    
    def calculate_capacity_multiplier(self):
        return None
    

class CondensedMana(MajorStat):
    def __init__(self, name='', discription='', mana_multiplier=1,mana_capacity_flag=False):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag)
        self._power = 1

    @property
    def power(self):
        return self._power
    @power.setter
    def power(self, value):
        self._power = value
    
    def __str__(self):
        return_string = f"Con Mana: {self.level}"
        return return_string



class SkillStat(Attribute):
    # This stat holds all of the information and levels of the skills
    # Any skill created will be linked to in here
    def __init__(self, 
                 name='', 
                 description='', 
                 mana_multiplier=1, 
                 mana_capacity_flag=False, 
                 level=0):
        super().__init__(name, description, mana_multiplier, 
                         mana_capacity_flag, level)
        self.dict_of_skills = {}
        self._affects_character_level = True
    
    @property
    def affects_character_level(self):
        return self._affects_character_level
    @affects_character_level.setter
    def affects_character_level(self, flag):
        if isinstance(flag, bool):
            self._affects_character_level = flag

    # takes the amount of mana used on the skills in dict_of_skills and sets the 
    # level of the SkillStat based on it.
    
    def calculate_next_level_requirement(self):
        # original formula : 1 * 1.008 * level
        self.actual_mana_to_next_level =  1.008 ** self.level
        self.mana_to_next_level = ceil(self.actual_mana_to_next_level)

    
    def calculate_level(self):
        self.previous_level = self.level
        con_mana = 0   # the mana used to increase skills if more than
                            # self.total_mana_used, and more than 
                            # the leftover_mana is more than 
                            #self.mana_to_next_level then it need to level up
        for skill in self.dict_of_skills.values():
            skill: Skill
            con_mana += skill.total_mana_used
        
        level = 0
        mana_to_next_level = 0
        total_mana_used = 0
        while True:
            mana_to_next_level = ceil(1.008 ** level)
            if total_mana_used + mana_to_next_level <= con_mana:
                total_mana_used += mana_to_next_level
                level += 1
            else:
                self.level = level
                self.mana_to_next_level = mana_to_next_level
                self.total_mana_used = con_mana
                return
        
    

class Skill(Attribute):
    def __init__(self, 
                 name='', 
                 description='', 
                 mana_multiplier=1,
                 mana_capacity_flag=False, 
                 level=0,
                 tagged_stats = [],
                 stat_increase_multiplier=1):
        super().__init__(name, 
                         description, 
                         mana_multiplier,     
                         mana_capacity_flag, 
                         level)
        self._basics = False
        self.mastery = basic

        self.stats_to_tag = tagged_stats
        self.tagged_stats = {}
        self.make_dictionary_of_tagged_stats()

        self.stat_multiplier = self.mastery.multiplier
        self.stat_increase_multiplier = stat_increase_multiplier
        self.original_stat_increase_multiplier = stat_increase_multiplier
            # stat increase multiplier must be less than 1
        self.original_mana_multiplier = self.mana_capacity_multiplier
    
    @property
    def basics(self):
        return self._basics
    @basics.setter
    def basics(self, basics):
        if isinstance(basics, bool):
            self._basics = basics
            self.set_mastery()
            self.calculate_base_power()
        else:
            print(f'Error: {self.name}.basics.setter :\nthe value <{basics}> is not type bool')
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self.previous_level = self._level
        self._level = level
        self.increase_total_mana_used()
        self.set_mastery()
        self.calculate_base_power()
        self.calculate_next_level_requirement()
        self.calculate_capacity_multiplier()
        self.calculate_effective_skill_level()
        self.calculate_stat_multiplier()
    
    def calculate_effective_skill_level(self):
        #effective level is depended on mastery of the skill
        self.effective_level = self.level * self.mastery.multiplier

    def make_dictionary_of_tagged_stats(self, stats_to_tag=None):
        if not isinstance(stats_to_tag, list):
            tagging_stats = self.stats_to_tag
        elif isinstance(stats_to_tag, list):
            tagging_stats = stats_to_tag
        else:
            return
        for stat in tagging_stats:
            if isinstance(stat, Stat):
                self.tagged_stats[stat.name] = stat

    def calculate_base_power(self):
        self._base_power = 1.01 ** (self.level * self.mastery.multiplier)


    def calculate_stat_multiplier(self):
        if not self.tagged_stats:
            return
        else:
            multiplier = self.original_stat_increase_multiplier + 1
            leveled_multiplier = multiplier ** (self.level * 
                                                self.mastery.multiplier)
            self.stat_increase_multiplier = leveled_multiplier



    def set_mastery(self):
        if not self.basics:
            if self.level == 0:
                self.mastery = basic
            elif self.level > 0 and self.level <= 100:
                if self.mastery.name != beginner.name:
                    self.mastery = beginner
                    self.calculate_capacity_multiplier()
        else:
            if self.level == 0:
                if self.mastery.name != beginner.name:
                    self.mastery = beginner
                    self.calculate_capacity_multiplier()
            elif self.level > 0 and self.level <= 109:
                if self.mastery.name != intermediate.name:
                    self.mastery = intermediate
                    self.calculate_capacity_multiplier()
            elif self.level > 109 and self.level <= 1000:
                if self.mastery.name != expert.name:
                    self.mastery = expert
                    self.calculate_capacity_multiplier()
            elif self.level > 1001 and self.level <= 10000:
                if self.mastery.name != master.name:
                    self.master = master
                    self.calculate_capacity_multiplier()
            
    
    

    



if __name__ == '__main__':
    a = Skill('aba', stat_increase_multiplier=.8)
    a.affects_mana_capacity = True
    a.level = 33
    a.calculate_stat_multiplier()
    a.basics = True
    print(a.mastery)