from stats import MajorStat, Stat ,Skill, SkillStat, CondensedMana, HiddenManaStat
import math

class Character():
    _dict_of_characters = {} 
    def __init__(self, 
                 name = '', 
                 race = '', 
                 body_mana_multiplier = None):
        self._dict_of_kills = {}
        self._dict_of_skills = {}
        self._dict_of_major_stats = {}
        self._dict_of_stats = {}
        self._dict_of_stats_affecting_level = {}
        self._dict_of_taggable_stats = {}
        self._mana_requirement_increaser = 1.008
        self._stat_strengthening_increaser = 1.01
        self._name = name
        self._race = race
        if body_mana_multiplier is None:
            self._body_mana_stat = 99798405
        else:
            self._body_mana_stat = body_mana_multiplier

        self._stats_and_skills_effecting_mana = {}

        # the major stats
        self._health = MajorStat("Health")
        self._max_health = MajorStat("Max Health")
        self._max_mana = MajorStat("Max Mana")
        self._current_mana = MajorStat("Mana")
        self._level = MajorStat("Level")
        self._condensed_mana = CondensedMana("Condensed Mana")
        self._total_condensed_mana = MajorStat("Total Condensed Mana")

        self._hidden_mana_stat = HiddenManaStat("Base Mana Capacity", 
                                           mana_capacity_flag=True,)
        self.hidden_mana_stat.level = self._body_mana_stat
        #print("ben hidden mana stat:", 
              #body_mana_multiplier,
              #self._body_mana_stat,
              #self.hidden_mana_stat.level, 
              #sep= ' | ')
        

        #regular stats
        
        #Strength
        self.strength = Stat(name = "Strength", 
                             isparent=True, 
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
                               isparent=True,
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
                                 isparent=True,
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
                              isparent=True,
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
                            isparent=True,
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
        self.skills_level = SkillStat(name = "Skills Level",
                                      affects_character_level=True)

        self.add_stat_to_mana_calc(
                                   self.magic_endurance,
                                   self.magic_resistance,
                                   self.magical_strength,
                                   self.mana_regen,
                                    )
        self.calculate_max_mana()
        self.current_mana.level = self.max_mana.level
        self.add_to_dict_stats_and_major_stats()
        #print(self._dict_of_taggable_stats)
    
    def __str__(self):
        string = f"""
{self.name} | {self.level.name}: {self.level.level}| {self.condensed_mana.name}: {self.condensed_mana.level}
{self.health.name}: {self.health.level}/{self.max_health.level} | Mana: {self.current_mana.level}/{self.max_mana.level}
{self.resistance.name}: {self.resistance.level} | {self.strength.name}: {self.strength.level}
{self.regeneration.name}: {self.regeneration.level} | {self.endurance.name}: {self.endurance.level}
{self.energy_potential.name}: {self.energy_potential.level} | {self.agility.name}: {self.agility.level}
"""
        return string
    
    def __repr__(self):
        string = f' {self.__dir__()}\n{self.name}\n'
        
        for key, item in self.__dict__.items():
            if isinstance(item,Stat) or isinstance(item,MajorStat):
                string += f'({item.name}, {item.level})\n'
        return string



   ##########################################################
   # here are all the propertie setters 
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def dict_of_characters(self):
        return self._dict_of_characters
    @dict_of_characters.setter
    def dict_of_characters(self, dictionary):
        if isinstance(dictionary, dict):
            self._dict_of_kills = dictionary
        else: 
            print(f"dictionary of characters must be class <dict>")
    
    @property
    def dict_of_kills(self):
        return self._dict_of_kills
    @dict_of_kills.setter
    def dict_of_character(self, name):
        self._dict_of_kills = name
    @property
    def dict_of_stats(self):
        return self._dict_of_stats
    @dict_of_stats.setter
    def dict_of_stats(self, dict):
        self._dict_of_stats = dict
    
    @property
    def dict_of_major_stats(self):
        return self._dict_of_major_stats
    @dict_of_stats.setter
    def dict_of_major_stats(self, dict):
        self._dict_of_major_stats = dict
    
    @property
    def mana_requirement_increaser(self):
        return self._mana_requirement_increaser
    @mana_requirement_increaser.setter
    def mana_requirement_increaser(self, value):
        self._mana_requirement_increaser = value
    
    @property
    def stat_strength_increaser(self):
        return self._stat_strengthening_increaser
    @stat_strength_increaser.setter
    def stat_strength_increaser(self, value):
        self._stat_strengthening_increaser = value


    @property
    def race(self):
        return self._race
    @race.setter
    def race(self, name):
        self._race = name
    
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, health):
        self._health = health
    
    @property
    def max_health(self):
        return self._max_health
    @max_health.setter
    def max_health(self, health):
        self._max_health = health

    @property
    def max_mana(self):
        return self._max_mana
    @max_mana.setter
    def max_mana(self, mana):
        self._max_mana = mana
    
    @property
    def current_mana(self):
        return self._current_mana
    @current_mana.setter
    def current_mana(self, mana):
        self._current_mana = mana

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level

    @property
    def condensed_mana(self):
        return self._condensed_mana
    @condensed_mana.setter
    def condensed_mana(self, mana):
        self.total_condensed_mana += mana
        self._condensed_mana = mana
    
    @property
    def total_condensed_mana(self):
        return self._total_condensed_mana
    @total_condensed_mana.setter
    def total_condensed_mana(self, mana):
        self._total_condensed_mana = mana
    @property
    def hidden_mana_stat(self):
        return self._hidden_mana_stat
    @hidden_mana_stat.setter
    def hidden_mana_stat(self, mana):
        self._hidden_mana_stat = mana

    @property
    def stats_and_skills_effecting_mana(self):
        return self._stats_and_skills_effecting_mana
    @stats_and_skills_effecting_mana.setter
    def stats_and_skills_effecting_mana(self, stat):
        self._stats_and_skills_effecting_mana = stat
    
    @property
    def dict_of_skills(self):
        return self._dict_of_skills
    @dict_of_skills.setter
    def dict_of_skills(self, value):
        self._dict_of_skills = value
        self.skills_level.dict_of_skills = value

    @property
    def template(self):
        return self._template
    @template.setter
    def template(self, mana):
        self._template = mana
    
    ###########################################################
    #calculating character level
    def calculate_character_level(self):
        #print('\n got into the character_level\n')
        #self.skills_level.calculate_level()
        #takes the average of all the levels to determine the character level
        temp_level = self.level.level
        sum_of_levels = 0
        num_of_levels = len(self._dict_of_stats_affecting_level)
        for stat in self._dict_of_stats_affecting_level.values():
            #print(stat.name, stat.level)
            sum_of_levels += stat.level
        
        temp_level = math.floor(sum_of_levels / num_of_levels)
        #print('temp level:', temp_level)

        self.level.level = temp_level
    #other misc methods
    
    def add_skill(self, skill):
        if isinstance(skill, Skill):
            if skill not in self._dict_of_skills:
                self.determine_tagged_stats(skill=skill)
                self._dict_of_skills[skill.name] = skill
                self.skills_level.dict_of_skills[skill.name] = skill
                #self.increase_skill_level(skill,100)
                self.calculate_character_level()
                self.calculate_effective_stat_level()
                if skill.affects_mana_capacity:
                    self.add_skill_to_mana_calc(skill)
                #print(skill.stat_multiplier)
    def determine_tagged_stats(self, skill):
        skill: Skill
        for stat in skill._stats_to_tag:
            stat: Stat
            skill.tagged_stats[stat.name] = stat
            stat.skills_effecting_stats[skill.name] = skill
    
    def calculate_effective_stat_level(self):
        for stat in self._dict_of_taggable_stats.values():
            stat : Stat
            stat_multiplier = 1
            for skill in stat.skills_effecting_stats.values():
                stat_multiplier *= skill.stat_multiplier
                #print(stat.name, stat_multiplier, sep= '\n')
            stat.effective_level = math.floor(stat.level * stat_multiplier)
            if stat._isparent:
                stat.average_effective_levels()


            
    def use_condensed_mana(self, amount):
        self.condensed_mana.level -= amount

    def add_condensed_mana(self, amount):
        self.condensed_mana.level += amount
    
    def kills_character(self, killed):
        if isinstance(killed, Character):
            mana_added = killed.level.level * 1.0001**self.energy_potential.level
            self._dict_of_kills[f"{killed.name}: lvl. {killed.level}"] = (killed, mana_added)
            self.add_condensed_mana(mana_added)
    
    def add_skill_to_mana_calc(self, *args):
        for skill in args:
            if isinstance(skill, Skill):
                self.stats_and_skills_effecting_mana[skill.name] = skill
                self.calculate_max_mana()

    def add_stat_to_mana_calc(self, *args):
        for stat in args:
            if isinstance(stat, Stat):
                self.stats_and_skills_effecting_mana[stat.name] = stat
                self.calculate_max_mana()
        
        
    
    def calculate_max_mana(self):
        #max mana is based on first the body's iniate abilities
        #average is 2 
        #max mana based on the <hidden>, <magic_resistance>,
        #<magic_endurance>, <magic_regeneration>, <Energy Potential>
        #and misc skills that will add to the calculation. 
        #average mana capacity of a person is 100 Mp 100,000,000 p
        #a person with a mana deficiency has a capacity of 1 -5 Mp
        #ben is 5000 p
        #numbers got crazy with exponential so now lets try 
        # hiden * (stat_multiplier ** stat_multiplier.energy potential)
        # average person's hidden stat needs to multiply to this: 54433106
        stat_skill_multipliers = []
        
        for stat_skill in self.stats_and_skills_effecting_mana.values():
        #    print(stat_skill.name, stat_skill.mana_capasity_multiplier, sep=' :: ')
            stat_skill_multipliers.append(stat_skill.mana_capasity_multiplier)
        #print(stat_skill_multipliers)
        mana_multiplier = math.prod(stat_skill_multipliers)
        mana_capacity = math.floor((self.hidden_mana_stat.level * (mana_multiplier** self.energy_potential.mana_capasity_multiplier)))
        #print('capacity  = hidden * multipliers ** potential')
        #print(f"{mana_capacity} = ({self.hidden_mana_stat.level} * ({mana_multiplier} ** {self.energy_potential.mana_capasity_multiplier}))")
        #print()
        

        if mana_capacity >1000000:
            mana_capacity/= 1000000
            self.max_mana.mana_unit = "Mp"
            self.current_mana.mana_unit = "Mp"
        elif mana_capacity <1000000 and mana_capacity >=20000:
            mana_capacity /= 1000
            self.max_mana.mana_unit ="kp"
            self.current_mana.mana_unit = "kp"
        elif mana_capacity < 20000:
            self.max_mana.mana_unit = "p"
            self.current_mana.mana_unit = "p"
        self.max_mana.level = math.floor(mana_capacity)

        #print(self.max_mana.level, self.max_mana.mana_unit)

        #self.max_mana.level = math.floor(mana_capacity)


        
        #print(stat_skill_multipliers)
        #print('hidden', self.hidden_mana_stat.level)
        #print("EP", self.energy_potential.mana_capasity_multiplier)
        #print('multiplicitive:',mana_multiplier)
        #print(f"mana capacity: {mana_capacity:,} {self.max_mana.mana_unit}")
    

    #stat should be the of the Stat class
    # level should only be an integer
    def add_to_dict_stats_and_major_stats(self, major_stat = False):
        if major_stat:
            if not bool(self._dict_of_major_stats):

                temp = [stat for stat in list(self.__dict__.values()) 
                        if isinstance(stat, Stat) | isinstance(stat, CondensedMana)]

                for stat in temp:
                    self._dict_of_major_stats[stat.name] = stat
        else:
            if not bool(self.dict_of_stats):

                temp = [stat for stat in list(self.__dict__.values()) 
                        if (isinstance(stat, Stat) |
                            isinstance(stat, CondensedMana) | 
                            isinstance(stat, SkillStat))]

                for stat in temp:
                    if stat.name == "Condensed Mana":
                        continue
                    elif stat.affects_character_level:
                        self._dict_of_stats_affecting_level[stat.name] = stat
                    self.dict_of_stats[stat.name] = stat
                
                for stat in self.dict_of_stats.values():
                    if isinstance(stat, Stat) and stat._is_taggable:
                        self._dict_of_taggable_stats[stat.name] = stat






