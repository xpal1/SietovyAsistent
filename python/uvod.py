#!/bin/bash/python3 python

import tkinter as tk
from datetime import datetime
from monitor import MonitorOneskoreni
from validator import Validator
from kalkulacka import IPKalkulacka

class Uvod:
    def __init__(self, master):
        self.master = master
        self.master.title("Uvod")
        
        # zobrazenie aktualneho datumu a casu
        self.datum_cas = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.label_uvod = tk.Label(self.master, text=f"Vitajte! \n\nDnes je:\n {self.datum_cas}", font=("Arial", 14))
        self.label_uvod.pack(pady=20)
        
        # tlacidlo pre moznost otvorenia monitorovania oneskorenia
        self.tlacidlo_monitorovanie = tk.Button(self.master, text="Monitorovanie oneskorenia serverov", command=self.spusti_monitorovanie, bg="dodgerblue1")
        self.tlacidlo_monitorovanie.pack(pady=10)
        
        # tlacidlo pre moznost otvorenia validacie IP adresy
        self.tlacidlo_validacia_ip = tk.Button(self.master, text="Validacia IPv4 adresy", command=self.spusti_validator, bg="deepskyblue2")
        self.tlacidlo_validacia_ip.pack(pady=10)
        
        # tlacidlo pre moznost otvorenia IPv4 kalkulacky
        self.tlacidlo_ip_kalkulacka = tk.Button(self.master, text="IPv4 kalkulacka", command=self.spusti_kalkulacku, bg="#00C957")
        self.tlacidlo_ip_kalkulacka.pack(pady=10)
        
        # tlacidlo pre ukoncenie aplikacie
        self.tlacidlo_koniec = tk.Button(self.master, text="Koniec", command=self.master.quit, bg="#CD0000", fg="white")
        self.tlacidlo_koniec.pack(pady=10)
        
    # funkcia, ktora zatvori uvodne okno a otvori okno pre monitorovanie oneskoreni
    def spusti_monitorovanie(self):
        self.master.destroy()
        self.otvor_monitorovanie()
        
    # funkcia, ktora otvori monitorovacie okno
    def otvor_monitorovanie(self):
        root = tk.Tk()
        MonitorOneskoreni(root)
        root.mainloop()
        
    # funkcia, ktora zatvori uvodne okno a otvori okno pre validovanie IP adresy
    def spusti_validator(self):
        self.master.destroy()
        self.otvor_validovanie()
        
    # funkcia, ktora otvori validovacie okno
    def otvor_validovanie(self):
        root = tk.Tk()
        Validator(root)
        root.mainloop()
        
    # funkcia, ktora zatvori uvodne okno a otvori okno pre kalkulacku IP adries
    def spusti_kalkulacku(self):
        self.master.destroy()
        self.otvor_kalkulacku()
        
    # funkcia, ktora otvori okno s kalkulackou
    def otvor_kalkulacku(self):
        root = tk.Tk()
        IPKalkulacka(root)
        root.mainloop()