#!/bin/bash/python3 python

from curses import window
from pydoc import text
import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter import font
import pandas as pd
import matplotlib.pyplot as plt
import socket
import threading
import time
import sqlite3

# trieda pre monitorovanie oneskorenia (odozvy) serverov
class MonitorOneskoreni():
    def __init__(self,master): 
        self.master = master
        self.master.title("Monitorovanie oneskorenia serverov")
        
        self.servery = []
        self.oneskorenia_data = pd.DataFrame(columns=["Server", "Oneskorenie (ms)"])
        self.prebieha_monitorovanie = False
        
        # inicializacia databazy
        self.init_db()
        
        self.server_vstup = tk.Entry(master)
        self.server_vstup.pack(pady=10)
        
        # posuvnik pre volbu casoveho intervalu merania oneskorenia
        # interval od 0.5s do 60s, krok je 0.5s
        self.interval_posuvnik = tk.Scale(master, from_=0.5, to=60, resolution=0.5, orient=tk.HORIZONTAL)
        self.interval_posuvnik.set(2) # prednastaveny interval na 2 sekundy
        self.interval_posuvnik.pack()
        
        self.interval_label = tk.Label(master, text="casovy interval (s)")
        self.interval_label.pack(pady=5)
        
        self.tlacidlo_pridaj = tk.Button(master, text="Pridat server", command=self.pridaj_server)
        self.tlacidlo_pridaj.pack(pady=5)
        
        self.tlacidlo_start = tk.Button(master, text="Spustit monitorovanie", command=self.spusti_monitorovanie)
        self.tlacidlo_start.pack(pady=5)
        
        self.tlacidlo_stop = tk.Button(master, text="Zastavit monitorovanie", command=self.zastav_monitorovanie)
        self.tlacidlo_stop.pack(pady=5)
        
        self.zobraz_graf_tlacidlo = tk.Button(master, text="Zobrazit graf oneskoreni", command=self.vykresli_graf_oneskoreni)
        self.zobraz_graf_tlacidlo.pack(pady=5)
        
        self.tlacidlo_zobraz_historiu = tk.Button(master, text="Zobrazit historiu oneskoreni", command=self.zobraz_obsah_db)
        self.tlacidlo_zobraz_historiu.pack(pady=5)
        
        self.vystupny_text = tk.Text(master, height=10, width=50)
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
            self.uloz_do_db(server, round(oneskorenie, 2))
            
        except (socket.timeout, socket.error):
            self.vystupny_text.insert(tk.END, f"Server {server} nie je dostupny\n")
            
    def spusti_monitorovanie(self):
        self.prebieha_monitorovanie = True
        self.vystupny_text.delete(1.0, tk.END)
        self.vystupny_text.insert(tk.END, "Monitorovanie bolo spustene\n")
        self.monitorovacie_vlakno = threading.Thread(target=self.monitoruj_oneskorenia)
        self.monitorovacie_vlakno.start()
        self.init_db() # nadviazanie spojenia s databazou
        
    def zastav_monitorovanie(self):
        self.prebieha_monitorovanie = False
        self.vystupny_text.insert(tk.END, "Monitorovanie bolo zastavene\n")
        self.conn.close() # ukoncenie spojenia s databazou
        
    def monitoruj_oneskorenia(self):
        interval = self.interval_posuvnik.get() # ziskanie intervalu z posuvnika
        while self.prebieha_monitorovanie:
            for server in self.servery:
                self.ping_server(server)
            time.sleep(interval) # casovy interval v akom sa budu pingovat servery - ziskame z posuvnika
            
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
            
    # inicializacia databazy
    def init_db(self):
        self.conn = sqlite3.connect("db/udaje_oneskorenia.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS oneskorenia (
                                id INTEGER PRIMARY KEY,
                                adresa_servera TEXT,
                                oneskorenie_ms REAL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )
                        ''')
        self.conn.commit()
        
    # funkcia na ulozenie udajov do databazy
    def uloz_do_db(self, adresa_servera, oneskorenie):
        self.cursor.execute('INSERT INTO oneskorenia (adresa_servera, oneskorenie_ms) VALUES (?, ?)', (adresa_servera, oneskorenie))
        self.conn.commit()
        
    def zobraz_obsah_db(self):
        # vytvorenie noveho okna
        db_okno = Toplevel(self.master)
        db_okno.title("Obsah databazy (historia oneskoreni)")
        
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
        
        # prepojenie scrollbaru s canvas
        platno.configure(yscrollcommand=scrollbar.set)
        
        # pridanie hlavicky tabulky
        hlavicka = ["ID", "Adresa servera", "Oneskorenie (ms)", "Cas"]
        for j, nazov_stlpca in enumerate(hlavicka):
            label = tk.Label(scrollable_ramec, text=nazov_stlpca, font=("Arial", 10, "bold"))
            label.grid(row=0, column=j, padx=5, pady=5)
        
        # nacitanie udajov z databazy
        try:
            self.init_db()
            self.cursor.execute("SELECT * FROM oneskorenia")
            rows = self.cursor.fetchall()
            
            # vytvorenie tabulky na zobrazenie udajov
            for i, row in enumerate(rows):
                for j, hodnota in enumerate(row):
                    label = tk.Label(scrollable_ramec, text=hodnota)
                    label.grid(row=i + 1, column=j, padx=5, pady=5)
                    
        except sqlite3.Error as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa nacitat udaje z databazy: {e}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorOneskoreni(root)
    root.mainloop()