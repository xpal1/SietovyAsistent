#!/bin/bash/python3 python

import tkinter as tk
from datetime import datetime
from monitor import MonitorOneskoreni

class Uvod:
    def __init__(self, master):
        self.master = master
        self.master.title("Uvod")
        
        # zobrazenie aktualneho datumu a casu
        self.datum_cas = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.label_uvod = tk.Label(self.master, text=f"Vitajte! \n\nDnes je:\n {self.datum_cas}", font=("Arial", 14))
        self.label_uvod.pack(pady=20)
        
        # tlacidlo pre moznost otvorenia monitorovania oneskorenia
        self.tlacidlo_monitorovanie = tk.Button(self.master, text="Monitorovanie oneskorenia serverov", command=self.spusti_monitorovanie, bg="lightblue")
        self.tlacidlo_monitorovanie.pack(pady=10)
        
        # tlacidlo pre ukoncenie aplikacie
        self.tlacidlo_koniec = tk.Button(self.master, text="Koniec", command=self.master.quit, bg="red", fg="white")
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