
class Thing():
    def __init__(self, name, use, pin=0, location=None, type='sensor', save_recordings=False):
        self.location = location
        self.pin = pin
        self.name = name
        self.use = use
        self.type = type
        self.save_recordings = save_recordings
