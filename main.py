import xboxController as xbc
import lidar
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import time
import csv
from dotenv import load_dotenv
import os
import threading
import serial

controller = xbc.XboxController()

#lid = lidar.Lidar("/dev/tty.usbserial-0001", 230400)

plt.ion()
points = []
hasToRun = True

port = '/dev/tty.usbserial-DN069WMS'
speed = 115200
ser = serial.Serial(port, speed)
start = 0


def updateMap():
    plt.clf()
    x = []
    y = []
    c = []
    
    start = time.time()
    points = lid.getMap()
    for point in points:
        if point[2] > 150:
            x.append(point[1])
            y.append(point[0])
            c.append(point[2])
    
    print(f'TimePerScan: {time.time()-start}')

    RADIUS = 6000
    plt.scatter(x, y, c=c, cmap=cm.plasma, vmin=150, vmax=255 )
    plt.ylim(RADIUS * -1, RADIUS)
    plt.xlim(RADIUS * -1, RADIUS)
    plt.grid()
    plt.colorbar()
    plt.show()
    plt.pause(0.01)

    #file = open('scan.csv', 'w')
    #writer = csv.writer(file)

    #for point in points: 
    #    dataLine = [point[0], point[1]]
    #    writer.writerow(dataLine)

    #file.close()
lastCommand = ''
while True:
    x, y, z, buttonA= controller.getValues()
    #print(x, y, z)
    command = f'{{"Steering": {int(x*-1)},"Throttle": {int(y)}, "A-Button":{buttonA}}}\n'
    
    if lastCommand != command:
        ser.write(command.encode('ASCII'))
        print(command)
    lastCommand = command

#event = threading.Event()

#lidarThread = threading.Thread(target=updateMap)
#lidarThread.start()




