from flask import Flask
from flask import request
from time import sleep
import datetime
from sense_hat import SenseHat

X = [255, 0, 0] #rouge
O = [0, 0, 0] #blanc
Z = [255,255,0] #jaune
W = [0,0,255] #bleu

now = datetime.datetime.now()
today8pm = now.replace(hour = 20, minute = 0, second = 0, microsecond = 0)
today8am = now.replace(hour = 22, minute = 0, second = 0, microsecond = 0)

if (now < today8pm) or (now > today8am):
        sense.low_light = True
else:
        sense.low_light = False

sense = SenseHat()
sense.set_rotation(180)
sense.clear(0,0,0)
temperature_value = 18

alert = [
O,O,O,X,X,O,O,O,
O,O,X,Z,Z,X,O,O,
O,O,X,Z,Z,X,O,O,
O,X,O,Z,Z,O,X,O,
O,X,O,O,O,O,X,O,
X,O,O,Z,Z,O,O,X,
X,O,O,Z,Z,O,O,X,
O,X,X,X,X,X,X,O
]

onde = [
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
X,O,O,O,X,O,O,O,
O,X,O,X,O,X,O,X,
O,O,X,O,O,O,X,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O
]


A = (0,0,255)

goutte = [
O,O,O,A,A,O,O,O,
O,O,O,A,A,O,O,O,
O,O,A,A,A,A,O,O,
O,A,A,A,A,A,A,O,
O,A,A,A,A,A,A,O,
O,A,A,A,A,A,A,O,
O,A,A,A,A,A,A,O,
O,O,A,A,A,A,O,O

]

app = Flask(__name__)

@app.route("/temperature", methods=['GET'])
def temperature():
        print(request.args.get('type'))
        #print(request.data)
        red = (255, 0, 0)
        yellow = (255, 255, 0)

        if request.args.get('type') == 'alert':
                sense.set_pixels(alert)
                sleep(1)
                sense.clear(0,0,0)
                sleep(1)
                sense.show_message(request.args.get('data'), text_colour = red)
        else :
                sense.show_message(request.args.get('data'), text_colour = yellow)


        if temperature_value > 30:
                red = (255, 0, 0)
        elif temperature_value > 20 and temperature_value <= 30:
                red = (0, 255, 0)
        else:
                red = (0, 0, 255)

        return "OK"

@app.route("/accelerometre", methods=['GET'])
def accelerometer():
        if request.args.get('type') == 'alert' :
                sense.set_pixels(onde)
                sleep(5)
                sense.clear(0,0,0)
                sleep(1)
                return "TREMBLEMENT DE TERRE, COUVREZ VOUS !"

@app.route("/humidite", methods=['GET'])
def humidity():
        if request.args.get('type') == 'alert' :
                sense.set_pixels(goutte)
                sleep(5)
                sense.clear(0,0,0)
                sleep(1)
                return "Humidite elevee, risque de pluie"

if __name__ == "__main__":
        app.debug = True
        app.run(host='0.0.0.0')