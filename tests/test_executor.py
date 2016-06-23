'''
Created on Jun 23, 2016

@author: damianpa
'''
import unittest
import mock
import minimock
import sys
sys.path.insert(0, '../acasa/')
import executor
from internet import meteo


class TestExecutor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        minimock.restore()

    def test_lights(self):
        minimock.mock("executor.dim.set_dim_level", returns=None)
        for i in ['0', '100', 'on', 'off']:
            self.assertEqual("Lights turned %s" % str(i), executor.lights(i))


#     @mock.patch('executor.meteo')
    def test_show_weather(self):
#         vreme = {"coord":{"lon":23.6,"lat":46.77},
#                  "weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],
#                  "base":"cmc stations",
#                  "main":{"temp":304.76,"pressure":1022,"humidity":52,"temp_min":304.26,"temp_max":305.37},
#                  "wind":{"speed":1.03,"deg":160},"rain":{"3h":0.0025},
#                  "clouds":{"all":20},"dt":1466701726,
#                  "sys":{"type":3,"id":40394,"message":0.0046,"country":"RO","sunrise":1466649139,"sunset":1466706224},
#                  "id":681290,"name":"Cluj-Napoca","cod":200}
        
#         mock_meteo.get_current_weather.return_value.startswith("The current weather condition")
#         executor.show('weather city')
#         executor = mock.Mock()
#         ex
        pass

    def test_forecast(self):
        hours = range(12)
        wobj = mock.Mock()
        wobj.general = "ceva general"
        wobj.temp = "cald"
        wobj.x.x.x.x.x.x.x.x.x = ""
#         executor.meteo.get_current_weather = lambda: wobj
        minimock.mock("executor.meteo.get_current_weather", returns=wobj)
#        executor.meteo.get_forecast = lambda x: wobj
        minimock.mock("executor.meteo.get_forecast", returns=wobj)
        returns = []
        for h in hours:
            returns.append( executor._forecast(h))
        self.assertIn("The weather in 3 hours will be ceva general with a temperature of cald*. ",
                      returns)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()