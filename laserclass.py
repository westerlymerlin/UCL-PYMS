from settings import settings
import requests
import serial


class LaserClass:
    def __init__(self):
        self.port = serial.Serial()
        self.port.port = settings['laser']['port']
        self.port.baudrate = settings['laser']['baud']
        print('Initialising laser on port %s' % self.port.port)
        try:
            self.port.open()
        except serial.serialutil.SerialException:
            print("Laserclass error opening port %s" % self.port.port)

    def off(self):
        message = {"item": 'laser', "command": 'off'}
        try:
            requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
        except requests.RequestException:
            print('Laserclass Automated Valve Controller Laser off Timeout Error')

    def on(self):
        message = {"item": 'laser', "command": 'on'}
        try:
            requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
        except requests.RequestException:
            print('Laserclass Automated Valve Controller Laser on Timeout Error')

    def setpower(self):
        lasermessage = bytearray(b'\xaa\x00\x02\x05\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x33')
        lasermessage[2] = int(settings['laser']['power'] / 10)
        lasermessage[3] = int(settings['laser']['power'] - (int(settings['laser']['power'] / 10) * 10))
        print('Laserclass Setting laser power to %s%%' % settings['laser']['power'])
        try:
            self.port.write(bytes(lasermessage))
        except serial.serialutil.SerialException:
            print("Laserclass error writing to port %s" % self.port.port)


laser = LaserClass()
