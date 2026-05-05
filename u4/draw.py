from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__polyline = []
        self.__polyline_simp = []
       
        
    def mousePressEvent(self, e):
        #Get position
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x,y)
            
        #Add point to polygon
        self.__polyline.append(p)      
      
        #Repaint screen
        self.repaint()


    def paintEvent(self, e):
        #Repaint screen
        
        #New object
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Graphic attributes, source polyline 
        qp.setPen(Qt.GlobalColor.black)
        
        #Draw source polyline
        qp.drawPolyline(self.__polyline)
        
        #Graphic attributes, simplified polyline
        qp.setPen(Qt.GlobalColor.red)
        
        #Draw simplified polyline
        qp.drawPolyline(self.__polyline_simp)
        
        #End draw
        qp.end()
        
        
    def changeStatus(self):
        #Change status: draw point / polygon
        self.__add_vertex = not(self.__add_vertex)
        
        
    def clearCanvas(self):
        #Clears the canvas
        self.__polyline.clear()
        self.__polyline_simp.clear()

        self.repaint()

    
    def getPolyline(self):
        #Get polyline
        return self.__polyline
    

    def setPolylineSimp(self, polyline_simp):
        #Set polyline
        self.__polyline_simp = polyline_simp
    
