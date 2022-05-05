from PyQt5.QtWidgets import QApplication, QHBoxLayout, QListView, QMainWindow, QPushButton, QSlider, QSplitter, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore    import Qt


class BioWindow(QMainWindow):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        hspl = QSplitter()
        self.setCentralWidget(hspl)

        left = QWidget()
        left.setLayout(QVBoxLayout())
        hspl.addWidget(left)

        self.genes_list = QListView()
        hspl.addWidget(self.genes_list)

        left.layout().addWidget(QListView())
        left.layout().addWidget(QSlider(Qt.Horizontal))
        left.layout().addWidget(QSlider(Qt.Horizontal))
        tabs = QTabWidget()
        left.layout().addWidget(tabs)
        btns = QWidget()
        btns.setLayout(QHBoxLayout())
        left.layout().addWidget(btns)

        btns.layout().addWidget(QPushButton('< Previous'))
        btns.layout().addWidget(QPushButton('Next >'))
        btns.layout().addWidget(QWidget())                             # spacer
        btns.layout().addWidget(QPushButton('Exit'))

        tabs.addTab(QWidget(), 'Genome')
        tabs.addTab(QWidget(), 'Transcription')
        tabs.addTab(QWidget(), 'Splicing')
        tabs.addTab(QWidget(), 'Translation')

        self.resize(1000, 500)
        hspl.setSizes([700, 300])


    def closeEvent(self, ev):
        QApplication.exit()
