#!/bin/bash/python3 python

import ipaddress
import tkinter as tk

class IPKalkulacka:
    def __init__(self, master):
        self.master = master
        self.master.title("IPv4 kalkulacka")
        
        # label pre IP adresu
        self.label_ip = tk.Label(self.master, text="Zadajte IP adresu:")
        self.label_ip.pack(pady=(10, 0)) # pridanie paddingu na vrchu
        
        # vstupne pole pre IP adresu
        self.ip_vstup = tk.Entry(self.master, width=20)
        self.ip_vstup.pack(pady=5)
        
        # label pre masku podsiete
        self.label_maska = tk.Label(self.master, text="Zadajte masku podsiete:")
        self.label_maska.pack(pady=(10, 0)) # pridanie paddingu na vrchu
        
        # vstupne pole pre masku podsiete
        self.maska_vstup = tk.Entry(self.master, width=20)
        self.maska_vstup.pack(pady=10)
        
        # tlacidlo pre vypocet
        self.tlacidlo_vypocet = tk.Button(self.master, text="Vypocitat", command=self.vypocitaj, bg="#007FFF", fg="white")
        self.tlacidlo_vypocet.pack(pady=10)
        
        # vystupny text pre vysledok
        self.vystupny_text = tk.Text(self.master, height=10, width=50)
        self.vystupny_text.pack(pady=10)
        
    # funkcia, ktora vypocita a vypise na zaklade zadanej IP adresy a jej masky:
    # adresu siete, 1. a poslednu pouzitelnu adresu, broadcastovu adresu a pocet hostov
    def vypocitaj(self):
        try:
            ip_adresa = self.ip_vstup.get()
            maska_siete = self.maska_vstup.get()
            
            # vytvorenie objektu IPv4Network za pomoci kniznice ipaddress
            network = ipaddress.IPv4Network(f"{ip_adresa}/{maska_siete}", strict=False)
            
            # ziskanie potrebnych informacii
            adresa_siete = network.network_address
            adresa_broadcast = network.broadcast_address
            pocet_hostov = network.num_addresses - 2 # adresu siete a broadcastu neratame
            
            # prva a posledna pouzitelna IP adresa
            prva_pouzitelna_ip = adresa_siete + 1
            posledna_pouzitelna_ip = adresa_broadcast -1
            
            # vypis vysledkov na vystup
            self.vystupny_text.delete(1.0, tk.END)
            self.vystupny_text.insert(tk.END, f"Adresa siete: {adresa_siete}\n")
            self.vystupny_text.insert(tk.END, f"1. pouzitelna IP: {prva_pouzitelna_ip}\n")
            self.vystupny_text.insert(tk.END, f"Posledna pouzitelna IP: {posledna_pouzitelna_ip}\n")
            self.vystupny_text.insert(tk.END, f"Broadcast adresa: {adresa_broadcast}\n")
            self.vystupny_text.insert(tk.END, f"Pocet hostov: {pocet_hostov}\n")
            
        except ValueError as e:
            self.vystupny_text.delete(1.0, tk.END)
            self.vystupny_text.insert(tk.END, f"Chyba: {str(e)}\n")