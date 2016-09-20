from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from pmath.functions.test_functions import parabolaxy
from optimization.optimization_method import SimulatedAnnealing

## Always start by initializing Qt (only once per application)
class SuperOkienkoAsi:
    def __init__(self):
        self.app = QtGui.QApplication([])

        ## Define a top-level widget to hold everything
        self.w = QtGui.QWidget()

        left_side = QtGui.QGroupBox()
        right_side = QtGui.QGroupBox()

        ## Create some widgets to be placed inside
        left_graph = pg.PlotWidget()
        algorithm_list = QtGui.QComboBox()
        back = QtGui.QPushButton('<|')
        play = QtGui.QPushButton('>')
        forward = QtGui.QPushButton('|>')

        right_graph = QtGui.QTextEdit()
        load = QtGui.QPushButton('load')
        save = QtGui.QPushButton('save')
        execute = QtGui.QPushButton('EXECUTE :(')


        text_font = QtGui.QFont()
        text_font.setFamily("Courier")
        text_font.setStyleHint(QtGui.QFont.Monospace)
        text_font.setFixedPitch(True)
        text_font.setPointSize(10)

        tab_const = 4
        metrics =  QtGui.QFontMetrics(text_font)

        right_graph.setFont(text_font)
        right_graph.setTabStopWidth(tab_const * metrics.width(' '))


        ## Create a grid layout to manage the widgets size and position
        layout = QtGui.QGridLayout()
        self.w.setLayout(layout)

        ## Add widgets to the layout in their proper positions
        layout.addWidget(left_side, 0, 0)
        layout.addWidget(right_side, 0, 1)

        left_layout = QtGui.QGridLayout()
        right_layout = QtGui.QGridLayout()

        left_layout.addWidget(left_graph, 0, 0, 3, 3)
        left_layout.addWidget(algorithm_list, 4, 1)
        left_layout.addWidget(back, 5, 0)
        left_layout.addWidget(play, 5, 1)
        left_layout.addWidget(forward, 5, 2)


        right_layout.addWidget(right_graph, 0, 0, 3, 3)
        right_layout.addWidget(load, 4, 0)
        right_layout.addWidget(save, 4, 1)
        right_layout.addWidget(execute, 4, 2)

        left_side.setLayout(left_layout)
        right_side.setLayout(right_layout)
        #QtCore.QObject.connect(play, QtCore.SIGNAL("clicked()"), self.dont_go)
        play.clicked.connect(lambda: self.dont_go(play))
        execute.clicked.connect(lambda: self.execute(right_graph))
        ## Display the widget as a new window

    def go(self):
        self.w.show()

        ## Start the Qt event loop
        self.app.exec_()

    def dont_go(self, cokliklem: QtGui.QPushButton):

        print("plis stay asia kocham cie", cokliklem)

    def execute(self, edit_field: QtGui.QTextEdit):
        exec(edit_field.toPlainText())

    def add_result(self, nazwa, punkty):
        pass

def test():
    mojaOkienko = SuperOkienkoAsi()
    mojaOkienko.go()