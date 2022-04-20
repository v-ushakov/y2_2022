import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QIcon, QPainter, QPen, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt, QPoint

def start():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Protein synthesis")
    window.setFixedWidth(1500)
    window.move(100, 100)
    window.setStyleSheet("background : #beb1c7;")##beb1c7#ab9bb7

    grid = QGridLayout()


    #display logo


    image = QPixmap("../videotutorial/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    #placing logo in the center:
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;"
                       "margin-bottom : 100px;")

    #button-widget:

    button = QPushButton("Start Biosynthesis")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#94ca6d';"+
                         "border-radius : 45px;"+
                         "font-size : 35px;"+
                         "color : 'white';"+
                         "padding: 25px 0;"+
                         "margin: 100px 200px;}" +
                         "*:hover{background: '#94ca6d';}"

                         )


    #grid.addWidget(logo, 0, 0)
    grid.addWidget(button, 1, 0)



window.setLayout(grid)
window.show()
sys.exit(app.exec())