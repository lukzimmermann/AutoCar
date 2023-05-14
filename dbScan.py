import csv
import matplotlib.pyplot as plt

 

x = []
y = []
csvFile = []

with open('scan.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    for line in csvFile:
        print(line)
        x.append(float(line[0]))
        y.append(float(line[1]))        

plt.scatter(x,y)
plt.show()
