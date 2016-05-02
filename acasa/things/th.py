import Adafruit_DHT

pin = 23    #GPIO Pin


def instant_th():
    steps = 10
    temps = 0.0
    hums = 0.0
    for i in range(steps):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        if humidity is not None and temperature is not None:
            temps += temperature
            hums+=humidity
        else:
            steps+=1
    return temps/steps, hums/steps

##t, h = instant_th()
##print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t, h))

