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
import os
import time
import data
import logger
import gmail
from aircraft import *
from SimConnect import *
from ui_a32x_tester import *

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cruise)
        self.pushButton_2.clicked.connect(self.quit)
        
    def log(self, msg, typ):
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {background-color: #E5E5E5; color: blue; font: 11px serif;}")
        if (typ == 1):
            self.plainTextEdit.appendPlainText(msg)
        else:
            self.plainTextEdit.insertPlainText(msg)
        self.plainTextEdit.repaint()
        
    def clearText(self):
        self.plainTextEdit.clear()
        
    def updateStatus(self, msg):
        self.statusBar().showMessage(msg)
        self.statusBar().repaint()
        
    def dumpToFile(self):
        f = open("test.txt", "w")
        dump = self.plainTextEdit.toPlainText()
        f.write(dump)
        f.close()
    def quit(self):
        exit()
        
    # Cruise test function
    def cruise(self):
        rnd = 1
        points = 200
        random.seed(0)
        cg = 0.27
        error_alt = 1
        error_tas = 1
        actual_vs = 1000
        n = 1
        
        # Read the Aircraft Data file
        df = data.data_read('CRZ')
        logger.test_header(self, "CRZ")
        if os.path.exists("test.txt"):
            os.remove("test.txt")
            
        start_time = time.time()
        
        if (rnd == 0):
            points = len(df.index)-1
            
        # Create the SimConnect link
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=0)
        ae = AircraftEvents(sm)
        logger.test_simconnect(self, 1)
        
        hsi = Event(b'HEADING_SLOT_INDEX_SET', sm)
        hsi(1)
    
        # Check and set initial aircraft settings:
        # AP1 ON, ATHR ON, FD ON & CLB
        ac_init(aq, ae)
        logger.test_init(self, 1)
            
        for i in range(n, points+1):
            if (rnd == 1):
                # Random Aircraft situation
                if (n == i):
                    start = n
                else:
                    start = 0
                   
                weight, altitude, tas, mach, n1 = data.a32x_state_rnd(df, start)
            else:
                weight, altitude, tas, mach, n1 = data.a32x_state_nrm(df, i)
            
            # Set Weight and CG ... this goes first to avoid excessive dumping
            W_n_B(aq, weight, cg)
            if (i == 1):
                logger.test_init(self, 0)
                logger.test_loop(self, 1)
            logger.test_obj(self, weight, cg, altitude, tas, mach, n1, i, points)
            
            # Main test point routine - Setting stable aircraft conditions   
            crz_alt_tas(sm, aq, ae, altitude, tas)
            
            # Altitude & Speed damping "filter". Use VS first as a measure
            # of stability
            # To avoid excesive damping, fuel and CG are set first with
            # enough headroom
            # A stability counter is implemented to account for VS damping
            counter = 0
            prev_n1 = 0
            ap_cycler = time.time()
            while counter < 50:
                if not (round(time.time() - ap_cycler) % 10):
                    actual_fcu_speed = float(aq.get("AUTOPILOT_AIRSPEED_HOLD_VAR"))
                    event_to_trigger = ae.find("AP_MASTER")
                    if (abs(actual_fcu_speed-tas) > 2):
                        crz_alt_tas(sm, aq, ae, altitude, tas)
                        print("FCU Trigger")
             
                    if (counter == 0):
                        print("AP Trigger")
                        event_to_trigger()
                        time.sleep(1)
                        event_to_trigger()
                    
                actual_alt = float(aq.get("INDICATED_ALTITUDE"))
                actual_tas = float(aq.get("AIRSPEED_TRUE"))
                actual_vs = float(aq.get("VERTICAL_SPEED"))         
                error_alt = round(abs((actual_alt-altitude)/altitude)*100,3)
                error_tas = round(abs((actual_tas-tas)/tas)*100,3)      
                
                if (error_alt < 0.5 and error_tas < 0.5 and abs(actual_vs) < 10):
                    actual_n1 = aq.get("TURB_ENG_N1:1")
                    print("Diff N1=" + str(actual_n1-prev_n1))
                    if (abs(float(actual_n1)-prev_n1) < 0.1):                  
                        counter += 1
                        print("counter=" + str(counter))
                        time.sleep(0.1)
                    else:
                        counter = 0
                    prev_n1 = float(actual_n1)
                    
                   
                elapsed_time = time.time()-start_time
                msg = "Tolerance Figures - Alt: " + str(error_alt) + "%  TAS: " + str(error_tas) + "%  VS: " + str(round(actual_vs,1)) + "fpm          Elapsed Time - " + str(round(elapsed_time,2)) + " secs."
                
                self.updateStatus(msg)
                QtCore.QCoreApplication.processEvents()
                   
            actual_weight = aq.get("TOTAL_WEIGHT")
            actual_alt = aq.get("INDICATED_ALTITUDE")
            actual_tas = aq.get("AIRSPEED_TRUE")
            actual_mach = aq.get("AIRSPEED_MACH")
            actual_vs = aq.get("VERTICAL_SPEED") 
            actual_cg = aq.get("CG_PERCENT")
            actual_fn = float(aq.get("TURB_ENG_JET_THRUST:1"))*2
            actual_n1 = aq.get("TURB_ENG_N1:1")
            actual_n2 = aq.get("TURB_ENG_N2:1")
            actual_n1_cor = aq.get("TURB_ENG_CORRECTED_N1:1")
            actual_n2_cor = aq.get("TURB_ENG_CORRECTED_N2:1")
            actual_egt_R = float(aq.get("GENERAL_ENG_EXHAUST_GAS_TEMPERATURE:1"))
            actual_egt = (actual_egt_R-491.67)*5/9
            actual_ff = float(aq.get("TURB_ENG_FUEL_FLOW_PPH:1"))*2*0.453592
            logger.test_actual(self, actual_weight, actual_cg, actual_alt, actual_tas, actual_mach, actual_vs, actual_fn, actual_n1, actual_n2, actual_n1_cor, actual_n2_cor, actual_egt, actual_ff, i, points)
            
            time.sleep(0.5)
            os.system('copy test.txt test.bck >NUL')
            self.dumpToFile()
            time.sleep(0.5)
            
            if not (i % 10):
                eta = ((time.time()-start_time)/i)*(points-i)
                if (eta > 3600):
                    eta = round(eta/3600, 2)
                    subject = "FBW Tester: ETA is " + str(eta)+ " hours"
                elif (eta < 3600 and eta > 60):
                    eta = round(eta/60)
                    subject = "FBW Tester: ETA is " + str(eta) + " minutes"
                else:
                    eta = eta
                    subject = "FBW Tester: ETA is " + str(eta) + " seconds"
                    
                gmail.gmail(subject)
            
        #sm.quit()
        logger.test_loop(self, 0)
        logger.test_simconnect(self, 0)
        self.dumpToFile()
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
