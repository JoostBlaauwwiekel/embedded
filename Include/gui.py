from tkinter import *
from tkinter import ttk
from threading import *
import threading
from time import sleep


class Gui(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.last_temperature = "Onbekend "
        self.last_light = "Onbekend"
        self.last_wind = "Onbekend"
        self.last_rain = "Onbekend"
        self.last_air = "Onbekend"

        self.light = Label
        self.temperature = Label
        self.wind = Label
        self.rain = Label
        self.air = Label

        self.label1 = Label
        self.label2 = Label
        self.label3 = Label
        self.label4 = Label
        self.label5 = Label

        self.connected_devices = []

    def run(self):
        self.update()
        self.render()

    def set_devices(self, devices):
        self.connected_devices = devices

    def get_last_temperature(self):
        if self.last_temperature == 'Onbekend':
            return ''
        else:
            return str(self.last_temperature) + "°C"

    def get_last_light(self):
        if self.last_light == 'Onbekend':
            return ''
        else:
            return str(self.last_light) + " Lumen"

    def get_last_wind(self):
        if self.last_wind == 'Onbekend':
            return ''
        else:
            return str(self.last_wind) + " Km/H"

    def get_last_rain(self):
        if self.last_rain == 'Onbekend':
            return ''
        else:
            return str(self.last_rain) + " mm/H"

    def get_last_air(self):
        if self.last_air == 'Onbekend':
            return ''
        else:
            return str(self.last_air) + "&"

    def change_light(self):
        if "LIGHT" in self.connected_devices:
            return "Lichtsenor\n\nAangesloten"

    def change_temperature(self):
        if "TEMPERATURE" in self.connected_devices:
            return "Temperatuursensor\n\nAangesloten"

    def change_wind(self):
        if "WIND" in self.connected_devices:
            return "Anemometer\n\nAangesloten"

    def change_rain(self):
        if "RAIN" in self.connected_devices:
            return "Regensensor\n\nAangesloten"

    def change_air(self):
        if "AIR" in self.connected_devices:
            return "Luchtvochtigheidsensor\n\nAangesloten"

    def update(self):
        if "LIGHT" in self.connected_devices:
            self.label1.config(text=self.change_light())
            self.light.config(text=self.get_last_light())

        if "TEMPERATURE" in self.connected_devices:
            self.label2.config(text=self.change_temperature())
            self.temperature.config(text=self.get_last_temperature())

        if "WIND" in self.connected_devices:
            self.label3.config(text=self.change_wind())
            self.wind.config(text=self.get_last_wind())

        if "RAIN" in self.connected_devices:
            self.label4.config(text=self.change_rain())
            self.rain.config(text=self.get_last_rain())

        if "AIR" in self.connected_devices:
            self.label5.config(text=self.change_air())
            self.air.config(text=self.get_last_air())

        threading.Timer(1, self.update).start()

    def render(self):
        root = Tk()
        root.title("Centrale")

        tabControl = ttk.Notebook(root)
        tabControl.grid(row=1, column=0, sticky="NESW")

        tab1 = ttk.Label(tabControl)
        tabControl.add(tab1, text="Dashboard")

        tab2 = ttk.Label(tabControl)
        tabControl.add(tab2, text="Lichtsensor")

        tab3 = ttk.Label(tabControl)
        tabControl.add(tab3, text="Temperatuursensor")

        tab4 = ttk.Label(tabControl)
        tabControl.add(tab4, text="Anemometer")

        tab5 = ttk.Label(tabControl)
        tabControl.add(tab5, text="Regensensor")

        tab6 = ttk.Label(tabControl)
        tabControl.add(tab6, text="Luchtvochtigheid")

        root.columnconfigure(0, weight = 1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(4, weight=1)

        self.label1 = ttk.Label(tab1, text="Lichtsenor\n\nNiet aangesloten", width = 20, anchor = S)
        self.label1.config(text=self.change_light())
        self.label2 = ttk.Label(tab1, text="Temperatuursensor\n\nNiet aangesloten", width = 20, anchor = S)
        self.label2.config(text=self.change_temperature())
        self.label3 = ttk.Label(tab1, text="Anemometer\n\nNiet aangesloten", width = 20, anchor = S)
        self.label3.config(text=self.change_wind())
        self.label4 = ttk.Label(tab1, text="Regensensor\n\nNiet aangesloten", width = 20, anchor = S)
        self.label4.config(text=self.change_rain())
        self.label5 = ttk.Label(tab1, text="Luchtvochtigheid\n\nNiet aangesloten", width = 20, anchor = S)
        self.label5.config(text=self.change_air())

        self.light = ttk.Label(tab1, text = "\n\n" + self.get_last_light(), anchor = S, font = ('arial', 18))
        self.light.config(text=self.get_last_light())
        self.temperature = ttk.Label(tab1, text="\n\n" + self.get_last_temperature(), anchor=S, font=('arial', 18))
        self.temperature.config(text=self.get_last_temperature())
        self.wind = ttk.Label(tab1, text="\n\n" + self.get_last_wind(), anchor=S, font=('arial', 18))
        self.wind.config(text=self.get_last_wind())
        self.rain = ttk.Label(tab1, text="\n\n" + self.get_last_rain(), anchor=S, font=('arial', 18))
        self.rain.config(text=self.get_last_rain())
        self.air = ttk.Label(tab1, text="\n\n" + self.get_last_air(), anchor=S, font=('arial', 18))
        self.air.config(text=self.get_last_air())

        self.label1.grid(row = 1, column = 0, stick = "nsew", ipady = 20)
        self.label2.grid(row = 1, column = 1, stick = "nsew", ipady = 20)
        self.label3.grid(row = 1, column = 2, stick = "nsew", ipady = 20)
        self.label4.grid(row = 1, column = 3, stick = "nsew", ipady = 20)
        self.label5.grid(row = 1, column = 4, stick = "nsew", ipady = 20)

        self.light.grid(row = 0, column = 0, stick = "nsew")
        self.temperature.grid(row=0, column=1, stick="nsew")
        self.wind.grid(row=0, column=2, stick="nsew")
        self.rain.grid(row=0, column=3, stick="nsew")
        self.air.grid(row=0, column=4, stick="nsew")

        # just because its possible
        ttk.Label(tab1, text="\nCopyright © 2019 Zeng Ltd.").grid(row = 2, columnspan = 5)

        root.mainloop()