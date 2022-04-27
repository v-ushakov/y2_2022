import sys
import math
import time
from PyQt5.QtWidgets import QScrollArea, QHBoxLayout,  QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QGraphicsScene,  QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QIcon, QPainter, QPen, QBrush, QPolygon, QColor, QTransform
from PyQt5.QtCore import Qt, QPoint

class Window(QMainWindow):
    def __init__(self):
        super(). __init__()
        self.c = "C"
        self.scene = QGraphicsScene()
        #self.setCentralWidget(QWidget())
        #self.horizontal = QHBoxLayout()  # Horizontal main layout
       # self.centralWidget().setLayout(self.horizontal)
        self.scene.setSceneRect(300,200,1500,500)

        self.setGeometry(300,200,1500,500)


    def set_letter(self, co):
        if isinstance(co,str):
            self.c = co



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        if self.c == "A":
            painter.setBrush(QBrush(QColor(100, 0, 0, 100), Qt.SolidPattern))
        if self.c == "T":
            painter.setBrush(QBrush(QColor(0, 100, 0, 100), Qt.SolidPattern))
        if self.c == "G":
            painter.setBrush(QBrush(QColor(200, 200, 0, 100), Qt.SolidPattern))
        if self.c == "C":
            painter.setBrush(QBrush(QColor(200, 0, 0, 100), Qt.SolidPattern))



        #[[2.2, 4.2], [7.2, -25.1], [9.26, -2.456]]
        pointsA = QPolygon([

            QPoint(80, 60),
            QPoint(80, 100),
            QPoint(115, 100),
            QPoint(115, 60),
            QPoint(97.5, 45),
            QPoint(80, 60)
        ])

        pointsT = QPolygon([

            QPoint(80, 60),
            QPoint(80, 100),
            QPoint(115, 100),
            QPoint(115, 60),
            QPoint(97.5, 75),
            QPoint(80, 60)
        ])

        pointsG = QPolygon([

            QPoint(80, 60),
            QPoint(80, 100),
            QPoint(115, 100),
            QPoint(115, 60),
            QPoint(110, 68),
            QPoint(103, 72),
            QPoint(97.5, 73),
            QPoint(99.5, 73),
            QPoint(95.5, 73),
            QPoint(97.5, 73),
            QPoint(92, 72),
            QPoint(85, 68),
            QPoint(80, 60)
        ])
        pointsC = QPolygon([

            QPoint(80, 60),
            QPoint(80, 100),
            QPoint(115, 100),
            QPoint(115, 60),
            QPoint(110, 52),#8
            QPoint(103, 48),#4
            QPoint(97.5, 47),#1
            QPoint(99.5, 47),
            QPoint(95.5, 47),
            QPoint(97.5, 47),
            QPoint(92, 48),#1
            QPoint(85, 52),#4
            QPoint(80, 60)#8
        ])
        #p = scene.addPolygon(pointsG)

        #transform = QtGui.QTransform()
        #transform.translate(20, 100)
        #transform.rotate(-90)

        #p.setTransform(transform)

        if self.c == "T":
            painter.drawText(93, 90, "T")
            painter.drawPolygon(pointsT)

        if self.c == "A":
            painter.drawText(93, 90, "A")
            painter.drawPolygon(pointsA)

        if self.c == "C":
            painter.drawText(93, 90, "C")
            painter.drawPolygon(pointsC)

        if self.c == "G":
            painter.drawText(93, 90, "G")
            painter.drawPolygon(pointsG)


# look for animation in pyQt







