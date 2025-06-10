from statistics import mean
from math import floor, ceil
from mastery import basic, beginner, intermediate, expert, master

# all classes need a: name, mana_to_next_level, total_mana_invested, power, discription

class Attribute():
    _attribute_dictionary = {}
    def __init__(self, name='', 
                 discription= '', 
                 mana_multiplier =1,
                 mana_capacity_flag = False,
                 level =0):
        self._name = name
        self._level = level
        
        self._mana_to_next_level = 1
        self._actual_mana_to_next_level =1
        self._total_mana_used = 0
        
        self._discription = discription

        self._power = 1
        
        self._mana_capasity_multiplier = mana_multiplier

        self._attribute_dictionary[self._name] = self
        self._affects_mana_capacity = mana_capacity_flag
        self.original_mana_multiplier = self.mana_capasity_multiplier
        
    
    def __str__(self):
        line1 = f"{self.name} | Level: {self.level:,} "
        line2 = f"mana to next level: {self._mana_to_next_level}"
        line3 = self.discription
        return "\n".join([line1, line2, line3])
    
    
    #getter and setter functions of _name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    #getter and setter function of _level
    @property
    def level(self):
        return self._level
   
    @level.setter
    def level(self, level):
        self._level = level
        #self.power = 1 *(1.01 ** self.level)
        self.calculate_capacity_multiplier()
   
    #getter and setter functions of _mana_to_next_level
    @property
    def mana_to_next_level(self):
        return self._mana_to_next_level
    
    @mana_to_next_level.setter
    def mana_to_next_level(self, mana):
        self._mana_to_next_level = mana
    
    @property
    def actual_mana_to_next_level(self):
        return self._actual_mana_to_next_level
    @actual_mana_to_next_level.setter
    def actual_mana_to_next_level(self, value):
        self.mana_to_next_level = ceil(value)
        self._actual_mana_to_next_level = value 

    #getter and setter functions of _total_mana_used
    @property
    def total_mana_used(self):
        return self._total_mana_used
   
    @total_mana_used.setter
    def total_mana_used(self, mana):
        self._total_mana_used = mana
    
    #getter and setter funcitons of _power
    
    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, power):
        self._power = power
    
    #getter and setter of the discription
    @property
    def discription(self):
        return self._discription
    
    @discription.setter
    def discription(self, discription):
        self._discription = discription

    #gets the number of diffrent attributes
    @property
    def number_of_attributes(self):
        return self._attribute_dictionary
    
    @property
    def mana_capasity_multiplier(self):
        return self._mana_capasity_multiplier

    @mana_capasity_multiplier.setter
    def mana_capasity_multiplier(self, value):
        self._mana_capasity_multiplier = value
    
    @property
    def affects_mana_capacity(self):
        return self._affects_mana_capacity
    @affects_mana_capacity.setter
    def affects_mana_capacity(self, flag):
        if isinstance(flag, bool):
            self._affects_mana_capacity = flag
    
    def calculate_capacity_multiplier(self):
        #need an initial value based on the type of skill
        # will be multiplied by level
        if self.affects_mana_capacity:
            self.mana_capasity_multiplier= round(self.original_mana_multiplier * 1.01 ** self.level,4)

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
    
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level
        
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
        return_string = f"Con Mana: {self.level:,}"
        return return_string

