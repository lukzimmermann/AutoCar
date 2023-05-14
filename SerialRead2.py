import serial
import numpy as np
import matplotlib.pyplot as plt

port = "/dev/tty.usbserial-0001"
speed = 230400

ser = serial.Serial(port, speed)

def parseByte(lsb, msb):
    msb = msb << 8
    return lsb + msb

data = [] 

counter = 0
dataBigSet = []
while counter < 38:
    isReading = True

    while isReading:
        byte = ser.read()

        if byte == b'\x54': 
            data.append(byte)
            
            
            while isReading:
                byte = ser.read()
                if byte == b'\x54':
                    isReading = False
                else:
                    data.append(byte)


        intData = []
        

        for i in data:
            int_val = int.from_bytes(i, "big")
            intData.append(int_val)
        

        dataArray = []
        #print(intData)
        if len(intData) > 4 and intData[1] == 44 and len(intData) == 47:
            speed = parseByte(intData[2], intData[3])
            startAngle = parseByte(intData[4], intData[5])
            endAngle = parseByte(intData[42], intData[43])
            step = (endAngle -startAngle)/11

            startByte = 6
            
            for i in range(12):
                dataSet = []
                distance = parseByte(intData[startByte+i*3], intData[startByte+i*3+1])
                intensity = intData[startByte+i*3+2]
                angle = startAngle + step * i
                dataSet.append(distance)
                dataSet.append(round(angle/100,1))
                dataSet.append(intensity)
                dataArray.append(dataSet)
            
            for data in dataArray:
                dataBigSet.append(data)

            counter += 1

        intData = []
        data = []

#print(dataBigSet)

points = []

for datapoint in dataBigSet:
    coor = []
    x = datapoint[0] * np.cos(round(datapoint[1]/180*np.pi,2))
    y = datapoint[0] * np.sin(round(datapoint[1]/180*np.pi,2))
    coor.append(x)
    coor.append(y)
    points.append(coor)

print(points)

for point in points:
    plt.scatter(point[1], point[0])

plt.show()
