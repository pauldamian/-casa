import Adafruit_DHT
import gpio_mapping as gm

pin = gm.DHT_PIN    # GPIO Pin

def instant_th(steps=3):
    temps = 0.0
    hums = 0.0
    for i in range(steps):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        if humidity is not None and temperature is not None:
            temps += temperature
            hums += humidity
        else:
            steps += 1
    return temps / steps, hums / steps
