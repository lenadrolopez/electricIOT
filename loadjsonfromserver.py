#import libraries
import urllib, json

#define url from where we will downloa data
url         = "https://api.esios.ree.es/archives/70/download"
#load data and store it in a var
response    = urllib.urlopen(url)
#convert response in a JSON
jsonObject  = json.loads(response.read())
print jsonObject

#iterate through json a print data
for i in jsonObject['PVPC']:
    print i['Dia']
    print i['Hora']
    print i['PMHGEN']
