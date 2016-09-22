from typing import List

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from pmath.functions.test_functions import parabolaxy, parabolaxy_region, MathFunction
from optimization.optimization_method import SimulatedAnnealing

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
        play = QtGui.QPushButton('>')
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
        left_layout.addWidget(play, 5, 1)
        left_layout.addWidget(forward, 5, 2)

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

        play.clicked.connect(lambda timer: self.play(timer))


        execute.clicked.connect(lambda: self.execute(text_box))
        ## Display the widget as a new window

    def go(self):
        self.w.show()

        ## Start the Qt event loop
        self.app.exec_()

    def update_iter_back(self):
        self.iter = max(0, self.iter - 1)
        #self.draw_active_case()
        self.remove_last_iter()

    def update_iter_forward(self):
        if self.active_case is not None:
            self.iter = min(self.iter + 1, len(self.active_case[1]) - 1)
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
            self.draw_active_case()
            self.iter = -1
            print(self.active_case[0], self.iter)

    def draw_active_case(self):
        if self.active_case is None:
            return
        if self.iter < 0:
            return
        tempx = []
        tempy = []
        for punkt in self.active_case[1][self.iter]:
            tempx.append(punkt[0])
            tempy.append(punkt[1])
        self.left_graph.addItem(pg.PlotDataItem(tempx, tempy, lines=None, symbol="x", symbolPen=pg.mkPen(width=2, color=pg.intColor(self.iter, hues=25, minValue=10))))
        print(item for item in self.left_graph.getPlotItem().items)
        #self.left_graph.plot(tempx, tempy, lines=None, symbol="x", symbolPen=pg.mkPen(width=2, color=pg.intColor(self.iter, hues=25, minValue=10, values=10)))

    def remove_last_iter(self):
        if self.active_case is None:
            return
        if self.iter < 1:
            return
        tempx = []
        tempy = []
        for punkt in self.active_case[1][self.iter - 1]:
            tempx.append(punkt[0])
            tempy.append(punkt[1])
        self.left_graph.removeItem(pg.PlotDataItem(tempx, tempy))


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
        img.setImage(np_array)

        image_region = QtCore.QRectF(xmin, ymin, (xmax - xmin), (ymax - ymin))
        img.setRect(image_region)

        self.left_graph.getPlotItem().clear()
        self.left_graph.addItem(img)
        self.img = img

    def play(self, timer: QtCore.QTimer):
        self.autoplay = not self.autoplay
        print(self.autoplay)
        if self.autoplay:
            timer.start(50)
        else:
            timer.stop()


def test():
    mojaOkienko = SuperOkienkoAsi()
    mojaOkienko.go()
