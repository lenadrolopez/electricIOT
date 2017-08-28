# electricIOT
IOT Device for display info of current electricity price from **Spain**.

Download/classify rates, and turns on a led on a nodemcu esp8266 depending on the price.

> In Spain, electric rates are published everyday at 20h.

###### This project is a summer exercice for an 8 years child, just for fun.


# How to use

Configure your wifi network and/or your mqtt server in the nodemcu sketch [electric/electric.ino](https://github.com/lenadrolopez/electricIOT/blob/master/electric/electric.ino)

Configure mqtt server in [main.py](https://github.com/lenadrolopez/electricIOT/blob/master/main.py)

main.py must be running on a rpi or linux server.
Every 15 minutes, downloads info from [ree.es](http://www.ree.es/es/) _Red Eléctrica Española_ and classifies prices in 3 categories (expensive, medium and cheap).
Every 5 minutes, checks current time, finds current price and sends an mqtt message with a string:

* red - expensive

* yellow - medium

* green - cheap

## Hardware

* Rasperry Pi/linux server

* nodemcu esp8266

* 5 leds, different colours

* 5 resistors

* breadboard and wires