class Stat(Attribute):
    def __init__(self, 
                 name='',
                 discription='', 
                 isparent = False,
                 childstats = {},
                 mana_multiplier=1, 
                 mana_capacity_flag=False,
                 level = 0,
                 affects_character_level = False,
                 is_taggable = False
                 ):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag, level)
        
        self._acronym = self.name[:3].upper()
        self._is_taggable = is_taggable

        self._isparent = isparent
        self._child_stats = {}
        self._parent_stat = None
        self._power = 1
        self._affects_character_level = affects_character_level
        self._effective_level = 0
        self._skills_effecting_stat ={}
    @property
    def effective_level(self):
        return self._effective_level
    @effective_level.setter
    def effective_level(self, level):
        self._effective_level = level 
    
    @property
    def skills_effecting_stats(self):
        return self._skills_effecting_stat
    @skills_effecting_stats.setter
    def skills_effecting_stats(self, skill):
        self._skills_effecting_stat[skill] = skill

    
    @property
    def affects_character_level(self):
        return self._affects_character_level
    @affects_character_level.setter
    def affects_character_level(self, bloo):
        self._affects_character_level = [bloo]
    
    @property
    def isparent(self):
        return self._isparent
    
    @isparent.setter
    def isparent(self, stat):
        if isinstance(stat, bool):
            self._isparent = stat
        else:
              print(f'ERROR: {self.name}.isparent Must be type <bool>')
    
    @property
    def child_stats(self):
        return self._child_stats
    
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
    def power(self):
        return self._power
    @power.setter
    def power(self, power):
        self._power = round(1.01 ** self.level, 2)

    @property
    def level(self):
        if self.isparent:
            #self._level = floor(self.average_values())
            return self._level
        else:
            return self._level
    
    @ level.setter
    def level(self, level=None):
        if not self.isparent:
            self._level = level
            self.power = None
            if isinstance(self.parent_stat, Stat):
                self.parent_stat.level = None #just need it to equal to something
        else:
            self._level = floor(self.average_levels())
            #self.effective_level = floor(self.average_effective_levels())
            if isinstance(self.parent_stat, Stat):
                self.parent_stat.level = None
                self.power = None
        self.calculate_capacity_multiplier()

    
    def add_child_stat(self, *args):
        for stat in args:
            if isinstance(stat, Stat):
                self.isparent = True
                stat.parent_stat = self
                self._child_stats[stat.name] = stat
            else:
                print(f'\nThe added instance <{stat}> is not a class Stat\n')
    
    
    def print_child_stats(self):
        #print(f'the Child Stats of {self.name} are:')
        if self.child_stats == {}:
            print(f"\n{self.name} has no Child Stats\n")
        #else:
            #for name, stat in self.child_stats.items():
                #print(f'Name: {name}, Level: {stat.level}')
    
    # used to calculate the level of a parent stat based on 
    # the average of the levels of the childstats
    def average_levels(self):
        levels = []
        for name, stat in self.child_stats.items():
            levels.append(stat.level)
        #print(levels)
        return mean(levels)

    def average_effective_levels(self):
        effectivelevels = []
        for name, stat in self.child_stats.items():
            #print(stat.name, stat.level, "@@@@@@@@@@@@@@@@@")
            stat: Stat
            effectivelevels.append(stat.effective_level)
        #print('effective',effectivelevels)
        #print('parent stat average level:',mean(effectivelevels))
        self.effective_level = floor(mean(effectivelevels))
        #return mean(effectivelevels)
    
    def level_overide(self, level_increase):
        pass

