from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points = []
        self.__DT = []
        
        '''
        self.__points.append(QPoint3DF(0,0,0))
        self.__points.append(QPoint3DF(100,0,0))
        self.__points.append(QPoint3DF(0,100,0))
        self.__points.append(QPoint3DF(100,100,0))
        self.__points.append(QPoint3DF(50,50,0))
        '''
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPoint3DF(x, y, 0)
        
        #Add P to polygon
        self.__points.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        pen = QPen()

        #Set attributes, lines
        pen.setColor(Qt.GlobalColor.green)
        qp.setPen(pen)

        #Draw lines
        for e in self.__DT:
            qp.drawLine(e.getStart(), e.getEnd())
        
        #Set attributes, points
        pen.setColor(Qt.GlobalColor.black)
        pen.setWidth(10)
        qp.setPen(pen)
        
        #Draw points
        qp.drawPoints(self.__points)
        
        #End draw
        qp.end()
        

    def setDT(self, DT):
        self.__DT = DT
        
    
    def getPoints(self):
        return self.__points