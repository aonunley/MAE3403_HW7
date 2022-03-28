from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Rankine_Gui import Ui_Form
from PyQt5 import uic
import sys
from PyQt5 import QtWidgets as qtw

from Rankine import rankine
from Steam import steam


class Mainwindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        '''
        Main Window Constructor
        '''
        super().__init__()
        self.setupUi(self)
        self.btn_Calculate.clicked.connect(self.calcRankine)
        self.tmpLoop = ''
        self.setWindowTitle('Rankine Cycle Calculator')
    # main UI code goes here


    def calcRankine(self):

        if self.rdo_Quality.isChecked():
            t_high = None
            quality = float(self.le_TurbineInletCondition.text())
        else:
            t_high = float(self.le_TurbineInletCondition.text())
            quality = None
        ph = int(self.le_PHigh.text())
        pl = float(self.le_PLow.text())
        r1 = rankine(pl, ph, t_high, name='Rankine Cycle', x=quality)
        r1.calc_efficiency()
        #  define the states using our R1 with the steam class
        state1 = r1.state1  # type: steam
        state2 = r1.state2  # type: steam
        state3 = r1.state3  # type: steam
        state4 = r1.state4  # type: steam
        #  set the text boxes to the h values for each of those states with only 2 decimal places
        self.le_H1.setText("{:.2f}".format(float(state1.h)))
        self.le_H2.setText("{:.2f}".format(float(state2.h)))
        self.le_H3.setText("{:.2f}".format(float(state3.h)))
        self.le_H4.setText("{:.2f}".format(float(state4.h)))
        self.le_TurbineWork.setText("{:.2f}".format(float(r1.turbine_work)))
        self.le_PumpWork.setText("{:.2f}".format(float(r1.pump_work)))
        self.le_HeatAdded.setText("{:.2f}".format(float(r1.heat_added)))
        self.le_Efficiency.setText("{:.2f}".format(float(r1.efficiency)))


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec_()