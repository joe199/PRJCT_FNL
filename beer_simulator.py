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
import time
import client_sensor
# import RPi.GPIO as GPIO
import random

users = [
    "Costa",
    "Borras",
    "Ortiz",
    "Delsams",
    "Godia",
    "Mateu"
]

class FakeNFCReader(object):
    """
    Fake NFC Reader class
    Mimicks an NFC Reader
    """

    uids = [
    "0000000000",
    "1111111111",
    "2222222222",
    "3333333333",
    "4444444444",
    "5555555555",
    "6666666666",
    "7777777777",
    "8888888888",
    "9999999999"
    ]

    def __init__(self):
        self.uid = None

    def is_card_present(self):
        r = random.random()
        if r < 0.8:
            self.uid = self.uids[random.randint(0,9)]
        else:
            self.uid = None
        return self.uid

    def read_uid(self):
        return self.uid


class FlowControl(object):
    """Controlling FlowControl"""
    def __init__(self, nfc=None, server=None):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.service = 0
        self.total = 0
        self.user = -2
        self.sortidor = 1
        self.nfc = nfc
        self.server = server
        self.client=client_sensor.client_sensor()

    def _get_user(self):
        if self.nfc is not None:
            if self.nfc.is_card_present():
                return self.nfc.read_uid()
        return "None"

    def update(self, channel):
        tim = time.time()
        delta = tim - self.previousTime
        if delta < 0.50:
            print ".",
            self.hertz = 1000.0 / delta
            self.flow = self.hertz / 450.0  # Liter/Second
            service = self.flow * (delta / 1000.0)
            self.service  += service
            self.total    += service
        else:
            if self.user != -2:
                print "+"
                print "user", self.user, " drank ", self.service
                self.server.update_score("1", self.user, self.service)
                self.client.enviar(self.user, self.service, self.sortidor)
            # Guardar a usuari self.service
            self.service = 0
            self.user = self._get_user()


        self.previousTime = tim

    def _debug_dump(self):
        print "DBG: TOTAL: ", self.total, "Servei:", self.service


class BeerServer(object):
    """Server"""
    def __init__(self):
        super(BeerServer, self).__init__()
        self.scores = {}

    def update_score(self, kegnum, user, beer):
        self.scores[user] = self.scores.get(user, 0.0) + float(beer)

    def print_leaderboard(self):
        print "*" * 40
        for s in self.scores:
            print s, " has drank ", self.scores[s], " L"
        print "*" * 40

    def run_loop(self):
        while True:
            r = receive()
            self.update_score(r)

class BeerControl(object):
    """Control KEG"""
    def __init__(self):
        super(BeerControl, self).__init__()
        self.server = BeerServer()

    def run(self):
        nf = FakeNFCReader()
        fl = FlowControl(nfc=nf, server=self.server)
        random.seed(1)
        c = 0
        try:
            while True:
                a = random.random()
                if a < 0.3:
                    fl.update(1)

                if a < 0.009:
                    time.sleep(0.550)

                time.sleep(0.002)
                c += 1
                if c > 1000:
                    c = 0
                    fl._debug_dump()
                    self.server.print_leaderboard()
        except Exception as e:
            print e
        finally:
            # GPIO.cleanup()
            pass


if __name__ == "__main__":
    arguments = docopt(doc=__doc__, version="NFCBEER 1.0")
    print arguments
    if arguments["client"]:
        c = BeerControl()
        c.run()
