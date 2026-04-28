from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms():    
    def getPolygonArea(self, pol: QPolygonF):
        #Calculate polygon area  using LH formula
        #Return sign of the area
        area = 0
        n = len(pol)

        #Process all edges
        for i in range(n):
            area += pol[i].x() * (pol[(i+1)%n].y() - pol[(i-1+n)%n].y())
        
        return area/2


    def getPointLineDistance(self, p: QPointF, p1: QPointF, p2: QPointF):
        #Distance of the point from the line
        numerator = p.x()*(p1.y()-p2.y()) + p.x1()*(p2.y()-p.y()) + p2.x()*(p.y()-p1.y())
        denominator = sqrt((p2.x()-p1.x())**2 + (p2.y()-p1.y())**2)

        d = abs(numerator/denominator)
        
        return d


    def dp(self, pol, pol_simp, h, s, e):
        #Recursive Douglas-Peucker algorithm
        if (e <= s + 1):
            return
        
        #Initialize variables
        i_max = s+1
        d_max = self.getPointLineDistance(pol[i_max], pol[s], pol[e])
        
        #Process all internal vertices
        for i in range(i_max + 1, e):
            
            #Compute distance of point from the line
            d = self.getPointLineDistance(pol[i], pol[s], pol[e])
            
            #Update maximum
            if d > d_max:
                d_max = d
                i_max = i
        
        #Furthest point outside polygon
        if d_max > h:
            
            #Process recursively the first segment
            self.dp(pol, pol_simp, h, s, i_max)
            
            #Add the furthest point
            pol_simp.append(pol[i_max])
            
            #Process recursively the second segment
            self.dp(pol, pol_simp, h, i_max, e)


    def simplifyDouglasPeucker(self, pol, h):
        #Apply Douglas Peucker algorithm
        s = 0
        e = len(pol)
        
        #Append start point
        pol_simp = [pol[s]]

        #Recursive processing
        self.dp(pol, pol_simp, h, s, e)

        #Append end point
        pol_simp.append(pol[e])
                
        return pol_simp


    def simplifyEuclideanDistance(self, pol, d_min):
        #Simplify polyline using Euclidean distance
        n = len(pol)
        pol_simp = []
        used = [True] * n
        
        #Process all points
        for i in range(0, n-2):
            #Starting point is pivot
            j = i
            while True:
                #Compute distance to the next point
                d = sqrt((pol[i].x()-pol[j+1].x())**2 + (pol[i].y()-pol[j+1].y())**2)
                
                #If smaller than tollerance, simplify
                if d < d_min:
                    used[j] = False
                    j = j+1

                #First larger distance we continue
                else:
                    break