
class Mastery:
    list_of_materies = {}
    def __init__(self,
                 name,
                 minimum_level = 0,
                 maximum_level = 1,
                 requires_basic = False,
                 multiplier = 1,
                 discription = ""
                 ):
        self._name = name
        self._maximum_level = maximum_level
        self._minimum_level = minimum_level
        self._requires_basic = requires_basic
        self._multiplier = multiplier
        self._discription = discription

        self.list_of_materies[self.name] = self
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def minimum_level(self):
        return self._minimum_level

    @property
    def maximum_level(self):
        return self._maximum_level
    
    @property
    def multiplier(self):
        return self._multiplier
    
    @property
    def discription(self):
        return self._discription
    
    @discription.setter
    def discription(self, string):
        self._discription = string




    def __str__(self):
        line1 = f'{self.name}'
        line2 = 'Discription:'
        line3 = self.discription
        line4 = f'\nlevel range: {self.minimum_level} - {self.maximum_level}'
        line5 = f'basicrequirement: {"Yes" if self._requires_basic else "No"}'
        line6 = f'power multiplier: {self.multiplier}'
        return '\n'.join([line1, line2, line3, line4, line5, line6])

# here are the objects of the types of mastery
basic_discription = "have a non-system amount of ability for that skill."
beginner_discription = '''
Skills boosted by mana, yet not capable of much strength.
Learn more about the skill and level it up as well.
(Cannot progress over 100 without the basics)
'''
intermediate_discription = """
You know the basics!
And you even have some ability in it!
Keep training and leveling 
to make it shine with mana
"""
expert_discription = """
You know how to use it!
You just have to master it.
strengthen its levels to unlock its power
and practice your skill to mastery
"""
master_discription = """
Remember though I have nothing left to teach you
never will you stop learning, 
growing
"""


basic = Mastery(name ="Basic",
               minimum_level= 0,
               maximum_level=100,
               requires_basic= False,
               multiplier= 1,
               discription=basic_discription
               )

beginner = Mastery(name ="Beginner",
                   minimum_level= 1,
                   maximum_level= 100,
                   requires_basic= False, 
                   multiplier= 1.5,
                   discription=beginner_discription
                   )
intermediate = Mastery(name = "Intermediate",
                   minimum_level= 1, 
                   maximum_level= 109,
                   requires_basic= True, 
                   multiplier= 2.5,
                   discription=intermediate_discription
                    )
expert = Mastery(name ="Expert",
                   minimum_level= 110,
                   maximum_level= 1000,
                   requires_basic= True,
                   multiplier= 6,
                   discription=expert_discription
                   )
master = Mastery(name = "Master",
                   minimum_level= 1001, 
                   maximum_level=10000,
                   requires_basic= True,
                   multiplier= 12,
                   discription=master_discription
                   )