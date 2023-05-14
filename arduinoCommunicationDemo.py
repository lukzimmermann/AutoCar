import serial

port = '/dev/tty.usbserial-DN069WMS'
speed = 115200
ser = serial.Serial(port, speed)
start = 0

counter = 0
try:
    message = '{"Steering": -1000,"Throttle": 23}\n'
    ser.writelines(message.encode())
except:
  print("An exception occurred")
finally:
  ser.close()

    