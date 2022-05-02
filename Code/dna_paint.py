from PyQt5.QtWidgets import QWidget, QScrollArea, QMainWindow, QScrollArea, QSlider, QSplitter, \
                            QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QTransform, qGray, QCursor
from PyQt5.QtCore import Qt, QPoint, QTimer
from biosynth import reading_letters as rl
from biosynth import find_genes

import math

nucleotides = { }



class Nucleotide:
    def __init__(self, key, r, g, b, points):
        nucleotides[key] = self
        self.key = key

        self.r = r
        self.g = g
        self.b = b
        self.gray = qGray(r, g, b)

        #self.gray_color_fac = qGray(r, g, b)
        #self.gray = QColor(self.gray_color_fac, self.gray_color_fac, self.gray_color_fac, 85)
        #self.hgray = QColor(r, g, b, 50)
        #self.color = QColor(r, g, b, 100)

        self.shape = QPolygon([QPoint(int(x), int(y)) for (x, y) in points])
        self.shape.translate(-80, -60)
        trans = QTransform()
        trans = trans.rotate(180)
        self.rshape = trans.map(self.shape)
        self.shape.translate(0, 110)
        self.rshape.translate(35, 110)

    def draw(self, painter, gr, shape):
        color = QColor(((100-gr)*self.r + gr*self.gray)//100,
                       ((100-gr)*self.g + gr*self.gray)//100,
                       ((100-gr)*self.b + gr*self.gray)//100, 100)

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

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.timerShot2)

        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.timerColor)

        self.color_count = 0
        self.counter = 0
        self.counterDNA = 0
        self.stage = 1

        self.genes = find_genes(dna)


    def setCounter(self, val):
        self.counter = val
        self.repaint()


    def setCounterDNA(self, val):
        self.counterDNA = val
        self.repaint()

    def setGray(self, val):
        self.color_count = val
        self.repaint()

    def timerShot(self):
        self.setCounter(self.counter + 1)
        if self.counter >= OUT:
            self.timer.stop()
            print("timer has been stopped")
            self.color_timer.start(5)

    def timerShot2(self):
        self.setCounterDNA(self.counterDNA + 1)
        if self.counterDNA >= OUT+50:
            self.timer2.stop()
            print("timer has been stopped")
            self.counterDNA = 0


    def timerColor(self):
        self.setGray(self.color_count + 1)
        self.repaint()
        if self.color_count >= 100:
            self.color_timer.stop()
            print("color timer has been stopped")
            self.timer2.start(50)
    def paintEvent(self, ev):
        dn = {'T': 'A','C': 'G','G': 'C','A' : 'T'}
        try:
            painter = QPainter(self)
            painter.save()
            a = (ev.rect().x())//36
            b = (ev.rect().x() + ev.rect().width()+35)//36
            painter.translate(36*a, 10)

            for x in self.dna[a:b+1]:
                n = dn[x]
                painter.save()
                painter.translate(0, (self.counterDNA) * 2)
                nucleotides[x].draw(painter, self.color_count, nucleotides[x].shape)
                painter.restore()
                painter.save()
                painter.translate(0, (self.counter - OUT)*2)
                nucleotides[n].draw(painter, 0, nucleotides[n].rshape)
                painter.restore()
                painter.translate(36, 0)

            painter.restore()
            for gene in self.genes:
                painter.setPen(QPen(QColor(140, 0, 0), 5, Qt.SolidLine))
                painter.drawLine(gene[0]*36,170, (gene[0]+4)*36, 170)

                painter.setPen(QPen(QColor(140, 0, 0), 5, Qt.DotLine))
                painter.drawLine((gene[0]+4)*36, 170, (gene[1])*36, 170)

                painter.setPen(QPen(QColor(0, 140, 0), 5, Qt.SolidLine))
                painter.drawLine((gene[1])*36,170, (gene[2]+3)*36, 170)
                painter.drawLine((gene[1])*36,160, (gene[1])*36, 170)
                painter.drawLine((gene[2]+3)*36, 160, (gene[2]+3)*36, 170)


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
    dna = DNA_view(rl("dna_sequence"))#("ACGTTGCAT"*20)

    win = QScrollArea()
    win.setWidget(dna)
    win.resize(1000, 500)


    slider1 = QSlider(Qt.Horizontal)
    slider1.valueChanged.connect(dna.setCounter)
    slider1.setRange(0, 70)
    slider2 = QSlider(Qt.Horizontal)
    slider2.setRange(0, 100)
    slider2.valueChanged.connect(dna.setGray)
    slider3 = QSlider(Qt.Horizontal)
    slider3.setRange(0, 100)
    slider3.valueChanged.connect(dna.setCounterDNA)


    button1 = QPushButton("Start transcription")
    button1.setCursor(QCursor(Qt.PointingHandCursor))
    button1.setStyleSheet("*{border: 2px solid '#c9bd6b';" +
                         "border-radius : 25px;" +
                         "font-size : 25px;" +
                         "color : 'black';" +
                         "padding: 25px 0;" +
                         "margin: 5px 10px;}" +
                         "*:hover{background: '#c9bd6b';}")
    button1.clicked.connect(dna.start_trans)

    layout = QVBoxLayout()
    layout.addWidget(slider1)
    layout.addWidget(slider2)
    layout.addWidget(slider3)
    layout.addWidget(button1)

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
