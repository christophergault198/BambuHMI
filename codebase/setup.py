import tkinter as tk
from tkinter import scrolledtext, messagebox
import shutil
import os

# Load the content of config.py into a string
def load_config():
    with open('config.py', 'r') as file:
        return file.read()

# Save the modified content back to config.py
def save_config(new_content):
    with open('config.py', 'w') as file:
        file.write(new_content)

# Copy config.py to the specified directories
def copy_config():
    destinations = [
        'functions/BambuHMI_SSHCommander',
        'functions/RIV',
        'functions/Tools/sd_upload_tool'
    ]
    for dest in destinations:
        shutil.copy('config.py', dest)
    messagebox.showinfo("Success", "Config file setup successfully!")

# Create the main window
root = tk.Tk()
root.title("Config Editor")

# Create a scrolled text widget for editing the config file
editor = scrolledtext.ScrolledText(root, width=60, height=20)
editor.pack(padx=10, pady=10)
editor.insert(tk.INSERT, load_config())

# Save button
#save_button = tk.Button(root, text="Save Changes", command=lambda: save_config(editor.get("1.0", tk.END)))
#save_button.pack(side=tk.LEFT, padx=10, pady=10)

# Copy button
copy_button = tk.Button(root, text="Apply Config", command=copy_config)
copy_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()
