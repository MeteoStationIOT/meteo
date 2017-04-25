import os, urlparse
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
from time import sleep
import json
import datetime
from sense_hat import SenseHat

tmax = 35
tmin = tmax - 7

sense = SenseHat()
sense.clear()

mqttc = mqtt.Client()

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://hrrgcrqx:af3wqGskmMfY@m20.cloudmqtt.com:12771')
url = urlparse.urlparse(url_str)

# Connect
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)

# Publish a message
while True:

    now = datetime.datetime.now()
    today8pm = now.replace(hour = 20, minute = 0, second = 0, microsecond = 0)
    today8am = now.replace(hour = 22, minute = 0, second = 0, microsecond = 0)

    if (now < today8pm) or (now < today8am):
        sense.low_light = True
    else:
        sense.low_light = False


    #Temperature
    temp = sense.get_temperature()

    if temp < 20 :
        for x in range(0,4):
            for y in range(0,2):
                sense.set_pixel(x, y, (0, 255, 0))
    elif (temp >= 20 and temp < 30) :
        for x in range(0,4):
            for y in range(0,2):
                sense.set_pixel(x, y, (0, 255, 0))
            for x in range(0,4):
                sense.set_pixel(x,2,(255,255,0))

    elif temp >= 30 :
        for x in range(0,4):
            for y in range(0,2):
                sense.set_pixel(x, y, (0, 255, 0))
        for x in range(0,4):
            sense.set_pixel(x,2,(255,255,0))

        for x in range(0,4):
            sense.set_pixel(x, 3,(255,0,0))    

    obj = { "temperature" : temp }
    mqttc.publish("garden/temperature", json.dumps(obj))
    #pressure
    pressure = sense.get_pressure()
    pressure = round(pressure, 1)
    obj = { "airPressure" : pressure }
    mqttc.publish("garden/airPressure", json.dumps(obj))
    #humidity
    humidity = sense.get_humidity()

    if humidity < 30:
        for x in range(0,4):
            sense.set_pixel(x, 4, (255, 255, 255))
    elif (humidity >= 30 and humidity < 50):
        for x in range(0,4):
            sense.set_pixel(x, 4, (255, 255, 255))

        for x in range(0,4):
            sense.set_pixel(x,5,(174,255,255))


    elif (humidity >= 50 and humidity < 70):
        for x in range(0,4):
            sense.set_pixel(x, 4, (255, 255, 255))

        for x in range(0,4):
            sense.set_pixel(x,5,(174,255,255))

        for x in range(0,4):
            sense.set_pixel(x,6,(68,68,255))

    elif humidity >= 70:
        for x in range(0,4):
            sense.set_pixel(x, 4, (255, 255, 255))

        for x in range(0,4):
            sense.set_pixel(x,5,(174,255,255))

        for x in range(0,4):
            sense.set_pixel(x,6,(68,68,255))

        for x in range(0,4):
            sense.set_pixel(x, 7, (0,0,255))

    obj = { "humidity" : humidity }
    mqttc.publish("garden/humidity", json.dumps(obj))
    #accelerometer
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)

    for a in range(0,8):
        for b in range(5,7):
            sense.set_pixel(b,a,(0,255,0))

    obj = { "axes X" : x,
            "axes Y" : y,
            "axes Z" : z }
    mqttc.publish("garden/accelerometer", json.dumps(obj))

    yellow = (255, 0, 0)
    red = (0, 255, 0)
    none = (0, 0, 0)
    
    if(x != 0 or y != 0 or z!=1):
        for a in range(0,5):
            sense.set_pixel(6,2, red)
            sense.set_pixel(5,3, red)
            sense.set_pixel(5,6, red)
            sense.set_pixel(6,7, red)

            sense.set_pixel(7,0, none)
            sense.set_pixel(7,1, none)
            sense.set_pixel(4,4, none)
            sense.set_pixel(4,5, none)

            sense.set_pixel(4, 0, yellow)
            sense.set_pixel(4, 1, yellow)
            sense.set_pixel(5, 2, yellow)
            sense.set_pixel(6, 3, yellow)
            sense.set_pixel(7, 4, yellow)
            sense.set_pixel(7, 5, yellow)
            sense.set_pixel(6, 6, yellow)
            sense.set_pixel(5, 7, yellow)

            sleep(1)

            sense.set_pixel(5,2, red)
            sense.set_pixel(6,3, red)
            sense.set_pixel(5,7, red)
            sense.set_pixel(6,6, red)

            sense.set_pixel(4,0, none)
            sense.set_pixel(4,1, none)
            sense.set_pixel(7,4, none)
            sense.set_pixel(7,5, none)

            sense.set_pixel(7, 0, yellow)
            sense.set_pixel(7, 1, yellow)
            sense.set_pixel(6, 2, yellow)
            sense.set_pixel(5, 3, yellow)
            sense.set_pixel(4, 4, yellow)
            sense.set_pixel(4, 5, yellow)

            sense.set_pixel(5, 6, yellow)
            sense.set_pixel(6, 7, yellow)

            sleep(1)

    else:
        for b in range(0,8):
            sense.set_pixel(4, b, none)
            sense.set_pixel(7, b, none)
       
    #sleep
    sleep(5)