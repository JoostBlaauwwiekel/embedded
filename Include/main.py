import threading
from threading import *
from time import sleep
from Include.gui import Gui
from Include.port import SerialThread


class Main(Thread):

    def __init__(self):
        # Thread.__init__(self)
        Thread.__init__(self)

        self.gui = Gui()
        self.gui.start()

        self.serial = SerialThread()
        self.serial.start()

        while(True):
            connected_devices = self.serial.get_connected_devices()
            sleep(5)

            try:
                for device in connected_devices:
                    if device[0] == 'TEMPERATURE':
                        last_temperature = device[1].read_data()

                    if device[0] == 'LIGHT':
                        last_light = device[1].read_data()
            except:
                continue


main = Main()
