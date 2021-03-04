##################################################
## SimConnect Testbench
##
##################################################
## Author: J.M. Roldan
## Date: 12/17/2020
## License: GPL 3.0
## Discord: TazX [Z+1]#0405
## Status: WIP
##################################################
import profile
import random
import threading
from ui_a32x_tester import *

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(cruise)
        
    def log(self, msg):
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {background-color: #E5E5E5; color: blue; font: 12px serif;}")
        self.plainTextEdit.appendPlainText(msg)
        self.plainTextEdit.repaint()
        
    def updateStatus(self, msg):
        self.statusBar().showMessage(msg)
        self.statusBar().repaint()
        
def cruise():
    random.seed(0)
    points = 20
    thread_crz = threading.Thread(target = profile.cruise, args=(w, points))
    thread_crz.start()
    #profile.cruise(w, points)  
    
if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication([])
    w = MainWindow()
    font = w.font()
    font.setPointSize(8)
    w.setFont(font) 
    w.show()
    app.exec_()
