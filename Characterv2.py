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
        
        