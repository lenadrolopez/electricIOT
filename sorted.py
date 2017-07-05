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
    dayPrices[i['Hora']] = day

print(dayPrices)

#create a new dictionary with the data sorted by price (cheaper to expensive)
dayPrices2 = sorted(dayPrices.items(), key=lambda x: x[1]['Precio'], reverse=False)
#print info
for key, value in dayPrices2
    print "%s: %s" % (key, value)
