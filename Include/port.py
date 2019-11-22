import serial
import serial.tools.list_ports
import threading
from Include.device import Device
from threading import *


# noinspection PyBroadException,PyArgumentList
class SerialThread(threading.Thread):

    # initialization of a SerialThread object
    # here is dictionary with as index the COM port and
    # the value the type of device, like 'TEMPERATURE'
    def __init__(self):
        # Thread.__init__(self)
        threading.Thread.__init__(self)
        self.connected_devices = {}

    # function that runs updates on the ports
    def run(self):
        self.update()

    # function to update port states
    def update(self):
        self.scan_ports()
        threading.Timer(1, self.update).start()

    def read_data(self, ser):
        line = ser.read()
        # only show bytes with content, not the empty ones
        if line != b'':
            while line is not None:
                # make sure to use int.from_bytes(line, "big")
                # otherwise it will print something like b'\xa4'

                return ord(line)

    def handshake(self, serial):
        if self.read_data() == 255:
            self.write_data(b'\xFF')
            device_id = self.read_data(serial)

            if device_id == 150:  # 0x96
                device = 'TEMPERATURE'
            elif device_id == 105:  # 0x69
                device = 'LIGHT'
            else:
                print("ERROR: Something went wrong with the handshake!")

            print('Unit is:', device)

            return device

    # this function scans ports to see if a device is connected
    def scan_ports(self):
        for port in serial.tools.list_ports.comports():
            try:
                # if a device is not connected and found by this function:
                if port not in self.connected_devices:
                    print('Found device on:', port.device)

                    # found a device, now perform the handshake
                    ser = serial.Serial(port, baudrate=19200, timeout=5)
                    device = self.handshake(ser)

                    # now we know what type device we have
                    # create a device object and save it in the
                    # self.connected devices dictionary
                    temp = Device(device, ser)
                    self.connected_devices[port] = temp
                    print(device, "Connected")

                # when a the list has a port with no device left
                # delete the key and value from the dictionary
                # THIS PART HAS NOT BEEN TESTED YET
                for key_port, value_device in self.connected_devices.items():
                    if port != key_port:
                        print(value_device, "disconnected from port", key_port)
                        del self.connected_devices[key_port]
            except:
                continue