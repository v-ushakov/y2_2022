from PyQt5.QtWidgets import QWidget, QScrollArea, QMainWindow, QScrollArea, QSlider, QSplitter, \
                            QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QTransform, qGray, QCursor
from PyQt5.QtCore import Qt, QPoint
from statistics import mean
from biosynth import read_dna as rl
from biosynth import find_genes, proteins

import math
from amino import aminos, Yellow, Pink, Green, Blue
nucleotides = { }

class Nucleotide:
    def __init__(self, key, r, g, b, points):
        nucleotides[key] = self
        self.key = key

        self.r = r
        self.g = g
        self.b = b
        self.gray = qGray(r, g, b)

        self.shape = QPolygon([QPoint(int(x), int(y)) for (x, y) in points])
        self.shape.translate(-80, -60)
        trans = QTransform()
        trans = trans.rotate(180)
        self.rshape = trans.map(self.shape)
        self.shape.translate(0, 110)
        self.rshape.translate(35, 110)

    def draw(self, painter, gray, upper, shift = 0, rna = None):

        if rna is None: rna = upper
        key = 'U' if rna and self.key == 'T' else self.key

        color = QColor(((100-gray)*self.r + gray*self.gray)//100,
                       ((100-gray)*self.g + gray*self.gray)//100,
                       ((100-gray)*self.b + gray*self.gray)//100, 100)
        if upper: shift = -shift
        painter.save()
        painter.translate(0, shift)
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        if upper:
            painter.drawPolygon(self.rshape)
            painter.drawText(self.rshape.boundingRect().center() + QPoint(-3, -2), key)
        else:
            painter.drawPolygon(self.shape)
            painter.drawText(self.shape.boundingRect().center() + QPoint(-3, 10), key)
        painter.restore()

    def pair(self):
        dn = {'T': 'A', 'C': 'G', 'G': 'C', 'A': 'T'}
        return nucleotides[dn[self.key]]


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

def interpolate(value, target, source = (0, 1000)):
    tmin, tmax = target
    smin, smax = source
    value = min(max(smax, smin), max(min(smax, smin), value))
    return int(tmin + (value-smin)*(tmax-tmin)/(smax-smin))


class DNAView(QWidget):

    M_SPLASH    = 0
    M_WHOLE     = 1 # the whole genome is shown
    M_ZOOM      = 2 # zooming to a particular gene
    M_INTRONS   = 3 # highlighting introns
    M_SPLICE    = 4 # squashing introns
    M_PROTEIN   = 5 # translation and protein synthesis

    def __init__(self):
        super().__init__()
        self.mode = self.M_SPLASH
        self.setDNA('')

        self.zoom = 0                       # M_ZOOM: zooming to self.gene

        self.shift_bottom = 0
        self.shift_top = 0
        self.gray = 0
        #-----------------------------------------------------------------------
        self.stage = 1
        self.prot_counter = 0

    def DNA(self):
        return self.dna


    def setDNA(self, dna):
        self.dna = dna
        self.genes = find_genes(dna)
        self.gene = None
        self.fitGenome()
        self.repaint()

    def selectGene(self, index):
        self.gene = self.genes[index] if index >= 0 else None
        self.fitGenome()
        self.repaint()

    #---------------------------------------------------------------------------
    def numAmins(self):
        return len(self.gene[4])//3 if self.gene else 0

    def geneStartX(self):
        if self.mode != self.M_WHOLE or not self.gene:
            return None
        return 36*self.gene[1]

    #---------------------------------------------------------------------------
    def setShiftTop(self, val):
        self.shift_top = val
        self.repaint()

    def setShiftBottom(self, val):
        self.shift_bottom = val
        self.repaint()

    def setGray(self, val):
        self.gray = val
        self.repaint()




    #---------------------------------------------------------------------------
    def onViewResize(self, ev):
        self.fitGenome()

    def fitGenome(self):
        if self.mode == self.M_SPLASH:
            width = self.parent().contentsRect().width() if self.parent() else 0
        elif self.mode == self.M_WHOLE:
            width = 36*len(self.dna)
        elif self.mode == self.M_ZOOM:
            _, start, end, *_ = self.gene
            width = interpolate(self.zoom, (36*len(self.dna), 36*(end - start)))
        elif self.mode == self.M_INTRONS:
            _, start, end, *_ = self.gene
            width = 36*(end - start)
        elif self.mode == self.M_SPLICE:
            _, start, end, introns, *_ = self.gene
            inlen = introns[-1][2] if introns else 0
            width = interpolate(self.zoom, (36*(end-start), 36*(end-start-inlen)))
        elif self.mode == self.M_PROTEIN:
            _, _, _, _, genome = self.gene
            width = 36*len(genome)
        else:
            width = 0
        self.resize(width, 300)
        self.move(max(0, (self.parent().contentsRect().width() - width)//2)
                                                    if self.parent() else 0, 0)

    def setMode(self, mode):
        self.mode = mode
        self.fitGenome()
        self.repaint()

    def setZoom(self, zoom):
        self.zoom = zoom
        self.fitGenome()
        self.repaint()

    def setProt(self, num):
        self.prot_counter = num
        self.repaint()


    #---------------------------------------------------------------------------
    # Mode      Comment             Animations
    # --------------------------------------------------------------------------
    # M_WHOLE   whole genome        (a) top 5'->3' strand float
    #                               (b) fading non-coding segments
    #                               (c) gene selection?
    # M_ZOOM    zooming to a gene   ???
    #
    # M_INTRONS highlight introns   (a) graying introns
    #                               (b) dropping introns
    # M_SPLICE  squash introns      (a) squashing introns
    #
    # M_PROTEIN translate protein   ???
    # --------------------------------------------------------------------------

    def underlineGene(self, painter, gene, shift, opaq = 255):

        tata, tac, stop, *_ = gene

        painter.save()
        painter.translate(0, 10 + shift)

        painter.setPen(QPen(QColor(140, 0, 0, opaq), 5, Qt.SolidLine))
        painter.drawLine(36*tata, 170, 36*(tata + 4), 170)

        painter.setPen(QPen(QColor(140, 0, 0, opaq), 5, Qt.DotLine))
        painter.drawLine(36*(tata + 4), 170, 36*tac, 170)

        painter.setPen(QPen(QColor(0, 140, 0, opaq), 5, Qt.SolidLine))
        painter.drawLine(36*tac,  170, 36*stop, 170)
        painter.drawLine(36*tac,  160, 36*tac,  170)
        painter.drawLine(36*stop, 160, 36*stop, 170)
        painter.restore()


    def paintWholeGenome(self, ev, painter):

        leftmost  = (ev.rect().x())//36
        rightmost = (ev.rect().x() + ev.rect().width()+35)//36

        # paint nucleotides
        painter.save()
        painter.translate(36*leftmost, 10)
        for pos in range(leftmost, rightmost):
            x = nucleotides[self.dna[pos]]
            x       .draw(painter, 100, True,  self.shift_top, False)
            x.pair().draw(painter,   0, False, self.shift_bottom)
            painter.translate(36, 0)
        painter.restore()

        # underline genes
        for gene in self.genes:
            self.underlineGene(painter, gene, self.shift_bottom, 255)


    def paintZoom(self, ev, painter):

        _, start, end, *_ = self.gene
        hidden = interpolate(self.zoom, (0, 36*start))
        fly_up = interpolate(self.zoom, (0, 140), (  0,  300))
        fly_dn = interpolate(self.zoom, (140, 0), (400,  700))
        fade__ = interpolate(self.zoom, (255, 0), (  0,  400))
        gray   = interpolate(self.zoom, (0, 100), (  0,  500))
        drop   = interpolate(self.zoom, (0, 200), (700, 1000))

        leftmost  = (hidden + ev.rect().x())//36
        rightmost = (hidden + ev.rect().x() + ev.rect().width() + 35)//36

        painter.save()
        painter.translate(36*leftmost - hidden, 10)
        for pos in range(leftmost, rightmost):
            grayness = gray if pos < start or pos >= end else 0

            x = nucleotides[self.dna[pos]]
            x       .draw(painter,      100, True,  fly_up, False)
            x       .draw(painter, grayness, True,  fly_dn, True)
            x.pair().draw(painter, grayness, False, drop)
            painter.translate(36, 0)
        painter.restore()

        # underline genes
        for gene in self.genes:
            self.underlineGene(painter, gene, drop, fade__)

    def paintIntrons(self, ev, painter):

        _, start, _, introns, _ = self.gene

        leftmost  = start + (ev.rect().x())//36
        rightmost = start + (ev.rect().x() + ev.rect().width() + 35)//36

        i = 0
        while i < len(introns) and leftmost >= introns[i][1]: i += 1            # TODO: binary search?

        painter.translate(36*(leftmost - start), 10)
        for pos in range(leftmost, rightmost):
            grayness = 0
            shift = 0
            if i < len(introns):
                s, e, _ = introns[i]
                if pos >= s and pos < e:
                    grayness = interpolate(self.zoom, (0,  100), (  0,  300))
                    shift    = interpolate(self.zoom, (0, -250), (700, 1000))
                elif pos >= e:
                    i += 1

            nucleotides[self.dna[pos]].draw(painter, grayness, True, shift)
            painter.translate(36, 0)


    def paintSplice(self, ev, painter):

        _, start, end, introns, *_ = self.gene

        pos = start
        delta = 0
        i = 0
        while i < len(introns):                                                 # TODO: binary search?
            _, e, total = introns[i]
            lastx = interpolate(self.zoom, (36*(e-start-total), 36*(e-start)))
            # 36*(e - start) - round(36*total*(100 - self.zoom)/100.0)
            if lastx > ev.rect().x():
                break
            pos = e
            delta = lastx
            i += 1

        rect_l = ev.rect().x()                     - delta
        rect_r = ev.rect().x() + ev.rect().width() - delta
        painter.translate(delta, 10)

        # TODO: skip more
        while i < len(introns):
            s, e, _ = introns[i]
            while pos < s:
                if rect_r <= 0:
                    return
                nucleotides[self.dna[pos]].draw(painter, 0, True)
                painter.translate(36, 0)
                pos += 1
                rect_r -= 36
            pos = e
            delta = interpolate(self.zoom, (36*(e - s), 0))
            # round(36*(e - s)*(100 - self.zoom)/100.0)
            painter.translate(delta, 0)
            rect_r -= delta
            i += 1

        while pos < end and rect_r > 0:
            nucleotides[self.dna[pos]].draw(painter, 0, True)
            painter.translate(36, 0)
            pos += 1
            rect_r -= 36


    def paintProtein(self, ev, painter):

        _, _, _, _, genome = self.gene
        center = []
        for a in genome:
            center.append(nucleotides[a].rshape.boundingRect().center().y())
        y_center = mean(center)
        leftmost = (ev.rect().x()) // 36
        rightmost = (ev.rect().x() + ev.rect().width() + 35) // 36

        painter.translate(36 * leftmost, 10)
        painter.save()
        for pos in range(leftmost, rightmost):
            x = nucleotides[genome[pos]]
            x.draw(painter, 0, True)
            painter.translate(36, 0)
        painter.restore()

        painter.save()

        triplets = proteins(genome)

        for pos in range(leftmost, rightmost, 3):
            x = nucleotides[genome[pos]]
            am = triplets[int(pos/3)]
            if interpolate(self.zoom, (0, self.numAmins())) > pos/3:
                painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
                if aminos[am] in Yellow:
                    col = Qt.yellow
                elif aminos[am] in Green:
                    col = Qt.green
                elif aminos[am] in Pink:
                    col = QColor(150,0,150)
                elif aminos[am] in Blue:
                    col = Qt.blue
                painter.setBrush(QBrush(col, Qt.SolidPattern))
                painter.drawEllipse(QPoint(int(leftmost+ 35*1.5), int(y_center + 35*2.3)), 36*1.5, 36*1.5)
                painter.drawText(QPoint(int(leftmost+ 34*1.5), int(y_center + 35*2.3)), aminos[am])

                painter.translate(36*3, 0)
        painter.restore()

    def paintEvent(self, ev):
        try:
            painter = QPainter(self)
            if self.mode == self.M_SPLASH:
                painter.drawText(self.rect(), Qt.AlignCenter, 'BioSynth')
            elif self.mode == self.M_WHOLE:
                self.paintWholeGenome(ev, painter)
            elif self.mode == self.M_ZOOM:
                self.paintZoom(ev, painter)
            elif self.mode == self.M_INTRONS:
                self.paintIntrons(ev, painter)
            elif self.mode == self.M_SPLICE:
                self.paintSplice(ev, painter)
            elif self.mode == self.M_PROTEIN:
                self.paintProtein(ev, painter)
        except Exception as e:
            print('in paintEvent()', e)


if __name__ == "__main__":
    from sys import argv
    from PyQt5.QtWidgets import QApplication


    app = QApplication(argv)
    dna = DNAView()
    dna.setDNA('TATAATG'+'CTAGTCCCCAG'*7+'TAA')
    dna.selectGene(0)
    dna.setMode(dna.M_PROTEIN)

    win = QScrollArea()
    win.setWidget(dna)
    win.resize(1000, 500)


    slider1 = QSlider(Qt.Horizontal)
    slider1.valueChanged.connect(dna.setShiftBottom)
    slider1.setRange(0, 100)
    slider2 = QSlider(Qt.Horizontal)
    slider2.setRange(0, 100)
    slider2.valueChanged.connect(dna.setGray)
    slider3 = QSlider(Qt.Horizontal)
    slider3.setRange(0, 100)
    slider3.valueChanged.connect(dna.setShiftTop)

    slider4 = QSlider(Qt.Horizontal)
    slider4.setRange(0, 1000)
    slider4.valueChanged.connect(dna.setZoom)

    slider5 = QSlider(Qt.Horizontal)
    slider5.setRange(0, dna.numAmins())
    slider5.valueChanged.connect(dna.setProt)

    layout = QVBoxLayout()
    layout.addWidget(slider1)
    layout.addWidget(slider2)
    layout.addWidget(slider3)
    layout.addWidget(slider4)
    layout.addWidget(slider5)

    panel = QWidget()
    panel.setLayout(layout)
    #---------------------------------------------------------------------------

    spl = QSplitter(Qt.Vertical)
    spl.addWidget(win)
    spl.addWidget(panel)

    wid = QMainWindow()
    wid.setCentralWidget(spl)
    wid.resize(1000, 500)
    wid.show()

    win.show()
    dna.setFocus()
    app.exec()
