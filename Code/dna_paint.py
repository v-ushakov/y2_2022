from PyQt5.QtWidgets import QWidget, QScrollArea, QMainWindow, QScrollArea, QSlider, QSplitter, \
                            QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QTransform, qGray, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer


import math

nucleotides = { }



class Nucleotide:
    def __init__(self, c, r, g, b, points):
        nucleotides[c] = self
        self.key = c
        self.gray_color_fac = qGray(r, g, b)
        self.gray = QColor(self.gray_color_fac, self.gray_color_fac, self.gray_color_fac, 85)
        self.hgray = QColor(r, g, b, 50)
        self.color = QColor(r, g, b, 100)
        self.shape = QPolygon([QPoint(x, y) for (x, y) in points])
        self.shape.translate(-80, -60)
        trans = QTransform()
        trans = trans.rotate(180)
        self.rshape = trans.map(self.shape)
        self.shape.translate(0, 110)
        self.rshape.translate(35, 110)


    def get_gray_color_fac(self):
        return self.gray_color_fac

    def change_color(self,a, b, c):
        self.color = QColor(a, b, c, 100)







    def draw(self, painter, gr, shape, c):
        if c == 0:
            color = self.color
        elif c == 1:
            color = self.color.lighter(150)
        elif c == 2:
            color = self.color.lighter(170)
        elif c == 3:
            color = self.color.lighter(180)
        else:
            color = self.gray


        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        painter.drawPolygon(shape)
        if shape == self.shape:
            painter.drawText(shape.boundingRect().center() + QPoint(-3, 10), self.key)
        elif shape == self.rshape:
            key = 'U' if self.key == 'T' else self.key
            painter.drawText(shape.boundingRect().center() + QPoint(-3, -2), key)
        # if shape == self.shape:
        #     painter.drawText(13, 185, self.key)
        # elif shape == self.rshape:
        #     x = self.rshape
        #     y = 100
        #     painter.drawText(x, y, self.key)


Nucleotide('A', 100,   0, 0, [(80, 60), (80, 100), (115, 100), (115, 60),
                              (97.5, 45), (80, 60)])
Nucleotide('T', 0,   100, 0, [(80, 60), (80, 100), (115, 100), (115, 60),
                              (97.5, 75), (80, 60)])
Nucleotide('G', 200, 200, 0, [(80, 60), (80, 100), (115, 100), (115, 60),
                              (110, 68), (103, 72), (97.5, 73), (99.5, 73),
                              (95.5, 73), (97.5, 73), (92, 72), (85, 68),
                              (80, 60)])
Nucleotide('C', 200,   0, 0, [(80, 60), (80, 100), (115, 100), (115, 60),
                              (110, 52), (103, 48), (97.5, 47), (99.5, 47),
                              (95.5, 47), (97.5, 47), (92, 48), (85, 52),
                              (80, 60)])

OUT = 70

class DNA_view(QWidget):

    def __init__(self, dna):
        super().__init__()
        #self.setStyleSheet("background : #cbd4fb;")
        self.dna = dna
        self.resize(36*len(self.dna), 300)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerShot)

        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.timerColor)

        self.color_count = 0
        self.counter = 0
        self.stage = 1

    def timerShot(self):
        self.counter += 1
        self.repaint()
        if self.counter == OUT:
            self.timer.stop()
            print("timer has been stopped")
            self.color_timer.start(50)

    def timerColor(self):
        self.color_count += 1
        self.repaint()
        if self.color_count == 4:
            self.color_timer.stop()
            print("color timer has been stopped")
            self.stage = 2
            self.counter = 0
            #self.timer.start(50)









    def paintEvent(self, ev):
        dn = {'T': 'A','C': 'G','G': 'C','A' : 'T'}
        try:
            painter = QPainter(self)
            a = (ev.rect().x())//36

            b = (ev.rect().x() + ev.rect().width()+35)//36
            painter.translate(36*a, 10)

            for x in self.dna[a:b+1]:
                n = dn[x]
                gr = self.color_count
                nucleotides[x].draw(painter, 0, nucleotides[x].shape, gr)
                painter.save()

                painter.translate(0, (self.counter - OUT)*2)
                nucleotides[n].draw(painter, 0 , nucleotides[n].rshape, 0)

                painter.restore()
                painter.translate(36, 0)


        except Exception as e:
            print(e)

    def start_trans(self):
        self.counter = 0
        self.color_count = 0
        self.timer.start(50)

    def keyReleaseEvent(self, ev):
        print(ev.key())
        if ev.key() == 32:
            self.start_trans()
        elif ev.key() == 67:
            self.color_count = 0
            self.color_timer.start(50)











if __name__ == "__main__":
    from sys import argv
    from PyQt5.QtWidgets import QApplication


    app = QApplication(argv)
    dna = DNA_view("ACGTTGCAT"*20)

    win = QScrollArea()
    win.setWidget(dna)
    win.resize(1000, 500)


    slider1 = QSlider(Qt.Horizontal)
    #slider2 = QSlider(Qt.Horizontal)
    button1 = QPushButton("Start transcription")
    button1.setCursor(QCursor(Qt.PointingHandCursor))
    button1.setStyleSheet("*{border: 2px solid '#c9bd6b';" +
                         "border-radius : 25px;" +
                         "font-size : 25px;" +
                         "color : 'black';" +
                         "padding: 25px 0;" +
                         "margin: 50px 100px;}" +
                         "*:hover{background: '#c9bd6b';}")
    button1.clicked.connect(dna.start_trans)
    #self.color_timer.timeout.connect(self.timerColor)

    layout = QVBoxLayout()
    layout.addWidget(slider1)
    layout.addWidget(button1)
    #layout.addWidget(slider2)

    panel = QWidget()
    panel.setLayout(layout)
    #---------------------------------------------------------------------------

    spl = QSplitter(Qt.Vertical)
    spl.addWidget(win)
    spl.addWidget(panel)

    wid = QMainWindow()
    wid.setCentralWidget(spl)
    wid.resize(1000, 500)
    wid.show()

    win.show()
    dna.setFocus()
    app.exec()
