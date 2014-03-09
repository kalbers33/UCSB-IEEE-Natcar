import sys
import os

import serial
from serial.tools import list_ports
from PySide.QtCore import *
from PySide.QtGui import *

# borrowed from: http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def serial_ports():
  """
  Returns a generator for all available serial ports
  """
  if os.name == 'nt':
    # windows
    for i in range(256):
        try:
            s = serial.Serial(i)
            s.close()
            yield 'COM' + str(i + 1)
        except serial.SerialException:
            pass
  else:
    # unix
    for port in list_ports.comports():
      yield port[0]

class SerialEngine(QObject):
  onReceive = Signal()
  onConnect = Signal()
  onDisconnect = Signal()
  finished = Signal()
  
  def __init__(self):
    super(SerialEngine, self).__init__()
    self.serialPort = serial.Serial()
    self.poll = False

  def make_connect(self, port, baudrate=9600):
    print "Connecting to:", port
    if self.serialPort.isOpen():
      self.serialPort.close()
    self.serialPort.port = port
    self.serialPort.timeout = 5.0
    try:
      self.serialPort.open()
      # handshake with remote
      self.serialPort.write("HELLO")
      if self.serialPort.read(len("HAI")) != "HAI":
        raise Exception("Remote host did not respond properly.")
      self.onConnect.emit()
      self.poll = True
      return True
    except Exception as e:
      print "Failed to connect:", str(e)
      self.poll = False
      self.onDisconnect.emit()
      return False

  def loop_poll(self):
    while self.serialPort.isOpen() and self.poll:
      # do polling
      #print "YEHAW"
      pass
    self.finished.emit()

  def disconnect(self):
    self.poll = False
    if self.serialPort.isOpen():
      print "Closing connections..."
      self.serialPort.close()
    self.onDisconnect.emit()

class NatGUI(QMainWindow):
  def __init__(self):
    super(NatGUI, self).__init__()
    self.serialEngine = SerialEngine()
    self.serialThread = QThread()
    self.serialEngine.moveToThread(self.serialThread)
    self.serialThread.started.connect(self.serialEngine.loop_poll)
    self.serialEngine.finished.connect(self.serialThread.quit)
    self.serialEngine.finished.connect(self.serialEngine.deleteLater)
    self.serialThread.finished.connect(self.serialThread.deleteLater)
    self.initUI()
 
  def gracefulStop(self):
    self.serialEngine.disconnect()
    self.serialThread.wait()
    self.serialThread.quit()

  def getSerialPorts(self):
    self.comPort.clear()
    for port in list(serial_ports()):
      self.comPort.addItem(port)

  def doConnect(self):
    if self.serialThread.isRunning():
      self.gracefulStop()
    if not self.serialEngine.make_connect(self.comPort.currentText()):
      QMessageBox.critical(self, "Error", "Cannot connect to remote. Check console for details.")
    else:
      # start polling thread
      self.serialThread.start()
      self.statusBar().showMessage('Successfully connected to remote!')
    
  def initUI(self):
    # layout basics
    rootLayout = QVBoxLayout()
    rootWidget = QWidget()
    
    # setup connection parameters:
    connectParamLayout = QHBoxLayout()
    self.comPort = QComboBox()
    self.getSerialPorts()
    connectButton = QPushButton("Connect!")
    connectButton.clicked.connect(self.doConnect)
    refreshButton = QPushButton("Refresh ports")
    refreshButton.clicked.connect(self.getSerialPorts)
    connectParamLayout.addWidget(self.comPort)
    connectParamLayout.addWidget(refreshButton)
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
  app.aboutToQuit.connect(natgui.gracefulStop)
  sys.exit(app.exec_())
