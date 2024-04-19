import tkinter as tk
from tkinter import scrolledtext, messagebox
import shutil
import os
import paramiko
from config import *

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
        'functions/Tools/sd_upload_tool',
        'functions'
    ]
    for dest in destinations:
        shutil.copy('config.py', dest)
    messagebox.showinfo("Success", "Config file setup successfully!")

# Add a popup confirmation before uploading files to the printer
def upload_files():
    if messagebox.askokcancel("Confirmation", "This will install all the files within /functions/Installed_machineMacros/macros & sh folders to the printer."):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(PRINTER_IP, username=PRINTER_USERNAME, password=PRINTER_PASSWORD)  # Update with your server's details
            sftp = ssh.open_sftp()

            # Upload files from /functions/Installed_machineMacros/macros to /mnt/sdcard/x1plus/macros/
            macros_source = 'functions/Installed_machineMacros/macros'
            macros_target = '/mnt/sdcard/x1plus/macros/'
            for file in os.listdir(macros_source):
                sftp.put(os.path.join(macros_source, file), os.path.join(macros_target, file))

            # Upload files from /functions/Installed_machineMacros/sh to /usr/bin
            sh_source = 'functions/Installed_machineMacros/sh'
            sh_target = '/usr/bin'
            for file in os.listdir(sh_source):
                sftp.put(os.path.join(sh_source, file), os.path.join(sh_target, file))

            messagebox.showinfo("Success", "Files uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload files: {e}")
        finally:
            if ssh:
                ssh.close()

# Create the main window
root = tk.Tk()
root.title("BambuHMI Configurator")
root.geometry("800x600")

# Create a label above the text field
label = tk.Label(root, text="Modify your configuration and 'Apply Config' before proceeding with 'Install Files to Printer'.")
label.pack(padx=10, pady=10)

# Create a scrolled text widget for editing the config file with text box scaling
editor = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
editor.pack(expand=True, fill='both', padx=10, pady=10)
editor.insert(tk.INSERT, load_config())

# Copy button
copy_button = tk.Button(root, text="Apply Config", command=copy_config)
copy_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Upload button
upload_button = tk.Button(root, text="Install Files to Printer", command=upload_files)
upload_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()
