from windowGUI import Window
from PyQt5.QtWidgets import QApplication
import sys
import time



def main():
    App = QApplication(sys.argv)
    typ = ["T"]
    window = Window()
    window.show()
    time.sleep(1)
    for t in typ:
        window.set_letter(t)
        window.show()
        # time.sleep(2)
    window.show()
    # window.set_letter("A")
    # window.show()
    # time.sleep(2)
    # window.set_letter("T")
    # window.show()
    sys.exit(App.exec())


main()