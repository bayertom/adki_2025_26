from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms():    
    def getPolygonArea(self, pol: QPolygonF):
        #Calculate polygon area  using LH formula
        #Return signed area
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

        return abs(numerator/denominator)


    def dp(self, pol, pol_simp, h, s, e):
        #Recursive Douglas-Peucker algorithm
        if (e <= s + 1):
            return
        
        #Initialize variables
        i_max = s + 1
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
        if len(pol) <=2:
            return pol
        
        #Initialize 
        s = 0
        e = len(pol) - 1 
        
        #Append start point
        pol_simp = [pol[s]]

        #Recursive processing
        self.dp(pol, pol_simp, h, s, e)

        #Append end point
        pol_simp.append(pol[e])
                
        return pol_simp


    def simplifyEuclideanDistanceV1(self, pol, d_min):
        #Simplify polyline using Euclidean distance
        #Remove points closer than d_min
        n = len(pol)
        if n <=2:
            return pol
        
        #Simplified polyline
        pol_simp = []
        
        #Flag, all points are used
        used = [True] * n
        
        #Process all points closer than d_min
        while i < n - 1:
            
            #Assign next point
            j = i + 1
            
            #Repeat until last point is found
            while j < n:
                #Compute distance to the next point
                d = sqrt((pol[i].x()- pol[j].x())**2 + (pol[i].y() - pol[j].y())**2)
                
                #If d smaller than tollerance, throw point
                if d < d_min:
                    
                    #Point will not be used
                    used[j] = False
                    
                    #Increment j
                    j = j + 1

                #First larger distance,  we continue
                else:
                    break
                
            #Update j
            i = j
            
        #Create output points
        for i in range(n):
            if used[i]:
               pol_simp.append(pol[i])
               
        return pol_simp 
    
    
    def simplifyEuclideanDistanceV2(self, pol, d_min):
        #Simplify polyline using Euclidean distance
        #Remove points closer than d_min
        #Simplified version
        n = len(pol)
        if n <= 2:
            return pol[:]
        
        #Always store the first point
        pol_simp = [pol[0]]
        
        #Store the last correct point
        last = pol[0]
        
        #Process all points
        for i in range(1, n):
            #Distance from the last point to the current point
            d = sqrt((last.x() - pol[i].x())**2 + (last.y() - pol[i].y())**2)
            
            #Point is too far, it becomes the last point
            if d >= d_min:
                #Add point to the list
                pol_simp.append(pol[i])
                
                #Update last point
                last = pol[i]
                
        #Store the last point
        if pol_simp[-1] != pol[-1]:
            pol_simp.append(pol[-1])
                
        return pol_simp