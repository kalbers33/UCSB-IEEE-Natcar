import sys, os, serial

def main(port):
  comPort = serial.Serial(port, 9600)
  while True:
    command = comPort.read(3) # read three-letter command
    print "Process command:", command
    if command == "HAI":      # ping back
      print "Ping back AOK"
      comPort.write("AOK")
    comPort.flush()

if __name__ == "__main__":
  main(sys.argv[1])
