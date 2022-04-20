from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer

nucleotides = { }

class Nucleotide:
    def __init__(self, c, r, g, b, points):
        self.key = c
        self.brush = QBrush(QColor(r, g, b, 100), Qt.SolidPattern)
        self.shape = QPolygon([QPoint(x, y) for (x, y) in points])
        nucleotides[c] = self

    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        painter.setBrush(self.brush)
        painter.drawText(93, 90, self.key)
        painter.drawPolygon(self.shape)

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
        self.shift = 0
        self.dna = dna


        self.timer = QTimer()
        self.timer.timeout.connect(self.shift_data)
        self.timer.start(10)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.shift, 0)
        for x in self.dna:
            painter.translate(36, 0)
            nucleotides[x].draw(painter)

    def shift_data(self):
        if self.shift > self.width():
            self.shift = 0
        else:
            self.shift += 1
        self.repaint()


if __name__ == "__main__":
    from sys import argv
    from PyQt5.QtWidgets import QApplication


    app = QApplication(argv)
    win = DNA_view("ACGTTGCA"*20)
    win.show()
    app.exec()
