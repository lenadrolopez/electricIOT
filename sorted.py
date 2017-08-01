#import libraries
import urllib, json
#define url from where we will downloa data
url         = "https://api.esios.ree.es/archives/70/download"
#load data and store it in a var
response    = urllib.urlopen(url)
#convert response in a JSON
jsonObject  = json.loads(response.read())
#define a dictionary for store only needed values
dayPrices   = {};
#iterate through json
for i in jsonObject['PVPC']:
    #create a dictionary for each entry, storing Precio, Hora and Dia
    day     = {'Dia':i['Dia'],"Hora":i['Hora'],"Precio":i['PMHGEN']}
    #add created dictionary to the dayPrices dictionary
    dayPrices[str(i['Hora'])] = day

#print(dayPrices)

#find current hour interval
from datetime import datetime, timedelta
#current hour
print datetime.now().hour
#current hour +1 hour
one_hour_from_now = datetime.now() + timedelta(hours=1)
print one_hour_from_now.hour
#create string with interval for match data format
interval = str(datetime.now().hour)+"-"+str(one_hour_from_now.hour)
print interval

#create a new dictionary with the data sorted by price (cheaper to expensive)
dayPrices2 = sorted(dayPrices.items(), key=lambda x: x[1]['Precio'], reverse=False)
#print info
i = 0
for key, value in dayPrices2:
    #assign color to items
    if i<=8:
        value['color'] = "green"
    elif i>8 and i<=16:
        value['color'] = "yellow"
    else:
        value['color'] = "red"
    print value
    dayPrices2[i] = value
    i += 1
    if key==interval:
        actual = value
        print "%s: %s" % (key, value)
print dayPrices2
print value
#parse list for access as dict
data = {x['Hora']: x for x in dayPrices2}
print data[interval]


import threading
#define a method that would be called every 5 seconds
def printit():
    #create the timer with parameters (frequency, method to call)
    #.start() call method to start the timer
    threading.Timer(5.0, printit).start()

    #sample code for check timer is working
    client.publish("carlosYLeo/electricityPrice","OFF")

#install mqtt
'''
Installation

Install PIP:
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install python-pip


The latest stable version is available in the Python Package Index (PyPi) and can be installed using

pip install paho-mqtt
'''


import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("carlosYLeo/electricityPrice")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client            = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#initiate the timer
printit()
client.loop_forever()
