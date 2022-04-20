from windowGUI import Window
from PyQt5.QtWidgets import QApplication
import sys
#from StartGUI
import time



def main():
    app = QApplication(sys.argv)

    typ = ["T", "G", "A"]
    window = Window()
    window.setStyleSheet("background : #cbd4fb;")
    window.show()
    time.sleep(1)
    for t in typ:
        window.set_letter(t)
        window.repaint()
        time.sleep(1)
    # window.set_letter("A")
    # window.show()
    # time.sleep(2)
    # window.set_letter("T")
    # window.show()
    sys.exit(app.exec())


main()