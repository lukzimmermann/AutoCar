import xboxController as xbc
import lidar
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import csv
from dotenv import load_dotenv
import os


controller = xbc.XboxController()

lid = lidar.Lidar("/dev/tty.usbserial-0001", 230400)

plt.ion()
points = []
hasToRun = True

while hasToRun:
    #hasToRun = False
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

#while True:
#    x, y, z = controller.getValues()
#    print(x, y, z)

