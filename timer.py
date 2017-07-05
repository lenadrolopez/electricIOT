#Import Library
import threading

#define a method that would be called every 5 seconds
def printit():
    #create the timer with parameters (frequency, method to call)
    #.start() call method to start the timer
    threading.Timer(5.0, printit).start()

    #sample code for check timer is working
    print "Hello, World!"
#initiate the timer
printit()
