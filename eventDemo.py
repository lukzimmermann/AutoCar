import threading

event = threading.Event()

def myfunction () :
    print ("Waiting for event to trigger... In")
    event.wait ()
    print ("Performing action XYZ now ...")

t1 = threading.Thread(target=myfunction)
t1.start ()

x = input ("Do you want to trigger the event? (y/n) \n")

if x == "y":
    event.set ()
