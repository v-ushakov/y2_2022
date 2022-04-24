from dna_paint import *

class View(QWidget):

    def __init__(self):
        super().__init__()

    def paintEvent(self, ev):
        painter = QPainter(self)
        dx = self.size().width()/2
        dy = self.size().height()/2
        painter.translate(dx, dy)
        painter.drawLine(-dx, 0, dx, 0)
        painter.drawLine(0, -dy, 0, dy)
        try:
            nucleotides['A'].draw(painter, 0, nucleotides['A'].shape)
        except Exception as e:
            print(e)


def main():
    from sys import argv
    from PyQt5.QtWidgets import QApplication


    app = QApplication(argv)
    dna = View()

    dna.show()
    app.exec()

main()