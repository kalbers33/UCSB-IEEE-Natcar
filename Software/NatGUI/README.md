# NATGUI
Simple GUI interface to communicate with the NatCar over an XBee network.

masoug@gmail.com for any questions about NatGUI.

## Quick Start
NatGUI is written in Python, so make sure you have the python interpreter installed.

Additional Dependencies (All are required):
* [PySide](http://qt-project.org/wiki/PySide): Python bindings for Qt GUI toolkit.
* [PySerial](http://pyserial.sourceforge.net/): Python interface for serial communications.
* [PyQWT](http://pyqwt.sourceforge.net/): Python bindings for the QWT widget toolkit.

Once you have those installed, just run 'python natgui.py' to bring up the interface. Enter the serial port your XBee is connected to and hit the "Connect!" button. If successfully connected, then the botton status bar indicate successful connection. If not, an error messsage will pop up with diagnostic information.
