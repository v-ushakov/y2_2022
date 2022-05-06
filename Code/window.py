import os.path, sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QListWidget, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSlider, QSplitter, QStyle, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore    import Qt

import biosynth
from dna_paint       import DNAView


def stdIcon(id):
    return QApplication.style().standardIcon(id)


def interpolate(value, target, source = (0, 100)):
    tmin, tmax = target
    smin, smax = source
    value = min(max(smax, smin), max(min(smax, smin), value))
    return int(tmin + (value-smin)*(tmax-tmin)/(smax-smin))


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
        pick = self.pick = QListWidget()
        pick.currentRowChanged.connect(self.selectGene)
        rght.layout().addWidget(pick)

        dnav = self.dnav = DNAView()
        view = self.view = QScrollArea()
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setWidget(dnav)
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)    # height
        view.setMinimumSize(0, 300)
        view.resizeEvent = dnav.onViewResize
        left.layout().addWidget(view)
        play = self.play = QSlider(Qt.Horizontal)
        play.valueChanged.connect(self.playStep)
        left.layout().addWidget(play)
        tabs = self.tabs = QTabWidget()
        left.layout().addWidget(tabs)
        self.dbg1 = QSlider(Qt.Horizontal)
        left.layout().addWidget(self.dbg1)
        self.dbg2 = QSlider(Qt.Horizontal)
        left.layout().addWidget(self.dbg2)
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
        tabs.addTab(pane, 'Genome')
        pane.setLayout(QGridLayout())
        file = self.file = QLabel(self.NO_FILE)
        file.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        pane.layout().addWidget(file, 0, 0)
        open = QPushButton(stdIcon(QStyle.SP_DialogOpenButton), 'Open File')
        open.clicked.connect(self.openFileDialog)
        pane.layout().addWidget(open, 0, 1)
        pane.layout().addWidget(QWidget(), 1, 0, 1, 2)                  # filler
        pane.layout().setColumnStretch(0, 1)

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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

    def playStep(self, value):
        tab = self.tabs.currentIndex()
        if tab == 0:
            self.dnav.setShiftTop(   interpolate(value, (0, 140)))
            self.dnav.setShiftBottom(interpolate(value, (0,  50)))

    def openFileDialog(self):
        if self.odlg.exec():
            self.openFile(self.odlg.selectedFiles()[0])

    def openFile(self, filename):
        try:
            self.dnav.setDNA(biosynth.read_dna(filename))
            self.pick.clear()
            for g in self.dnav.genes:
                self.pick.addItem(g[4])
            self.file.setText('File: ' + os.path.relpath(filename))
            self.fileLoaded(True)
            return True
        except Exception as e:
            QMessageBox(QMessageBox.Warning,
                                        'Cannot read DNA', str(e)).exec()
            self.dnav.setDNA('')
            self.pick.clear()
            self.file.setText(self.NO_FILE)
            self.fileLoaded(False)
            return False

    def fileLoaded(self, ok):
        self.file_loaded = ok
        for t in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(t, ok)
        self.tabChanged(self.tabs.currentIndex())

    def tabChanged(self, tab):
        self.prev.setEnabled(tab > 0)
        self.next.setEnabled(tab < 4 and self.file_loaded)
        if tab == 0 and self.file_loaded:
            self.dnav.setMode(self.dnav.M_WHOLE if self.dnav.DNA()
                                                        else self.dnav.M_SPLASH)
            self.dbg1.valueChanged.connect(self.dnav.setShiftTop)
            self.dbg1.setRange(0, 140)
            self.dbg2.valueChanged.connect(self.dnav.setShiftBottom)
            self.dbg2.setRange(0, 200)

            self.play.setRange(0, 100)
            self.play.setEnabled(True)
        else:
            self.play.setRange(0, 0)
            self.play.setEnabled(False)
            try:
                self.dbg1.valueChanged.disconnect()
                self.dbg2.valueChanged.disconnect()
            except TypeError:
                pass

        if tab == 1:
            self.dnav.setMode(self.dnav.M_ZOOM)
        elif tab == 2:
            pass
        elif tab == 3:
            pass

    def nextTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

    def prevTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() - 1)

    def selectGene(self, index):
        self.dnav.selectGene(index)
        x = self.dnav.geneStartX()
        if x is not None:
            self.view.ensureVisible(x, 0)

    def closeEvent(self, ev):
        QApplication.exit()
