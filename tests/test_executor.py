'''
Created on Jun 23, 2016

@author: damianpa
'''
import unittest
import minimock
import sys
sys.path.insert(0, '../acasa/')
import executor


class TestExecutor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        minimock.restore()

    def testLights(self):
        minimock.mock("executor.dim.set_dim_level", returns=None)
        for i in ['12', '50']:
            self.assertEqual("Lights turned %s" % str(i), executor.lights(i))
        for i in ['lala', '234$', '12 12', '-12', '0', '50.5', 'off']:
            self.assertEqual("Lights turned 0", executor.lights(i))
        for i in ['100', '34674', '1111111111', 'on']:
            self.assertEqual("Lights turned 100", executor.lights(i))

    def testForecast(self):
        hours = range(12)
        wobj = minimock.Mock('obj')
        wobj.general = "sunny"
        wobj.temp = "27"
        minimock.mock("executor.meteo.get_current_weather", returns=wobj)
        minimock.mock("executor.meteo.get_forecast", returns=wobj)
        returns = []
        for h in hours:
            returns.append(executor.forecast(h))
        self.assertIn("The weather in 3 hours will be sunny with a temperature of 27*. ",
                      returns)

    def testShowWeather(self):
#         vreme = {"coord":{"lon":23.6,"lat":46.77},
#                  "weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],
#                  "base":"cmc stations",
#                  "main":{"temp":304.76,"pressure":1022,"humidity":52,"temp_min":304.26,"temp_max":305.37},
#                  "wind":{"speed":1.03,"deg":160},"rain":{"3h":0.0025},
#                  "clouds":{"all":20},"dt":1466701726,
#                  "sys":{"type":3,"id":40394,"message":0.0046,"country":"RO","sunrise":1466649139,"sunset":1466706224},
#                  "id":681290,"name":"Cluj-Napoca","cod":200}
        minimock.mock("executor.forecast", returns="The weather in 3 hours will be ...")
        self.assertEqual("The weather in 3 hours will be ...", executor.show("weather city"))
        self.assertEqual("The weather in 3 hours will be ...", executor.show("weather"))
        for (t, h) in [(12, 34), (-20, -7), (40, 120), (12.121212, 45.67543)]:
            minimock.mock("executor.db.get_reading", returns=(t, h))
            r = "Outside temperature is %.1f*C, while humidity reaches %.1f%%" % (t, h)
            self.assertEqual(r, executor.show("weather outside"))
            r = "No sensor in that location!\n" + r
            self.assertEqual(r, executor.show("weather out"))
            self.assertEqual(r, executor.show("weather 12"))
            self.assertEqual(r, executor.show("weather #$"))
        for r in [None, "No sensor readings recorded!", "blablacar", (1, 2, 3)]:
            minimock.mock("executor.db.get_reading", returns=r)
            self.assertEqual(executor.show("weather outside"), "No records available")

    def testShowCommands(self):
        mockom = minimock.Mock('obj')
        mockom.order = 'show'
        mockom.schedule = '2016-12-12 12:12:12'
        mockom.args = 'something'
        lmock = [mockom]
        for m in [lmock, 2 * lmock, 5 * lmock]:
            minimock.mock("executor.db.read_next_commands", returns=m)
            msg = 'The following commands will be executed:'
            for i in range(len(m)):
                msg = msg + '\nshow something on 2016-12-12 12:12:12'
            self.assertEqual(executor.show('commands'), msg)
            self.assertEqual(executor.show('commands 3'), msg)
            self.assertEqual(executor.show('commands 5'), msg)
        for p in ['commands today', 'commands commands', 'commands 100%%']:
            msg = 'Invalid parameter for commands. Will return the next %s commands.\n' % executor.defaults['commands']
            msg += 'The following commands will be executed:'
            for i in range(executor.defaults['commands']):
                msg = msg + '\nshow something on 2016-12-12 12:12:12'
            minimock.mock("executor.db.read_next_commands", returns=3 * lmock)
            self.assertEqual(executor.show(p), msg)

    def testShowTemp(self):
        for r in ["No sensor readings recorded!", "blablacar", (1, 2, 3)]:
            minimock.mock("executor.db.get_reading", returns=r)
            self.assertEqual(executor.show("temp"), "No records available")
        for (t, h) in [(12, 34), (-20, -7), (40, 120), (12.121212, 45.67543)]:
            minimock.mock("executor.db.get_reading", returns=(t, h))
            r = 'Temperature is ' + str("%.1f" % t) + '*C'
            self.assertEqual(r, executor.show("temp inside"))
            self.assertEqual(r, executor.show("temp"))
            r = "No sensor in that location!"
            self.assertEqual(r, executor.show("temp in"))
            self.assertEqual(r, executor.show("temp 12"))
            self.assertEqual(r, executor.show("temp #$"))

    def testShowHum(self):
        for r in ["No sensor readings recorded!", "blablacar", (1, 2, 3)]:
            minimock.mock("executor.db.get_reading", returns=r)
            self.assertEqual(executor.show("hum"), "No records available")
        for (t, h) in [(12, 34), (-20, -7), (40, 120), (12.121212, 45.67543)]:
            minimock.mock("executor.db.get_reading", returns=(t, h))
            r = 'Humidity is ' + str("%.1f" % h) + '%'
            self.assertEqual(r, executor.show("hum inside"))
            self.assertEqual(r, executor.show("hum"))
            r = "No sensor in that location!"
            self.assertEqual(r, executor.show("hum in"))
            self.assertEqual(r, executor.show("hum 12"))
            self.assertEqual(r, executor.show("hum #$"))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
