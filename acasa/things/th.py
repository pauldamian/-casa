import Adafruit_DHT as dht
from thing import Thing
from time import sleep


class DHT(Thing):
    def __init__(self, name, use, location=None, pin=0):
        Thing.__init__(self, name, use, location, pin)

    def instant_th(self, steps=3):
        # Returns the averaged temperature, humidity
        # Also returns 0 for pressure, in order to keep similar format as sensortag
        temps = 0.0
        hums = 0.0
        for i in range(steps):
            humidity, temperature = dht.read_retry(dht.DHT11, self.pin)
            if humidity is not None and temperature is not None:
                temps += temperature
                hums += humidity
            else:
                steps += 1
            sleep(1)
        return temps / steps, hums / steps, 0
