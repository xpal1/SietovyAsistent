#!/bin/bash/python3 python

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from ping3 import ping
import threading
import time

# trieda pre monitorovanie oneskorenia (odozvy) serverov
class MonitorOneskoreni():
    def __init__(self,master):
        self.master = master
        self.master.title("Monitorovanie oneskorenia serverov")
        
        self.servery = []
        self.oneskorenia_data = pd.DataFrame(columns=["Server", "Oneskorenie (ms)"])
        
        self.server_vstup = tk.Entry(master)
        self.server_vstup.pack(pady=10)
        
        self.tlacidlo_pridaj = tk.Button(master, text="Pridat server", command=self.pridaj_server)
        self.tlacidlo_pridaj.pack(pady=5)
        
        self.tlacidlo_start = tk.Button(master, text="Spustit monitorovanie", command=self.spusti_monitorovanie)
        self.tlacidlo_start.pack(pady=5)
        
        self.zobraz_graf_tlacidlo = tk.Button(master, text="Zobrazit graf oneskoreni", command=self.vykresli_graf_oneskoreni)
        self.zobraz_graf_tlacidlo.pack(pady=5)
        
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
        oneskorenie = ping(server)
        if oneskorenie is not None:
            oneskorenie = round(oneskorenie * 1000, 2) # prevod na milisekundy
            self.oneskorenia_data.loc[len(self.oneskorenia_data)] = [server, oneskorenie]
            self.vystupny_text.insert(tk.END, f"Ping z {server}: {oneskorenie} ms\n")
        else:
            self.vystupny_text.insert(tk.END, f"Server {server} nie je dostupny\n")
            
    def spusti_monitorovanie(self):
        self.vystupny_text.delete(1.0, tk.END)
        self.monitorovacie_vlakno = threading.Thread(target=self.monitoruj_oneskorenia)
        self.monitorovacie_vlakno.start()
        
    def monitoruj_oneskorenia(self):
        while True:
            for server in self.servery:
                self.ping_server(server)
            time.sleep(2) # casovy interval v akom sa budu pingovat servery
            
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
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorOneskoreni(root)
    root.mainloop()