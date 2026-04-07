from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from qpoint3df import *
import sys

class Algorithms:
    
    def __init__(self):
        pass
    
    def analyzePointAndLinePosition(self, q, a, b):
        #Analyze point and line position (half plane test)
        tolerance = sys.float_info.epsilon * 10
         
        #Components of the vector
        ux = b.x() - a.x()
        uy = b.y() - a.y()
        vx = q.x() - a.x()
        vy = q.y() - a.y()
        
        #Cross product
        cross = ux * vy - uy * vx

        #Left halfplane
        if cross > tolerance:  
            return  1
        
        #Right halfplane
        if cross < -tolerance: 
            return -1 
        
        #On the line
        return 0
    
    
    def findNearestPoint(self, points, p):
        #Find point neares to P
        p_nearest = None
        min_distance = inf

        for point in points:
            #Skip if the same 
            if p == point:
                continue

            #Compute distance
            dx = point.x() - p.x()
            dy = point.y() - p.y()
            dz = point.z() - p.z()

            dist = sqrt(dx**2 + dy**2 + dz**2)

            #Actualize minimum
            if dist < min_distance:
                min_distance = dist
                p_nearest = point
        
        return p_nearest