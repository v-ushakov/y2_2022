import os.path, sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QListView, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSlider, QSplitter, QStyle, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore    import Qt

import biosynth


def stdIcon(id):
    return QApplication.style().standardIcon(id)

class BioWindow(QMainWindow):

    NO_FILE = 'No file selected'

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.file_loaded = False
        #-----------------------------------------------------------------------
        hspl = QSplitter()
        self.setCentralWidget(hspl)

        left = QWidget()
        left.setLayout(QVBoxLayout())
        hspl.addWidget(left)

        rght = QWidget()
        rght.setLayout(QVBoxLayout())
        hspl.addWidget(rght)
        hspl.setStretchFactor(0, 1)                     # keep the selected size
        pick = QListView()
        rght.layout().addWidget(pick)

        view = QScrollArea()
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)    # height
        view.setMinimumSize(0, 200)
        left.layout().addWidget(view)
        left.layout().addWidget(QSlider(Qt.Horizontal))
        left.layout().addWidget(QSlider(Qt.Horizontal))
        tabs = self.tabs = QTabWidget()
        left.layout().addWidget(tabs)
        btns = QWidget()
        btns.setLayout(QHBoxLayout())
        left.layout().addWidget(btns)

        #--- buttons -----------------------------------------------------------
        self.prev = QPushButton(stdIcon(QStyle.SP_ArrowBack), 'Previous')
        self.prev.clicked.connect(self.prevTab)
        btns.layout().addWidget(self.prev)

        self.next = QPushButton(stdIcon(QStyle.SP_ArrowForward), 'Next')
        self.next.clicked.connect(self.nextTab)
        btns.layout().addWidget(self.next)

        btns.layout().addWidget(QWidget())                              # filler

        butt = QPushButton(stdIcon(QStyle.SP_DialogCloseButton), 'Exit')
        butt.clicked.connect(self.close)
        btns.layout().addWidget(butt)

        #--- tabs --------------------------------------------------------------
        pane = QWidget()
        tabs.addTab(pane, 'Welcome')
        pane.setLayout(QGridLayout())
        file = self.file = QLabel(self.NO_FILE)
        file.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        pane.layout().addWidget(file, 0, 0)
        open = QPushButton(stdIcon(QStyle.SP_DialogOpenButton), 'Open File')
        open.clicked.connect(self.openFile)
        pane.layout().addWidget(open, 0, 1)
        pane.layout().addWidget(QWidget(), 1, 0, 1, 2)                  # filler
        pane.layout().setColumnStretch(0, 1)

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        tabs.addTab(QWidget(), 'Genome')
        tabs.addTab(QWidget(), 'Transcription')
        tabs.addTab(QWidget(), 'Splicing')
        tabs.addTab(QWidget(), 'Translation')
        tabs.currentChanged.connect(self.tabChanged)

        #--- dialogs -----------------------------------------------------------
        self.odlg = QFileDialog(
            caption = 'Please choose a file with DNA',
            directory = os.path.normpath(
                            os.path.join(
                                os.path.dirname(sys.argv[0]), '..', 'DNA')))
        self.odlg.setFileMode(QFileDialog.ExistingFile)

        #-----------------------------------------------------------------------
        self.resize(1000, 500)
        hspl.setSizes([700, 300])

        self.fileLoaded(False)
        self.tabChanged(0)

    def openFile(self):
        ok = self.odlg.exec()
        if ok:
            try:
                filename = self.odlg.selectedFiles()[0]
                dna = biosynth.read_dna(filename)
                # TODO: insert the data
                self.file.setText('File: ' + os.path.relpath(filename))
            except Exception as e:
                QMessageBox(QMessageBox.Warning,
                                            'Cannot read DNA', str(e)).exec()
                ok = False
                self.file.setText(self.NO_FILE)
            self.fileLoaded(ok)

    def fileLoaded(self, ok):
        self.file_loaded = ok
        for t in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(t, ok)
        self.tabChanged(self.tabs.currentIndex())

    def tabChanged(self, tab):
        self.prev.setEnabled(tab > 0)
        self.next.setEnabled(tab < 4 and self.file_loaded)

    def nextTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

    def prevTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() - 1)

    def closeEvent(self, ev):
        QApplication.exit()
