import serial
import serial.tools.list_ports
import threading
from Include.device import Device
from threading import *
from time import sleep


# noinspection PyBroadException,PyArgumentList
class SerialThread(threading.Thread):

    # initialization of a SerialThread object
    # here is dictionary with as index the COM port and
    # the value the type of device, like 'TEMPERATURE'
    def __init__(self):
        # Thread.__init__(self)
        threading.Thread.__init__(self)
        self.connected_devices = []

    def get_connected_devices(self):
        return self.connected_devices

    # function that runs updates on the ports
    def run(self):
        self.update()

    # function to update port states
    def update(self):
        self.check_connections()
        self.scan_ports()
        threading.Timer(1, self.update).start()

        # function that write a number to the arduino

    def write_data(self, ser, data):  # something like b'\x02'
        ser.write(data)
        sleep(.5)

    def read_data(self, ser):
        line = ser.read()
        # only show bytes with content, not the empty ones
        if line != b'':
            while line is not None:
                # make sure to use int.from_bytes(line, "big")
                # otherwise it will print something like b'\xa4'

                return ord(line)

    # in this function we will determine what kind of
    # device is connected. If the device responds to our
    # handshake, we will open a connection
    # otherwise we will ignore the device
    def handshake(self, serial):
        if self.read_data(serial) == 255:
            self.write_data(serial, b'\xFF')
            device_id = self.read_data(serial)

            if device_id == 150:    # 0x96
                device = 'TEMPERATURE'
            elif device_id == 105:  # 0x69
                device = 'LIGHT'
            elif device_id == 119:  # 0x77
                device = 'WIND'
            elif device_id == 19:   # 0x13
                device = 'RAIN'
            elif device_id == 136:  # 0x88
                device = 'AIR'
            else:
                device = 0

            print('Found', device)
        else:
            device = 0

        return device

    # this function scans ports to see if a device is connected
    def scan_ports(self):
        for port in serial.tools.list_ports.comports():
            try:
                # found a device, now perform the handshake
                ser = serial.Serial(port.device, baudrate=19200, timeout=5)
                device = self.handshake(ser)

                # now we know what type device we have
                # create a device object and save it in the
                # self.connected devices dictionary
                # 0 means an unknown device, look at handshake()
                if device != 0:
                    temp = Device(device, ser)
                    self.connected_devices.append(tuple((device, temp, port.device)))
                    print(device, "Connected")
            except:
                continue

    # this method removes a open connection from the
    # connected_devices list when a device is no longer
    # connected. We will send a message to all the connected
    # devices, when a device is not connected it will raise
    # a SerialException.
    def check_connections(self):
        for connection in self.connected_devices:
            try:
                connection[1].write_data(b'\xFF')

            except serial.SerialException:
                print('Device disconnected on port', connection[2])
                self.connected_devices.remove(connection)