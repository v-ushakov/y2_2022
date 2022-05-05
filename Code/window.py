from PyQt5.QtWidgets import QApplication, QHBoxLayout, QListView, QMainWindow, QPushButton, QScrollArea, QSizePolicy, QSlider, QSplitter, QStyle, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore    import Qt

def stdIcon(id):
    return QApplication.style().standardIcon(id)

class BioWindow(QMainWindow):

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
        hspl.setStretchFactor(0, 1)                         # stick to the right

        self.genes_list = QListView()
        rght.layout().addWidget(self.genes_list)

        view = QScrollArea()
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)    # height
        view.setMinimumSize(0, 200)
        left.layout().addWidget(view)
        left.layout().addWidget(QSlider(Qt.Horizontal))
        left.layout().addWidget(QSlider(Qt.Horizontal))
        self.tabs = QTabWidget()
        left.layout().addWidget(self.tabs)
        btns = QWidget()
        btns.setLayout(QHBoxLayout())
        left.layout().addWidget(btns)

        #-----------------------------------------------------------------------
        self.btn_prev = QPushButton(stdIcon(QStyle.SP_ArrowBack), 'Previous')
        self.btn_prev.clicked.connect(self.prevTab)
        btns.layout().addWidget(self.btn_prev)

        self.btn_next = QPushButton(stdIcon(QStyle.SP_ArrowForward), 'Next')
        self.btn_next.clicked.connect(self.nextTab)
        btns.layout().addWidget(self.btn_next)

        btns.layout().addWidget(QWidget())                             # spacer

        butt = QPushButton(stdIcon(QStyle.SP_DialogCloseButton), 'Exit');
        butt.clicked.connect(self.test)
        btns.layout().addWidget(butt)
        #-----------------------------------------------------------------------

        self.tabs.addTab(QWidget(), 'Welcome')
        self.tabs.addTab(QWidget(), 'Genome')
        self.tabs.addTab(QWidget(), 'Transcription')
        self.tabs.addTab(QWidget(), 'Splicing')
        self.tabs.addTab(QWidget(), 'Translation')
        self.tabs.currentChanged.connect(self.tabChanged)

        self.resize(1000, 500)
        hspl.setSizes([700, 300])

        self.fileLoaded(False)
        self.tabChanged(0)

    def tabChanged(self, tab):
        self.btn_prev.setEnabled(tab > 0)
        self.btn_next.setEnabled(tab < 4 and self.file_loaded)

    def fileLoaded(self, ok):
        self.file_loaded = ok
        for t in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(t, ok)
        self.tabChanged(self.tabs.currentIndex())

    def nextTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)

    def prevTab(self):
        self.tabs.setCurrentIndex(self.tabs.currentIndex() - 1)

    def closeEvent(self, ev):
        QApplication.exit()

    #---------------------------------------------------------------------------
    def test(self):
        self.fileLoaded(not self.file_loaded)