### Need to edit the way that a stat level is increased and decreased as it is confusing and prone to mistakes due to calculating the level first
    #this function checks if the stat is a Stat or Skill then calls a function to increas the stat level
    def increase_stat_or_skill_level(self, stat, level=1):
        #print(stat.name,  "############")
        quit_flag = False
        if not isinstance(stat, Stat) and not isinstance(stat, Skill):
            print( "Type Error: selected stat is not a type <Stat> or <Skill>.")
            print(f"is type {type(stat)}")
            quit_flag = True
        if not isinstance(level, int):
            print( "Type Error: level can only increase by integer values")
            quit_flag = True
        if quit_flag:
            return False
        else:
            if stat.name in self.dict_of_stats:
                if not stat.isparent:
                    self.increase_stat_level(stat=stat, level=level)
                else:
                    self.increase_stat_level(stat=stat, level=level)

            elif stat.name in self.skills_level.dict_of_skills:
                self.increase_skill_level(skill=stat, level = level)
            self.calculate_max_mana()
            self.calculate_effective_stat_level()
            #for stats in self.dict_of_stats.values():
                #stats : Stat
    
    def check_if_con_mana_more_than_stat(self,skill_stat: Skill | Stat):
        returnstat =  self.condensed_mana.level > skill_stat.mana_to_next_level
        return returnstat
    
    def increase_skill_level(self, skill: Skill, level=1):
        for _ in range(level):
            if self.check_if_con_mana_more_than_stat(skill_stat=skill):
                self.use_condensed_mana(skill.mana_to_next_level)
                skill.total_mana_used += skill.mana_to_next_level
                self.increase_next_level_requirement(stat=skill, level=1)
                skill.level +=1
                skill.calculate_stat_multiplier()
                
        self.skills_level.calculate_level()    
        self.calculate_character_level()
    

    def increase_stat_level(self, stat=  Stat, level=1):
        for _ in range(level):
            stat : Stat
            if self.check_if_con_mana_more_than_stat(skill_stat=stat,):
                self.use_condensed_mana(stat.mana_to_next_level)
                self.increase_next_level_requirement(stat=stat, level = 1)
                stat.level += 1
        self.calculate_character_level()
    
    def decrease_stat_level(self, stat=  Stat, level=1):
        for _ in range(level):
            stat : Stat
            self.add_condensed_mana(stat.mana_to_next_level-1)
            self.decrease_next_level_requirement(stat=stat, level = 1)
            stat.level -= 1
        self.calculate_character_level()
        self.calculate_max_mana()
        self.calculate_effective_stat_level()

    def increase_next_level_requirement(self, stat: Stat | Skill, level=1):
        next_actual_level_requirement = stat.actual_mana_to_next_level * (self.mana_requirement_increaser ** level)
        stat.actual_mana_to_next_level = next_actual_level_requirement

    def decrease_next_level_requirement(self, stat: Stat | Skill, level=1):
        previous_actual_level_requirement = stat.actual_mana_to_next_level * (self.mana_requirement_increaser ** (level-1))
        stat.actual_mana_to_next_level = previous_actual_level_requirement