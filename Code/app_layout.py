#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QScrollArea, QSlider, QSplitter, \
                            QVBoxLayout, QWidget
from PyQt5.QtCore    import Qt

class DNAMainWindow(QMainWindow):
    pass

if __name__ == "__main__":
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication

    app = QApplication(argv)

    dna = QWidget()
    dna.resize(3000, 200)

    scr = QScrollArea()
    scr.setWidget(dna)

    #---------------------------------------------------------------------------
    slider1 = QSlider(Qt.Horizontal)
    slider2 = QSlider(Qt.Horizontal)

    layout = QVBoxLayout()
    layout.addWidget(slider1)
    layout.addWidget(slider2)

    panel = QWidget()
    panel.setLayout(layout)
    #---------------------------------------------------------------------------

    spl = QSplitter(Qt.Vertical)
    spl.addWidget(scr)
    spl.addWidget(panel)

    win = DNAMainWindow()
    win.setCentralWidget(spl)
    win.show()

    app.exec()
