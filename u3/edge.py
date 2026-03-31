from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Edge():
    def __init__(self, start, end):
        self.__start = start
        self.__end = end
    
    def getStart(self):
        return self.__start
    
    def getEnd(self):
        return self.__end
    
    def switchOrientation(self):
        self.__start, self.__end = self.__end, self.__start