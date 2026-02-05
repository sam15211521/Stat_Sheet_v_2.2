from math import ceil
from timeit import default_timer as timer
from colorama import Fore, Back

class ABA():
    def __init__(self):
        self._dictionary = {}
        self.first = 1
        self.stat = CCC()
    
    @property
    def dictionary(self):
        return self._dictionary
    @property
    def dictionary(self, value):
        self._dictionary



class CCC():
    def __init__(self):
        self.dictionary = {}