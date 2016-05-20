#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
NFCBeer
Usage:
 nfcbeer.py client <id>
 nfcbeer.py server
 nfcbeer.py [-h | --help]
Options:
 -h --help      Shows help
"""
from docopt import docopt
import RPi.GPIO as GPIO
import time, sys
import signal
from NFCReader import NFCReader
from server_sensor import server_sensor

class FlowControl(object):
    """Controling FlowControl"""
    def __init__(self, nfc=None, server=None):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.count = 0
        self.litres = 0
        self.litres_decimal = 0
        self.service = 0
        self.total = 0
        self.nfc = NFCReader()
        self.server = server
        self.client = client_sensor()
        self.sortidor = 1
        self.cont = 0
        self.uid = None

    def _get_user(self):

        if self.nfc.is_card_present():
            self.uid = self.nfc.read_uid()
        return True



    def update(self, channel):
        tim = time.time()
        delta = tim - self.previousTime
        if delta < 0.5:
            self.count = self.count+1
            self.litres =(self.count/450.0)
            self.service += self.litres
            self.total += self.litres
            print "service =", self.litres
            print "self.service =", self.service
            print "self.total =", self.total
        else if self.cont > 0:
            self.server.enviar(self.uid, self.service, self.sortidor)
        else:
            self.service = 0
            self.user = self._get_user()
            self.server.update_score("1", self.user, self.service)
            self.cont = self.cont + 1

        self.previousTime = tim



class BeerServer(object):
    """Server"""
    def __init__(self):
        super(BeerServer, self).__init__()
        self.scores = {}

    def update_score(self, kegnum, user, beer):
        self.scores[user] = self.scores.get(user, 0.0) + float(beer) #SI no hi ha users, tornam 0
        pass

    def print_leaderboard(self):
        print "*"*40
        for s in self.scores:
            print s, "has drunk", self.scores[s], "L"
        print "*"*40

    def run_loop(self):
        pass
        def run_loop(self):
            while True:
                r = receive()
                self.update_score

class BeerControl(object):
    """COntrol KEG"""
    def __init__(self):
        super(BeerControl, self).__init__()
        self.server = BeerServer()
    def run(self):

        f1= FlowControl(self, self.server)

        FLOW_SENSOR = 16
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(FLOW_SENSOR, GPIO.RISING, callback=f1.update)


        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print '\ncaught keyboard interrupt!, bye'
                GPIO.cleanup()
                sys.exit()


if __name__ == "__main__":

    arguments = docopt(doc=__doc__, version="NFCBEER 1.0")
    print arguments
    c = BeerControl()
    c.run()
