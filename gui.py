import tkinter as tk
from tkinter import ttk
import pymem
from pymem.process import module_from_name

pm = pymem.Pymem("ac_client.exe")
gameModule = module_from_name(pm.process_handle, "ac_client.exe").lpBaseOfDll

def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i != offsets[-1]:
            addr = pm.read_int(addr + i)
    return addr + offsets[-1]

def apply_mods():
    selected_options = []
    for var, name in zip(option_vars, option_names):
        if var.get():
            selected_options.append(name)
            if name == "Ammo Hack":
                pm.write_int(GetPtrAddr(gameModule + 0x00183828, [0x8, 0x818, 0x98, 0x710]), 1337)

root = tk.Tk()
root.title("Mod Menü")
root.geometry("400x300")

# Überschrift
title_label = ttk.Label(root, text="Willkommen zum Mod Menü", font=("Helvetica", 16))
title_label.pack(pady=10)

option_frame = ttk.LabelFrame(root, text="Modifikationsoptionen")
option_frame.pack(pady=20, padx=20, fill="both", expand=True)

option_names = ["Ammo Hack"]
option_vars = []

for name in option_names:
    var = tk.BooleanVar()
    option_vars.append(var)
    check = ttk.Checkbutton(option_frame, text=name, variable=var)
    check.pack(anchor="w", padx=10, pady=5)

apply_button = ttk.Button(root, text="Anwenden", command=apply_mods)
apply_button.pack(pady=10)

root.mainloop()
