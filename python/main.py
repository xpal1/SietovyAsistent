#!/bin/bash/python3 python

import tkinter as tk
from monitor import MonitorOneskoreni

# hlavny vstup programu        
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorOneskoreni(root)
    root.mainloop()