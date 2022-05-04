from PyQt5.QtWidgets import QApplication, QWidget


class BioWindow(QWidget):

    def closeEvent(self, ev):
        QApplication.exit()
