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
        
        self.tlacidlo_pridaj = tk.Button(master, text="Pridat server")
        self.tlacidlo_pridaj.pack(pady=5)
        
        self.tlacidlo_start = tk.Button(master, text="Spustit monitorovanie")
        self.tlacidlo_start.pack(pady=5)
        
        self.zobraz_graf_tlacidlo = tk.Button(master, text="Zobrazit graf oneskoreni")
        self.zobraz_graf_tlacidlo.pack(pady=5)
        
        self.vystupny_text = tk.Text(master, height=10, width=50)
        self.vystupny_text.pack(pady=10)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorOneskoreni(root)
    root.mainloop()