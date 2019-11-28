from tkinter import *
from tkinter import ttk
from threading import *
import threading
from tkinter import messagebox

from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui(threading.Thread):

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

            self.label2.config(text=self.change_temperature())
            self.temperature.config(text=self.get_last_temperature())

            self.label3.config(text=self.change_wind())
            self.wind.config(text=self.get_last_wind())

            self.label4.config(text=self.change_rain())
            self.rain.config(text=self.get_last_rain())

            self.label5.config(text=self.change_air())
            self.air.config(text=self.get_last_air())
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
    def send_command(self, command, device):
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

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(4, weight=1)

        self.label1 = ttk.Label(tab1, text=self.change_light(), width=25, anchor=S, justify=CENTER)
        self.label1.config(text=self.change_light())
        self.label2 = ttk.Label(tab1, text=self.change_temperature(), width=25, anchor=S, justify=CENTER)
        self.label2.config(text=self.change_temperature())
        self.label3 = ttk.Label(tab1, text=self.change_wind(), width=25, anchor=S, justify=CENTER)
        self.label3.config(text=self.change_wind())
        self.label4 = ttk.Label(tab1, text=self.change_rain(), width=25, anchor=S, justify=CENTER)
        self.label4.config(text=self.change_rain())
        self.label5 = ttk.Label(tab1, text=self.change_air(), width=25, anchor=S, justify=CENTER)
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

        ttk.Label(tab2, text="Reset naar standaardwaarden:").grid(row=5, column=0, stick="nsew")
        ttk.Button(tab2, text='Reset naar standaardwaarden',command=lambda: self.send_command('reset_to_default', 'LIGHT')).grid(row=5, column=1, stick="nsew")

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
        ttk.Button(tab3, text='Automatisch rollen inschakelen', command=lambda: self.send_command('enable_autoroll', 'TEMPERATURE')).grid(row=4, column=1,
                                                                                                  stick="nsew")
        ttk.Label(tab3, text="Reset naar standaardwaarden:").grid(row=5, column=0, stick="nsew")
        ttk.Button(tab3, text='Reset naar standaardwaarden', command=lambda: self.send_command('reset_to_default', 'TEMPERATURE')).grid(row=5, column=1,
                                                                        stick="nsew")

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
        ttk.Label(tab4, text="Reset naar standaardwaarden:").grid(row=5, column=0, stick="nsew")
        ttk.Button(tab4, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'WIND')).grid(row=5, column=1,
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
        ttk.Label(tab5, text="Reset naar standaardwaarden:").grid(row=5, column=0, stick="nsew")
        ttk.Button(tab5, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'RAIN')).grid(row=5, column=1,
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
        ttk.Label(tab6, text="Reset naar standaardwaarden:").grid(row=5, column=0, stick="nsew")
        ttk.Button(tab6, text='Reset naar standaardwaarden',
                   command=lambda: self.send_command('reset_to_default', 'AIR')).grid(row=5, column=1,
                                                                                       stick="nsew")

        self.drawGraph(root, 2, 0)
        self.drawGraph(root, 2, 1)
        self.drawGraph(root, 3, 0)
        self.drawGraph(root, 3, 1)

        root.mainloop()

    def drawGraph(self, root, row, column):
        figure = Figure(figsize=(7, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)

        plot.plot(0.5, 0.3, color="red", marker="o", linestyle="")

        x = [0.1, 0.2, 0.3]
        y = [-0.1, -0.2, -0.3]
        plot.plot(x, y, color="blue", marker="x", linestyle="")

        canvas = FigureCanvasTkAgg(figure, root)
        canvas.get_tk_widget().grid(row=row, column=column)