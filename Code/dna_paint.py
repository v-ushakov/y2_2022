from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QTransform
from PyQt5.QtCore import Qt, QPoint
import math

nucleotides = { }



class Nucleotide:
    def __init__(self, c, r, g, b, points):
        nucleotides[c] = self
        self.key = c
        self.color = QColor(r, g, b, 50)
        self.shape = QPolygon([QPoint(x, y) for (x, y) in points])
        self.shape.translate(-80, -60)
        trans = QTransform()
        trans = trans.rotate(180)
        self.rshape = trans.map(self.shape)
        self.shape.translate(0, 110)
        self.rshape.translate(35, 110)





    def draw(self, painter, gr, shape):
        color = self.color
        #if gr != 0 :
        #color.setHSV(a = 50)
        #
        # else:
        #     color = self.color


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

class DNA_view(QWidget):

    def __init__(self, dna):
        super().__init__()
        #self.setStyleSheet("background : #cbd4fb;")
        self.dna = dna
        self.resize(36*len(self.dna), 300)

    def paintEvent(self, ev):
        dn = {'T': 'A','C': 'G','G': 'C','A' : 'T'}
        try:
            painter = QPainter(self)
            a = (ev.rect().x())//36

            b = (ev.rect().x() + ev.rect().width()+35)//36
            painter.translate(36*a, 10)

            painter.save()
            for x in self.dna[a:b+1]:
                n = dn[x]
                nucleotides[x].draw(painter, 0, nucleotides[x].shape)
                nucleotides[n].draw(painter, 0 , nucleotides[n].rshape)
                painter.translate(36, 0)
            painter.restore()
            for x in self.dna[a:b+1]:
                painter.translate(36, 0)
            print(ev.rect())
            print(ev.rect().x())
            print(ev.rect().width())
            #print(1622//36)
        except Exception as e:
            print(e)

    def keyReleaseEvent(self, ev):
        print(ev.key())


if __name__ == "__main__":
    from sys import argv
    from PyQt5.QtWidgets import QApplication


    app = QApplication(argv)
    dna = DNA_view("ACGTTGCAT"*20)

    win = QScrollArea()
    win.setWidget(dna)
    win.resize(1000, 500)

    win.show()
    dna.setFocus()
    app.exec()
