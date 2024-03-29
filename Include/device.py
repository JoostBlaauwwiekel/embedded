import serial as serial
import time
import threading
from threading import *
from tkinter import messagebox


# noinspection PyMethodMayBeStatic
class Device(threading.Thread):

    def __init__(self, device, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.device = device
        self.last_measure = 0
        self.device_min_border = 10
        self.device_max_border = 50
        self.device_auto_roll = True

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

    # change maximum roll out border
    def change_max_border(self, new_max):
        try:
            if(int(new_max) > self.device_min_border):
                self.write_data(b'\x01')
                time.sleep(1)
                self.write_data(bytes([int(new_max)]))
                self.device_max_border = int(new_max)
                print("Maximale uitrol waarde is succesvol aangepast")
                messagebox.showinfo("Melding", "Maximale uitrol waarde is succesvol aangepast")
            else:
                print("Fout: Maximale uitrol waarde mag niet kleiner zijn dan de maximale oprol waarde")
                messagebox.showinfo("Melding", "Fout: Maximale uitrol waarde mag niet kleiner zijn dan de maximale oprol waarde")
        except ValueError:
            messagebox.showinfo("Melding", "Fout: Uitrolwaarde mag alleen een getal zijn")

    # change maximum roll in border
    def change_min_border(self, new_min):
        try:
            if(int(new_min) < self.device_max_border):
                self.write_data(b'\x02')
                time.sleep(1)
                self.write_data(bytes([int(new_min)]))
                self.device_min_border = int(new_min)
                print("Maximale oprol waarde is succesvol aangepast")
                messagebox.showinfo("Melding", "Maximale oprol waarde is succesvol aangepast")
            else:
                print("Fout: Maximale oprol waarde mag niet groter zijn dan de maximale uitrol waarde")
                messagebox.showinfo("Melding", "Fout: Maximale oprol waarde mag niet groter zijn dan de maximale uitrol waarde")
        except ValueError:
            messagebox.showinfo("Melding", "Fout: Uitrolwaarde mag alleen een getal zijn")

    # manually roll out
    def manual_roll_out(self):
        self.write_data(b'\x03')
        print("Het rolluik rolt nu uit (let op: automatisch rollen is uitgeschakeld)")
        messagebox.showinfo("Melding", "Het rolluik rolt nu uit (let op: automatisch rollen is uitgeschakeld)")

    # manually roll in
    def manual_roll_in(self):
        self.write_data(b'\x04')
        print("Het rolluik rolt nu op (let op: automatisch rollen is uitgeschakeld)")
        messagebox.showinfo("Melding", "Het rolluik rolt nu op (let op: automatisch rollen is uitgeschakeld)")

    # reset border and auto roll values back to default
    def reset_to_default(self):
        self.write_data(b'\x05')
        self.device_min_border = 10
        self.device_max_border = 50
        self.device_auto_roll = True
        print("De maximale op- en uitrol waarden zijn gereset naar de standaard waarden")
        messagebox.showinfo("Melding", "De maximale op- en uitrol waarden zijn gereset naar de standaard waarden")

    # disable automatic rolling
    def disable_auto_roll(self):
        self.write_data(b'\x06')
        print("Automatisch rollen is nu uitgeschakeld")
        messagebox.showinfo("Melding", "Automatisch rollen is nu uitgeschakeld")

    # enable automatic rolling
    def enable_auto_roll(self):
        self.write_data(b'\x07')
        print("Automatisch rollen is nu ingeschakeld")
        messagebox.showinfo("Melding", "Automatisch rollen is nu ingeschakeld")

    def current_values(self):
        if(self.device_auto_roll == True):
            auto_roll_string = "Ingeschakeld"
        else:
            auto_roll_string = "Uitgeschakeld"


        print("Minimale uitrolwaarde: {0}cm.\nMaximale uitrolwaarde: {1}cm.\nAutomatisch rollen: {2}.".format(
            self.device_min_border, self.device_max_border, auto_roll_string))
        messagebox.showinfo("Melding", "Minimale uitrolwaarde: {0}cm.\nMaximale uitrolwaarde: {1}cm.\nAutomatisch rollen: {2}.".format(
            self.device_min_border, self.device_max_border, auto_roll_string))