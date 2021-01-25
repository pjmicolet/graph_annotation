from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import yfinance as yf
import sys
import os
import pandas as pd

def getData(symbol):
    data = yf.Ticker(symbol)
    hist = data.history(period="max")
    return hist

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()

        self.textbox = QLineEdit(self)
        self.textbox.resize(280, 40)
        self.textbox.returnPressed.connect(self.on_pushButtonOk_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.textbox)

        widget = QWidget()
        widget.setLayout(layout)
    
        self.setCentralWidget(widget)

    def plotData(self, symbol):
        stock = getData(symbol)    

        time = pd.to_datetime( stock.index )
        self.graphWidget.clear()
        self.graphWidget.plot([ x.timestamp() for x in stock.index ], stock["Close"])

    @QtCore.pyqtSlot()
    def on_pushButtonOk_clicked(self):
        newStock = self.textbox.text()
        self.plotData(newStock)


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.plotData(sys.argv[1])
    main.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
