from statsv2 import (MajorStat, Stat ,Skill, 
                     SkillStat, CondensedMana, HiddenManaStat, 
                     Energy_Potential,)
from math import log10, log, floor, ceil 

from colorama import Fore
from timeit import default_timer as timer

class Character():
    _dict_of_characters = {} 
    def __init__(self, 
                 name = '', 
                 race = '', 
                 body_mana_multiplier = None):
        self.dict_of_kills = {}
        self.dict_of_skills = {}
        self.dict_of_major_stats = {}
        self.dict_of_minor_stats = {}
        self.dict_of_stats = {}
        self.dict_of_stats_affecting_level = {}
        self.dict_of_stats_affecting_health = {}
        self.dict_of_stats_affecting_mana = {}
        self.dict_of_taggable_stats = {}
        self.mana_requirement_increaser = 1.008
        self.stat_strengthening_increaser = 1.01
        self.name = name
        self.race = race
        if body_mana_multiplier is None:
            self.body_mana_stat = 99798405
        else:
            self.body_mana_stat = body_mana_multiplier
        
        # the major stats
        self.health = MajorStat("Health")
        self.max_health = MajorStat("Max Health")
        self.max_mana = MajorStat("Max Mana")
        self.current_mana = MajorStat("Mana")
        self.level = 0
        self._condensed_mana = CondensedMana("Condensed Mana")
        self.total_condensed_mana = CondensedMana("Total Condensed Mana")

        self.hidden_mana_stat = HiddenManaStat("Base Mana Capacity", 
                                           affects_mana=True,)
        self.hidden_mana_stat.level = self.body_mana_stat

                #regular stats
        
        #Strength
        self.strength = Stat(name = "Strength", 
                             is_parent=True, 
                             affects_character_level=True)
        self.physical_strength = Stat(name = "Physical Strength",
                                      is_taggable=True)
        self.magical_strength = Stat(name = "Mana Strength",
                                     affects_mana=True,
                                     mana_multiplier=1.001,
                                     is_taggable=True)
        self.strength.add_child_stat(self.physical_strength, 
                                     self.magical_strength)

        #Resistance
        self.resistance = Stat(name="Resistance", 
                               is_parent=True,
                               affects_character_level=True)
        self.physical_resistance = Stat(name="Physical Resistance",
                                     is_taggable=True)
        self.magic_resistance = Stat(name="Mana Resistance",
                                     affects_mana=True,
                                     mana_multiplier=1.001,
                                     is_taggable=True)
        self.spiritual_resistance = Stat(name="Spiritual Resistance",
                                     is_taggable=True)
        self.resistance.add_child_stat(self.physical_resistance,
                                       self.magic_resistance,
                                       self.spiritual_resistance)
        
        #Regeneration
        self.regeneration = Stat(name="Regeneration", 
                                 is_parent=True,
                                 affects_character_level=True)
        self.health_regen = Stat(name="Health Regeneration",
                                     is_taggable=True)
        self.mana_regen= Stat(name="Mana Regeneration",
                              affects_mana=True,
                              mana_multiplier=1.0001,
                                     is_taggable=True)
        self.regeneration.add_child_stat(self.health_regen,
                                         self.mana_regen)
        
        #Endurance
        self.endurance = Stat(name="Endurance", 
                              is_parent=True,
                              affects_character_level=True)
        self.physical_endurance = Stat(name="Physical Endurance",
                                     is_taggable=True)
        self.magic_endurance = Stat(name="Magic_Endurance",
                                    affects_mana=True,
                                    mana_multiplier=1.01,
                                     is_taggable=True)
        self.endurance.add_child_stat(self.physical_endurance,
                                      self.magic_endurance)
        
        #Agility
        self.agility = Stat(name="Agility", 
                            is_parent=True,
                            affects_character_level=True)
        self.speed = Stat(name="Speed",
                                     is_taggable=True)
        self.coordination = Stat(name="Coordination",
                                     is_taggable=True)
        self.agility.add_child_stat(self.speed, 
                                    self.coordination)
        
        #Energy potential
        self.energy_potential = Energy_Potential(name= "Energy Potential", 
                                     affects_mana=True,
                                     mana_multiplier=1.01,
                                     affects_character_level=True)
        
        # Stat affected by all skills
        self.skill_stat = SkillStat(name = "Skills Level")
        
        self.add_stats_to_dict_of_stats_and_major_stats()
        

    def add_skills(self, *skills):
        for skill in skills:
            self.add_skill(skill)
        
    
    def add_skill(self, skill):
        if isinstance(skill, Skill) and skill not in self.dict_of_skills:
            self.dict_of_skills[skill.name] = skill
            self.skill_stat.dict_of_skills[skill.name] = skill
    
    @property
    def skills(self):
        return self.dict_of_skills
    @property
    def kills(self):
        return self.dict_of_kills
    @property
    def taggable_stats(self):
        return self.dict_of_taggable_stats
    
    @property
    def major_stats (self):
        return self.dict_of_major_stats
    @property
    def minor_stats(self):
        return self.dict_of_minor_stats
    
    @property
    def stats_affecting_health(self):
        return self.dict_of_stats_affecting_health
    
    @property
    def stats_affecting_level(self):
        return self.dict_of_stats_affecting_level
    
    @property
    def stats_affecting_mana(self):
        return self.dict_of_stats_affecting_mana
    
    @property
    def condensed_mana(self):
        return self._condensed_mana
    
    @condensed_mana.setter
    def condensed_mana(self, value):
        self._condensed_mana = value

    
   ########################################################

    def print_character_levels(self):
        print('level: ', self.level)
        for stat in self.stats_affecting_level.values():
            stat: Stat
            print(stat.name, stat.effective_level)
   # Methods to increase levels
    def increase_con_mana(self, value):
        self.condensed_mana.level += value
        self.total_condensed_mana.level += value
        self.calculate_character_level()

    def calculate_character_level(self):
        self.level = floor(log((1.008-1) * self.total_condensed_mana.level/7 + 1, 
                          1.008))

    def increase_stat_level(self, stat: Stat):
        stat.increase_level()

    def increase_skill_level(self, skill: Skill):
        skill.increase_level()
        self.calculate_stat_skill_level()

    def calculate_stat_skill_level(self):
        self.skill_stat.calculate_level()

    # Methods to determine if a level can be increased based on mana

    def increase_stat_level(self):
        useable


    


    
    def add_stats_to_dict_of_stats_and_major_stats(self):
        for stat in self.__dict__.values():
            self.add_new_stat(stat)
    
    def add_new_stat(self, stat):
        if isinstance(stat, MajorStat):
            self.dict_of_stats[stat.name] = stat
            self.dict_of_major_stats[stat.name] = stat
            self.add_major_stats_to_dict_of_major_stats(stat)
        elif isinstance(stat, Stat) and not stat.is_parent: 
            self.dict_of_stats[stat.name] = stat
            self.dict_of_taggable_stats[stat.name] = stat
            self.dict_of_minor_stats[stat.name] = stat
            self.determining_stats_affect(stat=stat)
        elif isinstance(stat, Stat) and stat.is_parent:
            self.dict_of_stats[stat.name] = stat
            self.dict_of_minor_stats[stat.name] = stat
            self.determining_stats_affect(stat=stat)
        elif isinstance(stat, HiddenManaStat):
            self.dict_of_stats[stat.name] = stat
            #not part of affects mana as it does a slightly different part
        elif isinstance(stat, (SkillStat,Energy_Potential)):
            self.dict_of_stats[stat.name] = stat
            self.dict_of_minor_stats[stat.name] = stat
            self.dict_of_stats_affecting_level[stat.name] = stat
            # also not part of affects mana as it causes another change
    
    def determining_stats_affect(self, stat:Stat):
        self.determine_if_stat_affects_health_level(stat)
        self.determine_if_stat_affects_level(stat)
        self.determine_if_stat_affects_mana_level(stat)
        
   ############################################################## 
   # These methods only really occur with determining_stats_affect
   # I decided to write them here just to help me with readability
    def determine_if_stat_affects_mana_level(self, stat: Stat):
        if stat.affects_mana:
            self.dict_of_stats_affecting_mana[stat.name] = stat
    
    def determine_if_stat_affects_health_level(self, stat: Stat):
        if stat.affects_health:
            self.dict_of_stats_affecting_health[stat.name] = stat
            
    def determine_if_stat_affects_level(self, stat: Stat):
        if stat.affects_character_level:
            self.dict_of_stats_affecting_level[stat.name] = stat

    def add_major_stats_to_dict_of_major_stats(self, stat: Stat):
        self.dict_of_major_stats[stat.name] = stat
    #############################################################
    def print_dict_items(self):
        print(Fore.CYAN+'skills'+Fore.RESET)
        print(self.dict_of_skills)
        print(Fore.CYAN+'stats'+Fore.RESET)
        print(*[(name, stat) for name, stat in self.dict_of_stats.items()], 
              sep='\n')

        print(Fore.CYAN+'major stats'+Fore.RESET)
        print(*[(name, stat) for name, stat in self.dict_of_major_stats.items()], 
              sep='\n')

        print(Fore.CYAN+'minor stats'+Fore.RESET)
        print(*[(name, stat) for name, stat in self.dict_of_minor_stats.items()], 
              sep='\n')

        print(Fore.CYAN+'stats affecting level'+ Fore.RESET)
        print(*[(name, stat) for name, stat in self.dict_of_stats_affecting_level.items()], 
              sep='\n')

        print(Fore.CYAN+'taggable stats'+Fore.RESET)
        print(*[(name, stat) for name, stat in self.dict_of_taggable_stats.items()], 
              sep='\n')
        


if __name__ == '__main__':
    ben = Character('Ben')
    bab = Skill('BaB', tagged_stats=['Energy Potential'])
    mathematics = Skill("Math", tagged_stats=['Mana Regeneration', 'Mana Strength'])
    ben.add_skills(bab, mathematics)
    ben.increase_con_mana(200)
    ben.print_character_levels()
    print(ben.condensed_mana.level)
    print(ben.total_condensed_mana.level)
    



    # in this system, levels are all based on mana... why then should the level
    #  of the character be based on the average of all levels... why not
    #  make the level of a character be based on how much mana the character
    #  has? but... expecially if the con mana that is absorbed is based on how
    #  much ... yep I am soled
    # average = sum(n+m) / len(m->n)
    # level =  len(m->n) * 