#!/usr/bin/env python


import RPi.GPIO as GPIO
import spi
import signal
import time
import MFRC522

class NFCReader(object):

    MIFAREReader = MFRC522.MFRC522()
    def __init__(self):
        self.uid = None


    def is_card_present(self):

        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        print "TagType", TagType
        return True

    def read_uid(self):

        (status,self.uid) = self.MIFAREReader.MFRC522_Anticoll()
        print "uid", self.uid
        return self.uid
