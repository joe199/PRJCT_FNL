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
