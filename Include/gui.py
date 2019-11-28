from tkinter import *
from tkinter import ttk
from threading import *
import threading
from tkinter import messagebox

from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys


class Gui(threading.Thread):

    light_sensor_data_x = [0,0]
    light_sensor_data_y = [0,0]

    temp_sensor_data_x = [0,0]
    temp_sensor_data_y = [0,0]

    counter = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.last_temperature = "Onbekend"
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

    def set_light(self, light):
        self.last_light = light

    def set_temperature(self, temperature):
        self.last_temperature = temperature

    def get_last_temperature(self):
        if self.last_temperature == 'Onbekend':
            return ''
        else:
            return "\n" + str(self.last_temperature) + "°C"

    def get_last_light(self):
        if self.last_light == 'Onbekend':
            return ''
        else:
            return "\n" + str(self.last_light) + " Lumen"

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
            return str(self.last_air) + "%"

    def change_light(self):
        for device in self.connected_devices:
            if device[0] == "LIGHT":
                return "Lichtsenor\n\nAangesloten"
            else:
                return "Lichtsenor\n\nNiet aangesloten"

        return "Lichtsenor\n\nNiet aangesloten"

    def change_temperature(self):
        for device in self.connected_devices:
            if device[0] == "TEMPERATURE":
                return "Temperatuursensor\n\nAangesloten"
            else:
                return "Temperatuursensor\n\nNiet aangesloten"

        return "Temperatuursensor\n\nNiet aangesloten"

    def change_wind(self):
        for device in self.connected_devices:
            if device[0] == "WIND":
                return "Anemometer\n\nAangesloten"

        return "Anemometer\n\nNiet aangesloten"

    def change_rain(self):
        for device in self.connected_devices:
            if device[0] == "RAIN":
                return "Regensensor\n\nAangesloten"

        return "Regensensor\n\nNiet aangesloten"

    def change_air(self):
        for device in self.connected_devices:
            if device[0] == "AIR":
                return "Luchtvochtigheidsensor\n\nAangesloten"

        return "Luchtvochtigheidsensor\n\nNiet aangesloten"

    def update(self):
        self.change_gui()
        self.detect_disconnected_devices()

        threading.Timer(1, self.update).start()

    def change_gui(self):
        # change values in the GUI
        try:
            self.label1.config(text=self.change_light())
            self.light.config(text=self.get_last_light())
            self.light_sensor_data_x.append(self.counter)
            self.light_sensor_data_y.append(self.get_last_light())

            self.label2.config(text=self.change_temperature())
            self.temperature.config(text=self.get_last_temperature())
            self.temp_sensor_data_x.append(self.counter)
            self.temp_sensor_data_y.append(self.get_last_temperature())

            self.label3.config(text=self.change_wind())
            self.wind.config(text=self.get_last_wind())

            self.label4.config(text=self.change_rain())
            self.rain.config(text=self.get_last_rain())

            self.label5.config(text=self.change_air())
            self.air.config(text=self.get_last_air())

            self.counter += 1
        except: TypeError

    def detect_disconnected_devices(self):
        if not self.connected_devices:
            self.last_temperature = "Onbekend"
            self.last_light = "Onbekend"
            self.last_air = "Onbekend"
            self.last_rain = "Onbekend"
            self.last_wind = "Onbekend"

        for device in self.connected_devices:
            if self.last_temperature != "Onbekend" and device[0] != 'TEMPERATURE':
                self.last_temperature = "Onbekend"

    # this functions sends a command to a device
    def send_command(self, command, device, value=0):
        if not self.connected_devices:
            messagebox.showinfo("Melding", "Fout: Betreffend apparaat niet aangesloten")
        else:
            for connected_devices in self.connected_devices:
                if connected_devices[0] == device:
                    # when the device is connected
                    if command == 'manual_roll_out':
                        connected_devices[1].manual_roll_out()

                    if command == 'manual_roll_in':
                        connected_devices[1].manual_roll_in()

                    if command == 'reset_to_default':
                        connected_devices[1].reset_to_default()

                    if command == 'disable_autoroll':
                        connected_devices[1].disable_auto_roll()

                    if command == 'enable_autoroll':
                        connected_devices[1].enable_auto_roll()

                    if command == 'min_border':
                        connected_devices[1].change_min_border(value)

                    if command == 'max_border':
                        connected_devices[1].change_max_border(value)
                else:
                    messagebox.showinfo("Melding", "Fout: Betreffend apparaat niet aangesloten")

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

        tab7 = ttk.Label(tabControl)
        tabControl.add(tab7, text="Help")

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(4, weight=1)

        self.label1 = ttk.Label(tab1, text=self.change_light(), width=20, anchor=S, justify=CENTER)
        self.label1.config(text=self.change_light())
        self.label2 = ttk.Label(tab1, text=self.change_temperature(), width=20, anchor=S, justify=CENTER)
        self.label2.config(text=self.change_temperature())
        self.label3 = ttk.Label(tab1, text=self.change_wind(), width=20, anchor=S, justify=CENTER)
        self.label3.config(text=self.change_wind())
        self.label4 = ttk.Label(tab1, text=self.change_rain(), width=20, anchor=S, justify=CENTER)
        self.label4.config(text=self.change_rain())
        self.label5 = ttk.Label(tab1, text=self.change_air(), width=20, anchor=S, justify=CENTER)

        self.label5.config(text=self.change_air())

        self.light = ttk.Label(tab1, text="\n\n" + self.get_last_light(), anchor=S, font=('arial', 18))
        self.light.config(text=self.get_last_light())
        self.temperature = ttk.Label(tab1, text="\n\n" + self.get_last_temperature(), anchor=S, font=('arial', 18))
        self.temperature.config(text=self.get_last_temperature())
        self.wind = ttk.Label(tab1, text="\n\n" + self.get_last_wind(), anchor=S, font=('arial', 18))
        self.wind.config(text=self.get_last_wind())
        self.rain = ttk.Label(tab1, text="\n\n" + self.get_last_rain(), anchor=S, font=('arial', 18))
        self.rain.config(text=self.get_last_rain())
        self.air = ttk.Label(tab1, text="\n\n" + self.get_last_air(), anchor=S, font=('arial', 18))
        self.air.config(text=self.get_last_air())

        self.label1.grid(row=1, column=0, stick="nsew", ipady=20)
        self.label2.grid(row=1, column=1, stick="nsew", ipady=20)
        self.label3.grid(row=1, column=2, stick="nsew", ipady=20)
        self.label4.grid(row=1, column=3, stick="nsew", ipady=20)
        self.label5.grid(row=1, column=4, stick="nsew", ipady=20)

        self.light.grid(row=0, column=0, stick="nsew")
        self.temperature.grid(row=0, column=1, stick="nsew")
        self.wind.grid(row=0, column=2, stick="nsew")
        self.rain.grid(row=0, column=3, stick="nsew")
        self.air.grid(row=0, column=4, stick="nsew")

        # just because its possible
        ttk.Label(tab1, text="\nCopyright © 2019 Zeng Ltd.").grid(row=2, columnspan=5)

        # buttons and text for the light section
        ttk.Label(tab2, text="Instellingen", font=('arial', 18)).grid(row=0, columnspan=2)

        ttk.Label(tab2, text="Handmatig uitrollen:").grid(row=1, column=0, stick="nsew")
        ttk.Button(tab2, text='Handmatig uitrollen', command=lambda: self.send_command('manual_roll_out', 'LIGHT')).grid(row=1, column=1, stick="nsew")

        ttk.Label(tab2, text="Handmatig oprollen:").grid(row=2, column=0, stick="nsew")
        ttk.Button(tab2, text='Handmatig oprollen', command=lambda: self.send_command('manual_roll_in', 'LIGHT')).grid(row=2, column=1, stick="nsew")

        ttk.Label(tab2, text="Automatisch rollen uitschakelen:").grid(row=3, column=0, stick="nsew")
        ttk.Button(tab2, text='Automatisch rollen uitschakelen', command=lambda: self.send_command('disable_autoroll', 'LIGHT')).grid(row=3, column=1, stick="nsew")

        ttk.Label(tab2, text="Automatisch rollen inschakelen:").grid(row=4, column=0, stick="nsew")
        ttk.Button(tab2, text='Automatisch rollen inschakelen', command=lambda: self.send_command('enable_autoroll', 'LIGHT')).grid(row=4, column=1, stick="nsew")

        entry_light_min = ttk.Entry(tab2, width=25)
        ttk.Button(tab2, text='Minimale uitrolwaarde',
                   command=lambda: self.send_command('min_border', 'LIGHT', entry_light_min.get())).grid(row=5, column=1, stick="nsew")

        entry_light_max = ttk.Entry(tab2, width=25)
        ttk.Button(tab2, text='Maximale uitrolwaarde',
                   command=lambda: self.send_command('max_border', 'LIGHT', entry_light_max.get())).grid(row=6, column=1, stick="nsew")

        entry_light_min.grid(row=5, column=0)
        entry_light_max.grid(row=6, column=0)

        ttk.Label(tab2, text="Reset naar standaardwaarden:").grid(row=7, column=0, stick="nsew")
        ttk.Button(tab2, text='Reset naar standaardwaarden', command=lambda: self.send_command('reset_to_default', 'LIGHT')).grid(row=7, column=1, stick="nsew")

        # buttons and text for the temperature section
        ttk.Label(tab3, text="Instellingen", font=('arial', 18)).grid(row=0, columnspan=2)

        ttk.Label(tab3, text="Handmatig uitrollen:").grid(row=1, column=0, stick="nsew")
        ttk.Button(tab3, text='Handmatig uitrollen', command=lambda: self.send_command('manual_roll_out', 'TEMPERATURE')).grid(row=1, column=1, stick="nsew")

        ttk.Label(tab3, text="Handmatig oprollen:").grid(row=2, column=0, stick="nsew")
        ttk.Button(tab3, text='Handmatig oprollen', command=lambda: self.send_command('manual_roll_in', 'TEMPERATURE')).grid(row=2, column=1, stick="nsew")

        ttk.Label(tab3, text="Automatisch rollen uitschakelen:").grid(row=3, column=0, stick="nsew")
        ttk.Button(tab3, text='Automatisch rollen uitschakelen', command=lambda: self.send_command('disable_autoroll', 'TEMPERATURE')).grid(row=3, column=1,
                                                                                                   stick="nsew")

        ttk.Label(tab3, text="Automatisch rollen inschakelen:").grid(row=4, column=0, stick="nsew")
        ttk.Button(tab3, text='Automatisch rollen inschakelen', command=lambda: self.send_command('enable_autoroll', 'TEMPERATURE')).grid(row=4, column=1, stick="nsew")

        entry_temperature_min = ttk.Entry(tab3, width=25)
        ttk.Button(tab3, text='Minimale uitrolwaarde', command=lambda: self.send_command('min_border', 'TEMPERATURE', entry_temperature_min.get())).grid(row=5, column=1, stick="nsew")

        entry_temperature_max = ttk.Entry(tab3, width=25)
        ttk.Button(tab3, text='Maximale uitrolwaarde', command=lambda: self.send_command('max_border', 'TEMPERATURE', entry_temperature_max.get())).grid(row=6, column=1, stick="nsew")

        entry_temperature_min.grid(row=5, column=0)
        entry_temperature_max.grid(row=6, column=0)

        ttk.Label(tab3, text="Reset naar standaardwaarden:").grid(row=7, column=0, stick="nsew")
        ttk.Button(tab3, text='Reset naar standaardwaarden', command=lambda: self.send_command('reset_to_default', 'TEMPERATURE')).grid(row=7, column=1,
                                                                        stick="nsew")
        # help tab with information on how to work the central
        canvas = Canvas(tab7, height=250, width=500)
        scroll_y = ttk.Scrollbar(tab7, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas)

        ttk.Label(frame, text="Help", font=('arial', 18, 'bold')).grid(row=0, columnspan=2)
        ttk.Label(frame, text="Hier vindt u uitleg en informatie over werken met de centrale\n", font=('arial', 10)).grid(row=1, columnspan=2)

        ttk.Label(frame, text="Dashboard:", font=('arial', 9, 'bold')).grid(row=2, column=0, stick="NW")
        ttk.Label(frame, text="Het eerste wat u ziet als u de centrale start is\n"
                             "de dashboard. Hier kunt u zien welke besturings-\n"
                             "eenheden zijn aangesloten op uw rolluik of\n"
                             "zonnescherm. Ook krijgt u de laatste meting van \n"
                             "elke sensor die de centrale ontvangen heeft.\n").grid(row=2, column=1, stick="NW")

        ttk.Label(frame, text="Instellingen:", font=('arial', 9, 'bold')).grid(row=3, column=0, stick="NW")
        ttk.Label(frame, text="Alle besturingseenheden hebben hun eigen tabblad.\n"
                             "Hier staan de knoppen om instellingen te wijzigen\n"
                             "van een gegeven besturingseenheid. \n"
                             "Deze worden verder besproken in de kopjes \n"
                            "hieronder. Verder staan hier de grafieken\n"
                             "van de gemeten sensorwaarden van elke eenheid.\n").grid(row=3, column=1, stick="NW")

        ttk.Label(frame, text="Op- en uitrol grenzen:", font=('arial', 9, 'bold')).grid(row=4, column=0, stick="NW")
        ttk.Label(frame, text="Bij de instellingen staan twee vakken waar\n"
                             "u in kunt typen. Met deze waarden kunt u de\n"
                             "oprol en uitrol grenzen (in centimeters)\n"
                             "aanpassen. De startwaarden van elke eenheid\n"
                             "is minimaal 10cm en maximaal 50cm.\n").grid(row=4, column=1, stick="NW")

        ttk.Label(frame, text="Handmatig rollen:", font=('arial', 9, 'bold')).grid(row=5, column=0, stick="NW")
        ttk.Label(frame, text="Er zijn twee knoppen voor het handmatig rollen.\n"
                             "Één voor oprollen en één voor uitrollen. Nadat\n"
                             "u op een knop drukt zal uw rolluik of zonne-\n"
                             "scherm op- of uitrollen, afhankelijk van welke\n"
                             "wordt ingedrukt. Let hierbij op dat na, het\n"
                             "indrukken van deze knoppen, het automatische\n"
                             "rollen wordt uitgeschakeld en dat u deze hand-\n"
                             "matig weer moet inschakelen\n").grid(row=5, column=1, stick="NW")

        ttk.Label(frame, text="Automatisch rollen:", font=('arial', 9, 'bold')).grid(row=6, column=0, stick="NW")
        ttk.Label(frame, text="Ook hier zijn twee knoppen voor, het in- en\n"
                             "uitschakelen van het automatisch rollen. Als\n"
                             "u het automatisch rollen uitschakeld dan zal\n"
                             "uw rolluik of zonnescherm niet meer rollen bij\n"
                             "de grenswaarden van de sensoren, maar alleen\n"
                             "als u op één van de handmatig rollen knoppen\ndrukt.\n").grid(row=6, column=1, stick="NW")

        ttk.Label(frame, text="Waarden resetten:", font=('arial', 9, 'bold')).grid(row=7, column=0, stick="NW")
        ttk.Label(frame, text="Als u op de 'reset naar standaardwaarden' knop\n"
                             "drukt dan zullen de op- en uitrolgrenzen herstelt\n"
                             "worden naar hun originele waarden (10cm & 50cm).\n"
                             "Ook zal het automatisch rollen weer ingeschakeld\n"
                             "zijn.").grid(row=7, column=1, stick="NW")

        ttk.Label(frame, text="\nCentrale versie 1.1").grid(row=8, columnspan=5)

        ttk.Label(frame, text="\nCopyright © 2019 Zeng Ltd.").grid(row=9, columnspan=5)

        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)

        canvas.grid(row=0, column=0)
        scroll_y.grid(row=0, column=3, sticky='ns')

        # buttons and text for the wind section
        ttk.Label(tab4, text="Instellingen", font=('arial', 18)).grid(row=0, columnspan=2)

        ttk.Label(tab4, text="Handmatig uitrollen:").grid(row=1, column=0, stick="nsew")
        ttk.Button(tab4, text='Handmatig uitrollen',
                   command=lambda: self.send_command('manual_roll_out', 'WIND')).grid(row=1, column=1,
                                                                                             stick="nsew")

        ttk.Label(tab4, text="Handmatig oprollen:").grid(row=2, column=0, stick="nsew")
        ttk.Button(tab4, text='Handmatig oprollen',
                   command=lambda: self.send_command('manual_roll_in', 'WIND')).grid(row=2, column=1,
                                                                                            stick="nsew")

        ttk.Label(tab4, text="Automatisch rollen uitschakelen:").grid(row=3, column=0, stick="nsew")
        ttk.Button(tab4, text='Automatisch rollen uitschakelen',
                   command=lambda: self.send_command('disable_autoroll', 'WIND')).grid(row=3, column=1,
                                                                                              stick="nsew")

        ttk.Label(tab4, text="Automatisch rollen inschakelen:").grid(row=4, column=0, stick="nsew")
        ttk.Button(tab4, text='Automatisch rollen inschakelen',
                   command=lambda: self.send_command('enable_autoroll', 'WIND')).grid(row=4, column=1,
                                                                                             stick="nsew")

        entry_wind_min = ttk.Entry(tab4, width=25)
        ttk.Button(tab4, text='Minimale uitrolwaarde',
                   command=lambda: self.send_command('min_border', 'WIND', entry_wind_min.get())).grid(row=5, column=1, stick="nsew")

        entry_wind_max = ttk.Entry(tab4, width=25)
        ttk.Button(tab4, text='Maximale uitrolwaarde',
                   command=lambda: self.send_command('max_border', 'WIND', entry_wind_max.get())).grid(row=6, column=1, stick="nsew")

        entry_wind_min.grid(row=5, column=0)
        entry_wind_max.grid(row=6, column=0)

        ttk.Label(tab4, text="Reset naar standaardwaarden:").grid(row=7, column=0, stick="nsew")
        ttk.Button(tab4, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'WIND')).grid(row=7, column=1,
                                                                                              stick="nsew")

        # buttons and text for the rain section
        ttk.Label(tab5, text="Instellingen", font=('arial', 18)).grid(row=0, columnspan=2)

        ttk.Label(tab5, text="Handmatig uitrollen:").grid(row=1, column=0, stick="nsew")
        ttk.Button(tab5, text='Handmatig uitrollen',
                   command=lambda: self.send_command('manual_roll_out', 'RAIN')).grid(row=1, column=1,
                                                                                      stick="nsew")

        ttk.Label(tab5, text="Handmatig oprollen:").grid(row=2, column=0, stick="nsew")
        ttk.Button(tab5, text='Handmatig oprollen',
                   command=lambda: self.send_command('manual_roll_in', 'RAIN')).grid(row=2, column=1,
                                                                                     stick="nsew")

        ttk.Label(tab5, text="Automatisch rollen uitschakelen:").grid(row=3, column=0, stick="nsew")
        ttk.Button(tab5, text='Automatisch rollen uitschakelen',
                   command=lambda: self.send_command('disable_autoroll', 'RAIN')).grid(row=3, column=1,
                                                                                       stick="nsew")

        ttk.Label(tab5, text="Automatisch rollen inschakelen:").grid(row=4, column=0, stick="nsew")
        ttk.Button(tab5, text='Automatisch rollen inschakelen',
                   command=lambda: self.send_command('enable_autoroll', 'RAIN')).grid(row=4, column=1,
                                                                                      stick="nsew")

        entry_rain_min = ttk.Entry(tab5, width=25)
        ttk.Button(tab5, text='Minimale uitrolwaarde',
                   command=lambda: self.send_command('min_border', 'RAIN', entry_rain_min.get())).grid(row=5, column=1,
                                                                                                        stick="nsew")

        entry_rain_max = ttk.Entry(tab5, width=25)
        ttk.Button(tab5, text='Maximale uitrolwaarde',
                   command=lambda: self.send_command('max_border', 'RAIN', entry_rain_max.get())).grid(row=6, column=1,
                                                                                                        stick="nsew")

        entry_rain_min.grid(row=5, column=0)
        entry_rain_max.grid(row=6, column=0)

        ttk.Label(tab5, text="Reset naar standaardwaarden:").grid(row=7, column=0, stick="nsew")
        ttk.Button(tab5, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'RAIN')).grid(row=7, column=1,
                                                                                       stick="nsew")

        # buttons and text for the air section
        ttk.Label(tab6, text="Instellingen", font=('arial', 18)).grid(row=0, columnspan=2)

        ttk.Label(tab6, text="Handmatig uitrollen:").grid(row=1, column=0, stick="nsew")
        ttk.Button(tab6, text='Handmatig uitrollen',
                   command=lambda: self.send_command('manual_roll_out', 'AIR')).grid(row=1, column=1,
                                                                                      stick="nsew")

        ttk.Label(tab6, text="Handmatig oprollen:").grid(row=2, column=0, stick="nsew")
        ttk.Button(tab6, text='Handmatig oprollen',
                   command=lambda: self.send_command('manual_roll_in', 'AIR')).grid(row=2, column=1,
                                                                                     stick="nsew")

        ttk.Label(tab6, text="Automatisch rollen uitschakelen:").grid(row=3, column=0, stick="nsew")
        ttk.Button(tab6, text='Automatisch rollen uitschakelen',
                   command=lambda: self.send_command('disable_autoroll', 'AiR')).grid(row=3, column=1,
                                                                                       stick="nsew")

        ttk.Label(tab6, text="Automatisch rollen inschakelen:").grid(row=4, column=0, stick="nsew")
        ttk.Button(tab6, text='Automatisch rollen inschakelen',
                   command=lambda: self.send_command('enable_autoroll', 'AIR')).grid(row=4, column=1,
                                                                                      stick="nsew")

        entry_air_min = ttk.Entry(tab6, width=25)
        ttk.Button(tab6, text='Minimale uitrolwaarde',
                   command=lambda: self.send_command('min_border', 'AIR', entry_air_min.get())).grid(row=5, column=1,
                                                                                                        stick="nsew")

        entry_air_max = ttk.Entry(tab6, width=25)
        ttk.Button(tab6, text='Maximale uitrolwaarde',
                   command=lambda: self.send_command('max_border', 'AIR', entry_air_max.get())).grid(row=6, column=1,
                                                                                                        stick="nsew")

        entry_air_min.grid(row=5, column=0)
        entry_air_max.grid(row=6, column=0)


        ttk.Label(tab6, text="Reset naar standaardwaarden:").grid(row=7, column=0, stick="nsew")
        ttk.Button(tab6, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'AIR')).grid(row=7, column=1,
                                                                                       stick="nsew")

        self.createLightGraph(tab2, 8, 1)
        self.createTempGraph(tab3, 8, 1)

        root.mainloop()

    def createLightGraph(self, tab, row, column):
        figure = plt.figure()
        ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])

        canvas = FigureCanvasTkAgg(figure, tab)
        canvas.get_tk_widget().grid(row=row, column=column)
        canvas.draw()

        self.plotbutton = tk.Button(text="plot", command=lambda: self.plotLightGraph(canvas, ax))
        self.plotbutton.grid(row=0, column=0)

    def createTempGraph(self, tab, row, column):
        figure = plt.figure()
        ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])

        canvas = FigureCanvasTkAgg(figure, tab)
        canvas.get_tk_widget().grid(row=row, column=column)
        canvas.draw()

        self.plotbutton = tk.Button(text="plot", command=lambda: self.plotTempGraph(canvas, ax))
        self.plotbutton.grid(row=0, column=0)

    def plotLightGraph(self, canvas, ax):
        x = self.light_sensor_data_x # tijd om de minuut
        y = self.light_sensor_data_y # waarde van sensor

        ax.plot(x, y)

        canvas.draw()
        ax.clear()

    def plotTempGraph(self, canvas, ax):
        x = self.temp_sensor_data_x # tijd om de minuut
        y = self.temp_sensor_data_y # waarde van sensor

        ax.plot(x, y)

        canvas.draw()
        ax.clear()

