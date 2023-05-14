import serial
import numpy as np
import time

class Lidar:
    
    def __init__(self, port, speed):
        self.port = port
        self.speed = speed
        self.ser = serial.Serial(self.port, self.speed)
        self.start = 0


    def readPacket(self):
        data = []  
        isReading = True

        while isReading:
            byte = self.ser.read()
            if byte == b'\x54': 
                data.append(byte)
                counter  = 0
                while counter < 46:
                    data.append(self.ser.read())
                    counter += 1

                isReading = False

                intData = []
            
                for i in data:
                    int_val = int.from_bytes(i, "big")
                    intData.append(int_val)

        return intData


    def parsePacket(self, data):
        
        def parseByte(lsb, msb):
            msb <<= 8
            return lsb + msb

        dataArray = []
        if len(data) > 4 and data[1] == 44 and len(data) == 47:
            speed = parseByte(data[2], data[3])
            startAngle = parseByte(data[4], data[5])
            endAngle = parseByte(data[42], data[43])
            step = (endAngle -startAngle)/11

            startByte = 6
            
            for i in range(12):
                dataSet = []
                distance = parseByte(data[startByte+i*3], data[startByte+i*3+1])
                intensity = data[startByte+i*3+2]
                angle = startAngle + step * i
                dataSet.append(distance)
                dataSet.append(round(angle/100,1))
                dataSet.append(intensity)
                dataArray.append(dataSet)

        return dataArray


    def getDataSet(self):
        dataSet = self.parsePacket(self.readPacket()) 
        while len(dataSet) == 0:
            dataSet = self.parsePacket(self.readPacket())
        
        return dataSet
        

    def getFullRotation(self):
        dataSet = []

        dataFragment = self.getDataSet()
        dataSet.extend(dataFragment)

        firstAngle = dataFragment[0][1]
        lastAngle = firstAngle

        #while lastAngle < firstAngle:
        while len(dataSet) < 436:
            dataFragment = self.getDataSet()
            dataSet.extend(dataFragment)
            lastAngle = dataFragment[len(dataFragment)-1][1]
        
        #print(f'First: {firstAngle}\tLast: {lastAngle}')
        return dataSet


    def getMap(self):
    
        points = []
        dataSet = self.getFullRotation()

        for datapoint in dataSet:
            coor = []
            x = datapoint[0] * np.cos(round(datapoint[1]/180*np.pi,2))
            y = datapoint[0] * np.sin(round(datapoint[1]/180*np.pi,2))
            coor.append(round(x,0))
            coor.append(round(y,0))
            coor.append(datapoint[2])
            points.append(coor)
        
        return points
