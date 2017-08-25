# electricIOT
IOT Device displays info of current electricity price from **Spain** and switchs on a led in a nodemcu esp8266 

###### This project is a summer exercice for an 8 years child, just for fun.

# How to use

Configure your wifi network and/or your mqtt server in the nodemcu sketch [electric/electric.ino](https://github.com/lenadrolopez/electricIOT/blob/master/electric/electric.ino)

main.py must be running on a rpi or linux server.
Every 15 minutes, downloads info from [ree.es](http://www.ree.es/es/) _Red Eléctrica Española_ and classifies prices in 3 categories (expensive, medium and cheap).
Every 5 minutes, checks current time, finds current price and sends an mqtt message with a string:

> red - expensive

> yellow - medium

> green - cheap