class Skill(Attribute):
    def __init__(self, 
                 name='', 
                 discription='', 
                 mana_multiplier=1, 
                 mana_capacity_flag=False, 
                 level=0,
                 tagged_stats = [],
                 stat_increase_multiplier=0):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag, level)
        self._basics = False
        self._mastery = basic
        self._stats_to_tag = tagged_stats
        self._tagged_stats = {}
        self._stat_increase_multiplier = stat_increase_multiplier
        self._stat_multiplier = self.mastery.multiplier
        self.original_mana_multiplier = self.mana_capasity_multiplier
    @property
    def tagged_stats(self):
        return self._tagged_stats
    @tagged_stats.setter
    def tagged_stats(self, dic):
        self._tagged_stats = dic
    

    @property
    def stat_multiplier(self):
        return self._stat_multiplier
    @stat_multiplier.setter
    def stat_multiplier(self, value):
        self._stat_multiplier = value
    
    @property
    def level(self):
        return self._level
   
    @level.setter
    def level(self, level):
        self._level = level
        self.power = None
        self.mastery= None
        self.calculate_capacity_multiplier()
        self.calculate_stat_multiplier()
    
    @property
    def basics(self):
        return self._basics
    @basics.setter
    def basics(self, basics):
        if isinstance(basics, bool):
            self._basics = basics
        else:
            print(f'Error: {self.name}.basics.setter :\nthe value <{basics}> is not type bool')
    
    @property
    def mastery(self):
        return self._mastery
    
    @mastery.setter
    def mastery(self, mastery):
        if not self.basics:
            if self.level == 0:
                self._mastery = basic
            elif self.level > 0 and self.level <= 100:
                if self.mastery.name != beginner.name:
                    self._mastery = beginner
                    self.calculate_capacity_multiplier()
        else:
            if self.level == 0:
                if self.mastery.name != beginner.name:
                    self._mastery = beginner
                    self.calculate_capacity_multiplier()
            elif self.level > 0 and self.level <= 109:
                if self.mastery.name != intermediate.name:
                    self._mastery = intermediate
                    self.calculate_capacity_multiplier()
            elif self.level > 109 and self.level <= 1000:
                if self.mastery.name != expert.name:
                    self._mastery = expert
                    self.calculate_capacity_multiplier()
            elif self.level > 1001 and self.level <= 10000:
                if self.mastery.name != master.name:
                    self._master = master
                    self.calculate_capacity_multiplier()
    
    def calculate_stat_multiplier(self):
        # statincrease_multi ** (level *mastery_multiplier) 
        if self._stat_increase_multiplier >= 1:
            return
        else:
            self.stat_multiplier = round((1 + (self._stat_increase_multiplier * self.mastery.multiplier)) **(self.level), 8)
        
            
    
    def calculate_capacity_multiplier(self):
        #need an initial value based on the type of skill
        # will be multiplied by level
        #mastery multiplier will 
        
        if self.affects_mana_capacity:

            self.mana_capasity_multiplier = round(self.original_mana_multiplier * 1.001 ** (self.level* self.mastery.multiplier),2)
            #print(self.name, self.mana_capasity_multiplier, sep=' | ')


class SkillStat(Attribute):
    def __init__(self, name='', 
                 discription='', 
                 mana_multiplier=1, 
                 mana_capacity_flag=False, 
                 level=0,
                 affects_character_level=False):
        super().__init__(name, discription, mana_multiplier, mana_capacity_flag, level)
        self._dict_of_skills = {} 
        self._affects_character_level = affects_character_level
    
    @property
    def dict_of_skills(self):
        return self._dict_of_skills
    @dict_of_skills.setter
    def dict_of_skills(self, value):
        self._dict_of_skills = value
    
    @property
    def abc(self):
        return self._abc
    @abc.setter
    def abc(self, value):
        self._abc = value
    
    @property
    def affects_character_level(self):
        return self._affects_character_level
    @affects_character_level.setter
    def affects_character_level(self, flag):
        if isinstance(flag, bool):
            self._affects_character_level = flag

   
   
    # takes the amount of mana used on the skills in dict_of_skills and sets the 
    # level of the SkillStat based on it.
    def calculate_level(self):
        amount_of_mana = 0
        for skill in self.dict_of_skills.values():
            amount_of_mana += skill.total_mana_used
        self.total_mana_used = amount_of_mana

        actual_current_level_cost = self.actual_mana_to_next_level
        shown_current_level_cost = ceil(actual_current_level_cost)

        while actual_current_level_cost <= amount_of_mana:
            self.level += 1
            amount_of_mana -= ceil(actual_current_level_cost)
            actual_current_level_cost = actual_current_level_cost * (1.008 ** self.level)
        self.actual_mana_to_next_level = actual_current_level_cost
        self.mana_to_next_level = shown_current_level_cost
        
        

        
        
        
    def increase_next_level_requirement(self, stat: Stat | Skill, level):
        next_actual_level_requirement = stat.actual_mana_to_next_level * (1.008 ** level)
        stat.actual_mana_to_next_level = next_actual_level_requirement
