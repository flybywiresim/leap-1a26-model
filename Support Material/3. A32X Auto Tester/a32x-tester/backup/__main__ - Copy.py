#--------------------------------------------------
# FBW Aircraft  Tester
#--------------------------------------------------
# Author: J.M. Roldan
# Date: 12/17/2020
# License: GPL 3.0
# Discord: TazX [Z+1]#0405
# Status: WIP
#--------------------------------------------------
import random
import time
import data
import logger
from aircraft import *
from SimConnect import *
from ui_a32x_tester import *

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cruise)
        
    def log(self, msg):
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {background-color: #E5E5E5; color: blue; font: 12px serif;}")
        self.plainTextEdit.appendPlainText(msg)
        self.plainTextEdit.repaint()
        
    def clearText(self):
        self.plainTextEdit.clear()
        
    def updateStatus(self, msg):
        self.statusBar().showMessage(msg)
        self.statusBar().repaint()
    
    # Cruise test function
    def cruise(self):
        points = 20
        random.seed(0)
        cg = 0.33
        error_alt = 1
        error_ias = 1
        actual_vs = 1000
        
        # Read the Aircraft Data file
        df = data.data_read('CRZ')
        logger.test_header(self, "CRZ")
        start_time = time.time()
        i = 1
        # Random Aircraft situation
        weight, altitude, ias = data.a32x_state(df)
        logger.test_env(self, weight, altitude, ias, i, points)
        
        # Create the SimConnect link
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=0)
        ae = AircraftEvents(sm)
        
        # Check and set initial aircraft settings:
        # AP1 ON, ATHR ON, FD ON & CLB
        ac_init(aq, ae)
        
        # Set Weight and CG ... this goes first to avoid excessive dumping
        W_n_B(aq, weight, cg)
        
        # Main test point routine - Setting stable aircraft conditions   
        crz_alt_ias(sm, aq, ae, altitude, ias)
        
        # Altitude & Speed damping "filter". Use VS first as a measure
        # of stability
        # To avoid excesive damping, fuel and CG are set first with
        # enough headroom  
        
            
        while error_alt > 1 or error_ias > 1 or abs(actual_vs) > 10:
            actual_alt = aq.get("INDICATED_ALTITUDE")
            actual_ias = aq.get("AIRSPEED_INDICATED")
            actual_vs = aq.get("VERTICAL_SPEED")            
            error_alt = round(abs((actual_alt-altitude)/altitude)*100,3)
            error_ias = round(abs((actual_ias-ias)/ias)*100,3)
            elapsed_time = time.time()-start_time
            msg = "Tolerance Figures - Alt: " + str(error_alt) + "%  IAS: " + str(error_ias) + "%  VS: " + str(round(actual_vs,1)) + "fpm          Elapsed Time - " + str(round(elapsed_time,2)) + " secs."
            self.updateStatus(msg)
            QtCore.QCoreApplication.processEvents()
        
        #print(error_alt, " ", error_ias, " ", actual_vs)        
        print(aq.get("TOTAL_WEIGHT"))
        print(aq.get("CG_PERCENT"))
        #sm.quit()
        #exit()

def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication([])
    w = MainWindow()
    font = w.font()
    font.setPointSize(8)
    w.setFont(font) 
    w.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
