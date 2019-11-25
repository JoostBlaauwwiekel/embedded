import serial as serial
import time
import threading
from threading import *


# noinspection PyMethodMayBeStatic
class Device(threading.Thread):

    def __init__(self, device, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.device = device
        self.last_measure = 0

    # run thread function for Device object
    def run(self):
        time.sleep(1)
        self.last_measure = 0
        self.main()

    # function that write a number to the arduino
    def write_data(self, data):  # something like b'\x02'
        self.ser.write(data)
        time.sleep(.5)

    # function that returns a number from the arduino
    def read_data(self):
        line = self.ser.read()
        # only show bytes with content, not the empty ones
        if line != b'':
            while line is not None:
                # make sure to use int.from_bytes(line, "big")
                # otherwise it will print something like b'\xa4'


                   return ord(line)

    # main function
    def main(self):

        data = self.read_data()
        if data is not None:
            self.last_measure = data

    # getter for last measurement
    def get_last_measure(self):
        return self.last_measure

    # getter for device name
    def get_device(self):
        return self.device

    # function that calls a command from the arduino
    def send_command(self, data):

        # send command value to arduino and wait for a response
        self.write_data(data)
        print("Command send")