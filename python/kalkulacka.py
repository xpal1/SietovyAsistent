#!/bin/bash/python3 python

import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

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
        self.label_maska = tk.Label(self.master, text="Vyberte masku podsiete:")
        self.label_maska.pack(pady=(10, 0)) # pridanie paddingu na vrchu
        
        # vstupne pole pre masku podsiete
        self.maska_vyber = ttk.Combobox(self.master, state="readonly", values=[
            "255.255.255.252 /30",
            "255.255.255.248 /29",
            "255.255.255.240 /28",
            "255.255.255.224 /27",
            "255.255.255.192 /26",
            "255.255.255.128 /25",
            "255.255.255.0 /24",
            "255.255.254.0 /23",
            "255.255.252.0 /22",
            "255.255.248.0 /21",
            "255.255.240.0 /20"
        ])
        self.maska_vyber.pack(pady=10)
        
        # tlacidlo pre vypocet
        self.tlacidlo_vypocet = tk.Button(self.master, text="Vypocitat", command=self.vypocitaj, bg="#007FFF", fg="white")
        self.tlacidlo_vypocet.pack(pady=10)
        
        # tlacidlo pre exportovanie vysledku
        self.tlacidlo_export = tk.Button(self.master, text="Exportovat", command=self.exportuj, bg="#28A745", fg="white")
        self.tlacidlo_export.pack(pady=10)
        
        # tlacidlo pre vycistenie vystupu
        self.tlacidlo_vymaz = tk.Button(self.master, text="Vymazat", command=lambda: self.vystupny_text.delete(1.0, tk.END), bg="#EE2C2C", fg="white")
        self.tlacidlo_vymaz.pack(pady=10)
        
        # vystupny text pre vysledok
        self.vystupny_text = tk.Text(self.master, height=10, width=50)
        self.vystupny_text.pack(pady=10)
        
    # funkcia, ktora vypocita a vypise na zaklade zadanej IP adresy a jej masky:
    # adresu siete, 1. a poslednu pouzitelnu adresu, broadcastovu adresu a pocet hostov
    def vypocitaj(self):
        try:
            ip_adresa = self.ip_vstup.get()
            maska_siete = self.maska_vyber.get().split(" /")[1]
            
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
            
    # funkcia na exportovanie vysledku do txt suboru
    def exportuj(self):
        # ziskanie textu z vystupneho pola
        vysledok = self.vystupny_text.get(1.0, tk.END).strip()
        
        # ak na vystupe nic nie je, nic sa nepocitalo
        if not vysledok:
            messagebox.showwarning("Upozornenie", "Nie je zatial co exportovat!")
            return
        
        # otvorenie dialogu na vyber umiestnenia a nazvu suboru
        cesta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textove subory", "*.txt"), ("Vsetky subory", "*.*")], title="Ulozit vysledok ako")
        
        # ak uzivatel nezrusil dialog
        if cesta:
            try:
                with open(cesta, "w") as subor:
                    subor.write(vysledok)
                messagebox.showinfo("OK", "Vysledok bol uspesne exportovany!")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodarilo sa ulozit subor: {str(e)}")