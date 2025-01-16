#!/bin/bash/python3 python

import tkinter as tk
from uvod import Uvod

# hlavny vstup programu, otvori uvodne okno    
if __name__ == "__main__":
    root = tk.Tk()
    Uvod(root)
    root.mainloop()