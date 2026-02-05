from statsv2 import MajorStat, Stat ,Skill, SkillStat, CondensedMana, HiddenManaStat
import math

class Character():
    _dict_of_characters = {} 
    def __init__(self, 
                 name = '', 
                 race = '', 
                 body_mana_multiplier = None):
        self.dict_of_kills = {}
        self.dict_of_skills = {}
        self.dict_of_major_stats = {}
        self.dict_of_stats = {}
        self.dict_of_stats_affecting_level = {}
        self.dict_of_taggable_stats = {}
        self.mana_requirement_increaser = 1.008
        self.stat_strengthening_increaser = 1.01
        self.name = name
        self.race = race
        if body_mana_multiplier is None:
            self.body_mana_stat = 99798405
        else:
            self.body_mana_stat = body_mana_multiplier
        self._stats_and_skills_effecting_mana = {}
        
        # the major stats
        self.health = MajorStat("Health")
        self.max_health = MajorStat("Max Health")
        self.max_mana = MajorStat("Max Mana")
        self.current_mana = MajorStat("Mana")
        self.level = MajorStat("Level")
        self.condensed_mana = CondensedMana("Condensed Mana")
        self.total_condensed_mana = MajorStat("Total Condensed Mana")

        self.hidden_mana_stat = HiddenManaStat("Base Mana Capacity", 
                                           mana_capacity_flag=True,)
        self.hidden_mana_stat.level = self.body_mana_stat

                #regular stats
        
        #Strength
        self.strength = Stat(name = "Strength", 
                             is_parent=True, 
                             affects_character_level=True)
        self.physical_strength = Stat(name = "Physical Strength",
                                      is_taggable=True)
        self.magical_strength = Stat(name = "Mana Strength",
                                     mana_capacity_flag=True,
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
                                     mana_capacity_flag=True,
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
                              mana_capacity_flag=True,
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
                                    mana_capacity_flag=True,
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
        self.energy_potential = Stat(name= "Energy Potential", 
                                     mana_capacity_flag=True,
                                     mana_multiplier=1.01,
                                     affects_character_level=True)
        
        # Stat affected by all skills
        self.skill_stat = SkillStat(name = "Skills Level")
        

        
    
    def add_skill(self, skill):
        if isinstance(skill, Skill) and skill not in self.dict_of_skills:
            self.dict_of_skills[skill.name] = skill
            self.skill_stat.dict_of_skills[skill.name] = skill






if __name__ == '__main__':
    Ben = Character('Ben')
    bab = Skill('BaB')
    Ben.add_skill(bab)
    print(Ben.skill_stat.dict_of_skills, Ben.dict_of_skills, 
          sep='\n')