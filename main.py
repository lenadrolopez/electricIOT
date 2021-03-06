### Authors: Leandro & Carlos
### Date:  july/august 2017
### Description: summer code learning project for Carlos (8 years old)
### Downloads and classifies electric rates from Spain

import threading,urllib,json
from datetime import datetime,timedelta
import paho.mqtt.client as mqtt

#download data for ree.es
def downloadData():
    url ="https://api.esios.ree.es/archives/70/download"
    response=urllib.urlopen(url)
    jsonObject=json.loads(response.read())
    dayPrices={}
    #extract only the info that we want
    for i in jsonObject['PVPC']:
        dia = {'Dia':i['Dia'],'Hora':i['Hora'],'Precio':i['PMHGEN']}
        dayPrices[i['Hora']]=dia
    #print dayPrices
    #sort by price and assign a colour
    i=0
    dayPrices_ordered = sorted(dayPrices.items(), key=lambda x:x[1]['Precio'],reverse=False)
    for key,value in dayPrices_ordered:
    #    print "%s: %s" % (key,value)
        if i<=8:
            value['color']="green"
        elif i>8 and i<=16:
            value['color']="yellow"
        else:
            value['color']="red"
        dayPrices_ordered[i]=value
        i+=1
    #start timer for repeat download every N minutes. ree.es publish data every day at 20h CEST.
    #if we download data only once per day, we need to handle errors. Doing it every 15 minutes we avoid network errors at least
    threading.Timer(900.0,downloadData).start()
    return dayPrices_ordered

#generate interval in the same format than ree.es data
def getInterval():
    one_from_now =datetime.now()+timedelta(hours=1)
    #print one_from_now
    interval=str(datetime.now().hour)+"-"+str(one_from_now.hour)
    return interval

#send mqtt message with the colour
def send_color():
    #send message every minute. ree.es publishes info for each hour. Sending message every minute, we reduce network errors
    threading.Timer(60.0,send_color).start()
    interval= getInterval()
    print interval
    print dayPrices_ordered
    data={x['Hora']: x for x in dayPrices_ordered}
    print data[interval]['color']
    client.publish("carlosyLeo/", data[interval]['color'])

#mqtt calback
def on_conect(client,userData,flags,rc):
    print("connected "+str(rc))
    send_color()

client=mqtt.Client()
client.on_connect =on_conect
client.connect("iot.eclipse.org",1883,60)
#init download
dayPrices_ordered = downloadData()

client.loop_forever()
