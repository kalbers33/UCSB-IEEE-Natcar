import serial
import sys

port = serial.Serial(port=sys.argv[1], baudrate=int(sys.argv[2]))
buf = str()

while True:
  if port.inWaiting() > 0:
    buf += port.read(port.inWaiting())
    if "\n" in buf:
      buf = buf.strip()
      sys.stdout.write(buf+"\n")
      sys.stdout.flush()
      buf = str()
