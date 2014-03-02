import sys

from PySide.QtCore import *
from PySide.QtGui import *

class NatGUI(QMainWindow):
  def __init__(self):
    super(NatGUI, self).__init__()
    self.initUI()


  def initUI(self):
    # layout basics
    rootLayout = QVBoxLayout()
    rootWidget = QWidget()
    
    # setup connection parameters:
    connectParamLayout = QHBoxLayout()
    comPort = QLineEdit("Enter serial port here!")
    connectButton = QPushButton("Connect!")
    connectParamLayout.addWidget(comPort)
    connectParamLayout.addWidget(connectButton)
    rootLayout.addLayout(connectParamLayout)

    # setup PID control params:
    pidParamLayout = QHBoxLayout()
    for param in ["Proportional", "Derivative", "Integral"]:
      fieldLayout = QHBoxLayout()
      fieldLayout.addWidget(QLabel(param+":"))
      fieldLayout.addWidget(QDoubleSpinBox())
      pidParamLayout.addLayout(fieldLayout)
    pidParamLayout.addWidget(QPushButton("Set PID Constants!"))
    rootLayout.addLayout(pidParamLayout)
    
    rootWidget.setLayout(rootLayout)
    self.setCentralWidget(rootWidget)

    self.statusBar().showMessage('Hello! Welcome to NatGUI!')
    #self.setGeometry(300, 300, 250, 150)
    self.setWindowTitle('NatGUI')    
    self.show()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  natgui = NatGUI()
  sys.exit(app.exec_())
