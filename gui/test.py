from typing import List

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from pmath.functions.test_functions import *
#parabolaxy, parabolaxy_region, MathFunction
from optimization.optimization_method import SimulatedAnnealing
from optimization.pso import ParticleSwarmOptimization

## Always start by initializing Qt (only once per application)
from pmath.util.hcuberegion import HCubeRegion


class SuperOkienkoAsi:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.cases = []
        ## Define a top-level widget to hold everything
        self.w = QtGui.QWidget()
        self.iter = -1
        self.active_case = None

        left_side = QtGui.QGroupBox()
        right_side = QtGui.QGroupBox()

        ## Create some widgets to be placed inside
        left_graph = pg.PlotWidget()
        self.case_list = QtGui.QComboBox()
        back = QtGui.QPushButton('<|')
        play_button = QtGui.QPushButton('>')
        forward = QtGui.QPushButton('|>')

        text_box = QtGui.QTextEdit()
        load = QtGui.QPushButton('load')
        save = QtGui.QPushButton('save')
        execute = QtGui.QPushButton('EXECUTE :(')

        text_font = QtGui.QFont()
        text_font.setFamily("Courier")
        text_font.setStyleHint(QtGui.QFont.Monospace)
        text_font.setFixedPitch(True)
        text_font.setPointSize(10)

        tab_const = 4
        metrics = QtGui.QFontMetrics(text_font)

        text_box.setFont(text_font)
        text_box.setTabStopWidth(tab_const * metrics.width(' '))

        ## Create a grid layout to manage the widgets size and position
        layout = QtGui.QGridLayout()
        self.w.setLayout(layout)

        ## Add widgets to the layout in their proper positions
        layout.addWidget(left_side, 0, 0)
        layout.addWidget(right_side, 0, 1)

        left_layout = QtGui.QGridLayout()
        right_layout = QtGui.QGridLayout()

        left_layout.addWidget(left_graph, 0, 0, 3, 3)
        left_layout.addWidget(self.case_list, 4, 1)
        left_layout.addWidget(back, 5, 0)
        left_layout.addWidget(play_button, 5, 1)
        left_layout.addWidget(forward, 5, 2)


        self.gradient = pg.GradientWidget()
        step = 0.1
        x = 0
        while x <= 1.0:
            self.gradient.addTick(x, pg.mkColor(255*x,255*(1-x), 0))
            self.gradient.addTick(x+step/20, pg.mkColor(0,0,0))
            #self.gradient.addTick(x+step/5, pg.mkColor(0,0,0))
            self.gradient.addTick(x+step/10, pg.mkColor(255*x,255*(1-x), 0))
            x += step


        right_layout.addWidget(text_box, 0, 0, 3, 3)
        right_layout.addWidget(load, 4, 0)
        right_layout.addWidget(save, 4, 1)
        right_layout.addWidget(execute, 4, 2)

        left_side.setLayout(left_layout)
        right_side.setLayout(right_layout)

        self.left_graph = left_graph

        self.case_list.currentIndexChanged.connect(lambda case: self.set_active_case(case))

        back.clicked.connect(self.update_iter_back)
        forward.clicked.connect(self.update_iter_forward)

        self.autoplay = False
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_iter_forward)

        print(timer)

        play_button.clicked.connect(lambda: self.play(timer))

        execute.clicked.connect(lambda: self.execute(text_box))
        ## Display the widget as a new window

    def go(self):
        self.w.show()

        ## Start the Qt event loop
        self.app.exec_()

    def update_iter_back(self):
        self.iter = max(0, self.iter - 1)
        self.draw_active_case()

    def update_iter_forward(self):
        if self.active_case is not None:
            self.iter = min(self.iter + 1, len(self.active_case[1]) - 1)
            if self.iter == len(self.active_case[1]) - 1:
                self.autoplay = False
            self.draw_active_case()

    def execute(self, edit_field: QtGui.QTextEdit):
        exec(edit_field.toPlainText())

    def add_result(self, nazwa: str, punkty: List[List[List[float]]]):
        self.cases.append((nazwa, punkty))
        self.refresh_combobox()

    def refresh_combobox(self):
        self.case_list.clear()
        for nazwa, punkty in self.cases:
            self.case_list.addItem(nazwa)

    def set_active_case(self, case: int):
        self.active_case = None
        if case >= 0:
            self.active_case = self.cases[case]
            self.iter = -1
            self.draw_active_case()
            print(self.active_case[0], self.iter)

    def draw_case(self, iter: int, prev = False):
        if iter < 0:
            return
        i = 0
        #pen = pg.mkPen(width=1, color=pg.intColor(i, hues=100,minValue=10)))
        for punkt in self.active_case[1][iter]:
            col = QtGui.QColor(QtGui.QColor.colorNames()[(13 * i) % 148])
            #print(col.name())
            if prev is True:
                col.setAlpha(60)
            self.left_graph.addItem(
                pg.PlotDataItem([punkt[0]], [punkt[1]], lines=None, symbol="x", symbolPen=pg.mkPen(width=1,
                                                                                                   color=col)))
            i += 1
        return

    def draw_active_case(self):
        self.left_graph.getPlotItem().clear()
        self.left_graph.addItem(self.img)
        self.draw_case(self.iter - 1, prev=True)
        self.draw_case(self.iter)
        # self.left_graph.

    def set_function_and_region(self, func: MathFunction, region: HCubeRegion = None, step=0.01):
        if func.input_dim() != 2:
            raise ValueError("We only draw R^2 -> R functions. Please input gud function dud")

        if region is None:
            region = HCubeRegion([0, 0], [1, 1])

        xmin, ymin = region.ranges[0][0], region.ranges[1][0]
        xmax, ymax = region.ranges[0][1], region.ranges[1][1]

        x, y = xmin, ymin
        all_points = []
        while x <= xmax:
            y = ymin
            points = []
            while y <= ymax:
                points.append(func([x, y]))
                y += step
            x += step
            all_points.append(points)

        np_array = np.array(all_points)
        print(np_array)
        img = pg.ImageItem()




        img.setLookupTable(self.gradient.getLookupTable(100))
        img.setImage(np_array)

        #img.setLevels([[0, 4], [0, 255], [0, 255]])

        image_region = QtCore.QRectF(xmin, ymin, (xmax - xmin), (ymax - ymin))
        img.setRect(image_region)

        self.left_graph.getPlotItem().clear()
        self.left_graph.addItem(img)
        self.img = img

    def play(self, timer: QtCore.QTimer):
        self.autoplay = not self.autoplay
        print(self.autoplay)
        print(timer)
        if self.autoplay:
            timer.start(1000)
        else:
            timer.stop()


def test():
    mojaOkienko = SuperOkienkoAsi()
    mojaOkienko.go()
