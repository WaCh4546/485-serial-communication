from PySide2 import QtWidgets
from pyqtgraph.Qt import  QtCore
import pyqtgraph as pg
import sys
from random import randint
import  pandas  as pd
import xlrd
from PyQt5.QtWidgets import QFileDialog
title=''
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('历史数据')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        dakai=fileMenu.addAction("打开")
        dakai.triggered.connect(self.process)
        # 创建 PlotWidget 对象
        self.pw = pg.PlotWidget()

        # 设置图表标题
        self.pw.setTitle(title,
                         color='008080',
                         size='12pt')

        # 设置上下左右的label
        self.pw.setLabel("left","模型输出值")
        self.pw.setLabel("bottom","时间")

        # 设置Y轴 刻度 范围
        self.pw.setYRange(min=-10, # 最小值
                          max=50)  # 最大值

        # 显示表格线
        self.pw.showGrid(x=True, y=True)

        # 背景色改为白色
        self.pw.setBackground('w')

        # 设置Y轴 刻度 范围
        self.pw.setYRange(min=-10, # 最小值
                          max=50)  # 最大值

        # 居中显示 PlotWidget
        self.setCentralWidget(self.pw)

       

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.curve = self.pw.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

        self.i = 0
        self.x = [] # x轴的值
        self.y = [] # y轴的值
       

        # plot data: x, y values
        self.curve.setData(self.x,self.y)
    def process(self):
        name,_ = QFileDialog.getOpenFileName(None,'打开文件','.','Excel files(*.xlsx , *.xls)') 
        worksheet = xlrd.open_workbook(name)
        booksheet = worksheet.sheet_by_index(0)
        sheet_names= worksheet.sheet_names()
        self.pw.setTitle(name,
                         color='008080',
                         size='12pt')
        row_0 = booksheet.col_values(0)
        row_1 = booksheet.col_values(1)
        self.x=row_0      
        self.y=row_1
        self.curve.setData(self.x,self.y)   
if __name__ == '__main__':
    app = QtWidgets.QApplication()
    main = MainWindow()
    main.show()
    app.exec_()