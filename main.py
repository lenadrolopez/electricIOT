import threading,urllib,json
from datetime import datetime,timedelta
import paho.mqtt.client as mqtt

def downloadData():
    url ="https://api.esios.ree.es/archives/70/download"
    response=urllib.urlopen(url)
    jsonObject=json.loads(response.read())
    dayPrices={}
    for i in jsonObject['PVPC']:
        dia = {'Dia':i['Dia'],'Hora':i['Hora'],'Precio':i['PMHGEN']}
        dayPrices[i['Hora']]=dia
    #print dayPrices
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
    threading.Timer(900.0,downloadData).start()
    return dayPrices_ordered

def downloadDayInfo():
    threading.Timer(5.0,downloadDayInfo).start()
    print "downloadDayInfo"

def getInterval():
    #print datetime.now().hour#downloadDayInfo()
    one_from_now =datetime.now()+timedelta(hours=1)
    #print one_from_now
    interval=str(datetime.now().hour)+"-"+str(one_from_now.hour)
    return interval


def send_color():
    threading.Timer(60.0,send_color).start()
    interval= getInterval()
    print interval
    print dayPrices_ordered
    data={x['Hora']: x for x in dayPrices_ordered}
    print data[interval]['color']
    client.publish("carlosyLeo/", data[interval]['color'])

def on_conect(client,userData,flags,rc):
    print("connected "+str(rc))
    send_color()

client=mqtt.Client()
client.on_connect =on_conect
client.connect("iot.eclipse.org",1883,60)


dayPrices_ordered = downloadData()


client.loop_forever()
