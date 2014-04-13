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

class SerialWorker(QThread):
  def __init__(self):
    super(SerialWorker, self).__init__()
    self.serialPort = None
    self.isPolling = False
    self.cmdBuffer = list()

  def run(self):
    self.isPolling = True
    while self.isPolling and self.serialPort:
      try:
        # all communication goes through the command/response cycle.
        if self.cmdBuffer:
          cmd, callback = self.cmdBuffer.pop(0)
          print "Sending command:", cmd
          # COMMAND
          self.serialPort.write(cmd)
          # RESPONSE
          resp = self.serialPort.read(3)
          self.serialPort.flush()
          if resp == "AOK":
            # OK response; invoke callback
            callback("AOK", None, None)
          elif resp == "DAT":
            # DATA response; get data length and read it
            # read next 4 characters; length of data
            dataLen = self.serialPort.read(4)
            dataLen = int(dataLen)
            # then read that datalength:
            data = self.serialPort.read(dataLen)
            # then invoke callback:
            callback("DAT", data, dataLen)
          elif resp == "ERR":
            # non-critical error;
            # read error-message length
            errLen = self.serialPort.read(4)
            errLen = int(errLen)
            error = self.serialPort.read(errLen)
            # invoke callback
            callback("ERR", error, errLen)
          else:
            # invalid response--help!
            print "Recieved invalid response from remote!"
        self.serialPort.flushInput()
      except Exception as e:
        QMessageBox.critical(self, "EXCEPTION", "Serial communication loop failed;"+str(e))
        self.stopThread()
  
  def sendCommand(self, command, callback):
    self.cmdBuffer.append((command, callback))

  def stopThread(self):
    self.isPolling = False

  def setPort(self, serialPort):
    self.serialPort = serialPort

class NatGUI(QMainWindow):
  def __init__(self):
    super(NatGUI, self).__init__()
    self.serialPort = serial.Serial()
    self.serialThread = SerialWorker()
    self.initUI()
 
  def gracefulStop(self):
    self.serialThread.stopThread()
    self.serialThread.wait()
    self.serialThread.quit()
    if self.serialPort.isOpen():
      print "Closing connections..."
      self.serialPort.close()
    print "Connection closed!"

  def getSerialPorts(self):
    self.comPort.clear()
    for port in list(serial_ports()):
      self.comPort.addItem(port)

  def restartThread(self):
    if self.serialThread.isRunning():
      self.gracefulStop()
    self.serialThread.start()

  def doConnect(self):
    port = self.comPort.currentText()
    print "Connecting to:", port
    if self.serialPort.isOpen():
      self.serialPort.close()
    self.serialPort.port = port
    self.serialPort.timeout = 5.0
    self.serialPort.baudrate = 9600
    self.serialPort.open()
    self.serialThread.setPort(self.serialPort)
    # handshake with remote
    self.serialThread.sendCommand("HAI", self.onPing)
    
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

  # CALLBACKS
  def onPing(self, status, response, length):
    if status == "AOK":
      print "Remote is okay :)"
      self.statusBar().showMessage('Successfully connected to remote!')
      self.restartThread()
    else:
      QMessageBox.critical(self, "Error", "Cannot connect to remote. Check console for details.")
      print "Remote host did not respond properly."

if __name__ == "__main__":
  app = QApplication(sys.argv)
  natgui = NatGUI()
  app.aboutToQuit.connect(natgui.gracefulStop)
  sys.exit(app.exec_())
