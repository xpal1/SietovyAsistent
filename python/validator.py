#!/bin/bash/python3 python

import tkinter as tk
import re

class Validator():
    def __init__(self, master):
        self.master = master
        self.master.title("Validator IPv4 adresy")
        
        # label pre IP adresu
        self.label_ip = tk.Label(self.master, text="Zadajte IP adresu na kontrolu:")
        self.label_ip.pack(pady=(10, 0)) # pridanie paddingu na vrchu
        
        # vstupne pole pre IP adresu
        self.ip_vstup = tk.Entry(self.master, width=20)
        self.ip_vstup.pack(pady=10)
        
        # tlacidlo na overenie IP adresy
        self.tlacidlo_over = tk.Button(self.master, text="Overit IP adresu", command=self.over_ip, bg="#28A745", fg="white")
        self.tlacidlo_over.pack(pady=10)
        
        # vystupny text pre vysledok
        self.vystupny_text = tk.Text(self.master, height=5, width=30)
        self.vystupny_text.pack(pady=10)
        
    # funkcia, ktora sluzi na overenie spravneho tvaru IP adresy, ktoru uzivatel zadal
    def over_ip(self):
        ip_adresa = self.ip_vstup.get()
        if self.validna_ip(ip_adresa):
            self.vystupny_text.delete(1.0, tk.END)
            self.vystupny_text.insert(tk.END, f"IP adresa {ip_adresa} je platna\n")
        else:
            self.vystupny_text.delete(1.0, tk.END)
            self.vystupny_text.insert(tk.END, f"IP adresa {ip_adresa} nie je platna\n")
            
    # funkcia, ktora kontroluje, ci je zadana IP spravneho tvaru podla patternu - vzoru
    def validna_ip(self, ip_ad):
          # regularny vyraz na validaciu IPv4 adresy
          vzor = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
          return re.match(vzor, ip_ad) is not None