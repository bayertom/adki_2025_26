from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__building = QPolygonF()
        self.__ch = QPolygonF()
        self.__building_simp = QPolygonF()

        

    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x,y)
        
        #Add P to polygon
        self.__building.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Set attributes, polygon
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw building
        qp.drawPolygon(self.__building)
        
        #Set attributes, CH
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        #Draw CH
        qp.drawPolygon(self.__ch)
        
        #Set attributes, building_simp
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        #Draw building_simp
        qp.drawPolygon(self.__building_simp)
        
        #End draw
        qp.end()
        
        
    def getBuilding(self):
        #Returns 'private' building
        return self.__building
    
    
    def setSimplifiedBuilding(self, building):
        #Sets the building
        self.__building_simp = building
    
    
    def setCH(self, ch):
        #Sets the convex hull
        self.__ch = ch