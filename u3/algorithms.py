from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from qpoint3df import *
import sys
from edge import *

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
            return 0
        
        #On the line
        return -1
    
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        #Correct interval
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        
        return acos(arg)
    
    
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

            dist = sqrt(dx**2 + dy**2)

            #Actualize minimum
            if dist < min_distance:
                min_distance = dist
                p_nearest = point
        
        return p_nearest
    
    
    def findDelaunayPoint(self, p1, p2, points):
        #Find Delaunay point for a given edge
        max_omega = 0
        p_dt = None

        #For all points calculate the angle
        for p in points:

            #Point p different from p1, p2
            if p == p1 or p == p2:
                continue

            #Point p in the right half plane
            if self.analyzePointAndLinePosition(p, p1, p2) == 0:
                continue
            
            #Compute angle in triangle
            omega = self.get2VectorsAngle(p, p1, p, p2)
            
            #Update maximum
            if omega > max_omega:
                max_omega = omega
                p_dt = p
        
        return p_dt
    
            
    def createDT(self, points):
        #Create Delaunay triangulation
        DT = []
        AEL = []

        #Find pivot
        q = min(points, key=lambda k: k.x())

        #Find nearest point to pivot
        q_n = self.findNearestPoint(points, q)

        #Create initial edges
        e = Edge(q, q_n)
        e_s = e.switchOrientation()

        #Add them to AEL
        AEL.append(e)
        AEL.append(e_s)
        
        #Repaet until AEl is empty
        while AEL:
            
            #Take first edge
            e1 = AEL.pop()
            e1_s = e1.switchOrientation()
            
            #Find Delaunay point
            p_dt = self.findDelaunayPoint(e1_s.getStart(), e1_s.getEnd(), points)
            
            #We did not find any suitable point
            if not p_dt:
                continue

            #Create new edges
            e2 = Edge(e1_s.getEnd(), p_dt)
            e3 = Edge(p_dt, e1_s.getStart())
            
            #Add edgest to DT
            DT.append(e1_s)
            DT.append(e2)
            DT.append(e3)
            
            #Update AEL
            self.updateAEL(e2, AEL)
            self.updateAEL(e3, AEL)

        return DT
    
    
    def updateAEL(self, e, AEL):
        #Update AEL
        
        #Switch orientation
        e_s = e.switchOrientation()
        
        #Edge e_s in AEL
        if e_s in AEL:
            AEL.remove(e_s)
            
        #Edge e_s in not in AEL    
        else:
            AEL.append(e)
            