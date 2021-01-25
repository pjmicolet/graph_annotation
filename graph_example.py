from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import yfinance as yf
import sys
import os
import pandas as pd
from random import randint
from random import seed

def getData(symbol:str):
    data = yf.Ticker(symbol)
    hist = data.history(period="max")
    return hist

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget() 
        self.graphWidget.setBackground('w')

        self.textbox = QLineEdit(self)
        self.textbox.resize(280, 40)
        self.textbox.returnPressed.connect(self.on_pushButtonOk_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.textbox)

        widget = QWidget()
        widget.setLayout(layout)
    
        self.setCentralWidget(widget)
            
        seed( 1337 )

    def plotData(self, symbols:list):
        self.graphWidget.clear()
        for symbol in symbols:
            dataType = "Close"
            label = symbol
            if "@" in symbol:
                dataType = symbol.split("@")[1]
                symbol = symbol.split("@")[0]
            brush = (randint(0,200),randint(0,200),randint(0,200))
            stock = getData(symbol)    
            time = pd.to_datetime( stock.index )
            pen = pg.mkPen(color=brush)
            self.graphWidget.addLegend()
            self.graphWidget.plot([ x.timestamp() for x in stock.index ], stock[dataType],pen=pen,name=label)

    @QtCore.pyqtSlot()
    def on_pushButtonOk_clicked(self):
        newStock = self.textbox.text().split(" ")
        self.plotData(newStock)


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
