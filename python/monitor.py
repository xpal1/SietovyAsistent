#!/bin/bash/python3 python

import tkinter as tk
from tkinter import Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import socket
import threading
import time
import sqlite3
from databaza import Databaza

# trieda pre monitorovanie oneskorenia (odozvy) serverov
class MonitorOneskoreni():
    def __init__(self,master):
        # okno s nazvom
        self.master = master
        self.master.title("Monitorovanie oneskorenia serverov")
        
        self.servery = []
        self.oneskorenia_data = pd.DataFrame(columns=["Server", "Oneskorenie (ms)"])
        self.prebieha_monitorovanie = False
        
        # inicializacia databazy
        self.db = Databaza()
        
        # GUI komponenty
        self.vykresli_gui()
        
    # funkcia, ktora vytvori a vykresli GUI komponenty
    def vykresli_gui(self):
        # vstupne pole pre zadavanie adresy servera
        self.server_vstup = tk.Entry(self.master)
        self.server_vstup.pack(pady=10)
        
        # posuvnik pre volbu casoveho intervalu merania oneskorenia
        # interval od 0.5s do 60s, krok je 0.5s
        self.interval_posuvnik = tk.Scale(self.master, from_=0.5, to=60, resolution=0.5, orient=tk.HORIZONTAL)
        self.interval_posuvnik.set(2) # prednastaveny interval na 2 sekundy
        self.interval_posuvnik.pack()
        
        self.interval_label = tk.Label(self.master, text="casovy interval (s)")
        self.interval_label.pack(pady=5)
        
        # tlacidlo na pridanie servera
        self.tlacidlo_pridaj = tk.Button(self.master, text="Pridat server", command=self.pridaj_server)
        self.tlacidlo_pridaj.pack(pady=5)
        
        # tlacidlo na spustenie monitorovania
        self.tlacidlo_start = tk.Button(self.master, text="Spustit monitorovanie", command=self.spusti_monitorovanie)
        self.tlacidlo_start.pack(pady=5)
        
        # tlacidlo na zastavenie monitorovania
        self.tlacidlo_stop = tk.Button(self.master, text="Zastavit monitorovanie", command=self.zastav_monitorovanie)
        self.tlacidlo_stop.pack(pady=5)
        
        # tlacidlo na zobrazenie oneskoreni vo forme grafu
        self.zobraz_graf_tlacidlo = tk.Button(self.master, text="Zobrazit graf oneskoreni", command=self.vykresli_graf_oneskoreni)
        self.zobraz_graf_tlacidlo.pack(pady=5)
        
        # tlacidlo na zobrazenie historie oneskoreni z databazy
        self.tlacidlo_zobraz_historiu = tk.Button(self.master, text="Zobrazit historiu oneskoreni", command=self.zobraz_obsah_db)
        self.tlacidlo_zobraz_historiu.pack(pady=5)
        
        # textove pole, ktore sluzi ako vystup pre merania oneskoreni
        self.vystupny_text = tk.Text(self.master, height=10, width=50)
        self.vystupny_text.pack(pady=10)
        
    # funkcia na pridanie serveru do zoznamu
    def pridaj_server(self):
        server = self.server_vstup.get()
        if server and server not in self.servery:
            self.servery.append(server)
            self.vystupny_text.insert(tk.END, f"Server: {server}\n")
            self.server_vstup.delete(0, tk.END)
        else:
            messagebox.showwarning("Upozornenie", "Server nebol zadany alebo uz existuje!")
            
    # funkcia na vykonanie pingu na server - zistenie dostupnosti servera
    def ping_server(self, server):
        zaciatocny_cas = time.time()
        try:
            # servery budeme pingovat cez port 53 - DNS
            ip_adresa = socket.gethostbyname(server)
            sock = socket.create_connection((ip_adresa, 53), timeout=2)
            sock.close()
            oneskorenie = (time.time() - zaciatocny_cas) * 1000 # prevod na milisekundy
            
            self.oneskorenia_data.loc[len(self.oneskorenia_data)] = [server, round(oneskorenie, 2)]
            self.vystupny_text.insert(tk.END, f"Ping z {server}: {round(oneskorenie, 2)} ms\n")
            
            # ulozenie do databazy po zisteni oneskorenia servera
            self.db.uloz_do_db(server, round(oneskorenie, 2))
            
        except (socket.timeout, socket.error):
            self.vystupny_text.insert(tk.END, f"Server {server} nie je dostupny\n")
            
    # funkcia, ktora spusti monitorovanie oneskoreni vo vlakne a nadviaze spojenie s databazou
    def spusti_monitorovanie(self):
        self.prebieha_monitorovanie = True
        self.vystupny_text.delete(1.0, tk.END)
        self.vystupny_text.insert(tk.END, "Monitorovanie bolo spustene\n")
        self.monitorovacie_vlakno = threading.Thread(target=self.monitoruj_oneskorenia)
        self.monitorovacie_vlakno.start()
        self.db.otvor_spojenie()
        
    # funkcia, ktora v pripade potreby zastavi monitorovanie a ukonci spojenie s databazou
    def zastav_monitorovanie(self):
        self.prebieha_monitorovanie = False
        self.vystupny_text.insert(tk.END, "Monitorovanie bolo zastavene\n")
        self.db.zatvor_spojenie()
        
    # funkcia, ktora monitoruje oneskorenia v lubovolnom casovom intervale
    def monitoruj_oneskorenia(self):
        interval = self.interval_posuvnik.get() # ziskanie intervalu z posuvnika
        while self.prebieha_monitorovanie:
            for server in self.servery:
                self.ping_server(server)
            time.sleep(interval) # casovy interval v akom sa budu pingovat servery - ziskame z posuvnika
            
    # funkcia, ktora vhodne vykresli do grafu namerane oneskorenia aj s popisom
    def vykresli_graf_oneskoreni(self):
        if not self.oneskorenia_data.empty:
            plt.figure(figsize=(10, 5))
            for server in self.servery:
                server_data = self.oneskorenia_data[self.oneskorenia_data["Server"] == server]
                plt.plot(server_data.index, server_data["Oneskorenie (ms)"], label=server)
                plt.title("Oneskorenia serverov")
                plt.xlabel("cas [s]")
                plt.ylabel("oneskorenie [ms]")
                plt.legend()
                plt.grid()
                plt.show()
        else:
            messagebox.showwarning("Upozornenie", "Zatial ziadne data na zobrazenie!")
            
        self.analyza_oneskorenia()
            
    # funkcia na analyzovanie celkoveho oneskorenia (priemerne, maximalne a minimalne oneskorenie)
    def analyza_oneskorenia(self):
        if not self.oneskorenia_data.empty:
            priemer = self.oneskorenia_data["Oneskorenie (ms)"].mean()
            max_hodnota = self.oneskorenia_data["Oneskorenie (ms)"].max()
            min_hodnota = self.oneskorenia_data["Oneskorenie (ms)"].min()
            
            messagebox.showinfo("Analyza oneskorenia", f"Priemerne oneskorenie: {priemer:.2f} ms\nMax: {max_hodnota:.2f} ms\nMin: {min_hodnota:.2f} ms")
        else:
            messagebox.showwarning("Upozornenie", "Zatial ziadne data na analyzu!")
        
    # funkcia, ktora na zaklade spojenia s databazou pomocou dopytu
    # zisti a vypise z databazy v novom okne jej cely obsah
    # vo vhodnej tabulke s hlavickou
    def zobraz_obsah_db(self):
        # vytvorenie noveho okna
        db_okno = Toplevel(self.master)
        db_okno.title("Obsah databazy")
        
        # vytvorenie skrolovacieho ramca
        ramec = tk.Frame(db_okno)
        ramec.pack(fill=tk.BOTH, expand=True)
        
        # vytvorenie platna a skrolovacieho pruhu
        platno = tk.Canvas(ramec)
        scrollbar = tk.Scrollbar(ramec, orient="vertical", command=platno.yview)
        scrollable_ramec = tk.Frame(platno)
        
        # funkcia na aktualizaciu skrolovacieho ramca
        scrollable_ramec.bind(
            "<Configure>",
            lambda e: platno.configure(scrollregion=platno.bbox("all"))
        )
        
        platno.create_window((0,0), window=scrollable_ramec, anchor="nw")
        
        # umiestnenie skrolovacieho pruhu
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        platno.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # prepojenie scrollbaru s platnom
        platno.configure(yscrollcommand=scrollbar.set)
        
        # pridanie hlavicky tabulky
        hlavicka = ["ID", "Adresa servera", "Oneskorenie (ms)", "Cas"]
        for j, nazov_stlpca in enumerate(hlavicka):
            label = tk.Label(scrollable_ramec, text=nazov_stlpca, font=("Arial", 10, "bold"))
            label.grid(row=0, column=j, padx=5, pady=5)
        
        # nacitanie udajov z databazy
        try:
            self.db.otvor_spojenie()
            self.db.ziskaj_udaje_db()
            rows = self.db.fetchall_udaje_db()
            
            # vytvorenie tabulky na zobrazenie udajov
            for i, row in enumerate(rows):
                for j, hodnota in enumerate(row):
                    label = tk.Label(scrollable_ramec, text=hodnota)
                    label.grid(row=i + 1, column=j, padx=5, pady=5)
                    
        except sqlite3.Error as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa nacitat udaje z databazy: {e}")