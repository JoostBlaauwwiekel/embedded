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
        threading.Timer(5, self.update).start()

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

    def handshake(self, serial):
        if self.read_data(serial) == 255:
            self.write_data(serial, b'\xFF')
            device_id = self.read_data(serial)

            if device_id == 150:  # 0x96
                device = 'TEMPERATURE'
            elif device_id == 105:  # 0x69
                device = 'LIGHT'
            else:
                print("ERROR: Something went wrong with the handshake!")

            #print('Unit is:', device)

            return device

    # this function scans ports to see if a device is connected
    def scan_ports(self):
        for port in serial.tools.list_ports.comports():
            try:
                # if a device is not connected and found by this function:
                if "COM3" == port.device:
                    #print('Found device on:', port.device)

                    # found a device, now perform the handshake
                    ser = serial.Serial(port.device, baudrate=19200, timeout=5)
                    device = self.handshake(ser)

                    # now we know what type device we have
                    # create a device object and save it in the
                    # self.connected devices dictionary
                    temp = Device(device, ser)
                    self.connected_devices.append(tuple((device, temp, port.device)))
                    #print(device, "Connected")

                # when a the list has a port with no device left
                # delete the key and value from the dictionary
                # THIS PART HAS NOT BEEN TESTED YET
            except:
                continue

    def check_connections(self):
        for connection in self.connected_devices:
            try:
                connection[1].write_data(b'\xFF')

            except serial.SerialException:
                print('Device disconnected on port', connection[2])
                self.connected_devices.remove(connection)