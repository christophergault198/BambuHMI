import os
import tkinter as tk
from tkinter import filedialog, Listbox
import paramiko
from config import PRINTER_IP, PRINTER_USERNAME, PRINTER_PASSWORD

ip = PRINTER_IP
username = PRINTER_USERNAME
password = PRINTER_PASSWORD

def upload_file_to_server(local_path, server_folder, server_address, username, password):
    transport = paramiko.Transport((server_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    file_name = os.path.basename(local_path)
    server_path = f"{server_folder}/{file_name}"

    sftp.put(local_path, server_path)

    sftp.close()
    transport.close()

def list_files_in_directory(server_folder, server_address, username, password):
    transport = paramiko.Transport((server_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    files = sftp.listdir(server_folder)

    sftp.close()
    transport.close()
    return files

def browse_file():
    file_path = filedialog.askopenfilename()
    upload_file_to_server(file_path, '/opt/python/bin/templates', ip, username, password)

def show_files():
    files = list_files_in_directory('/opt/python/bin/templates', ip, username, password)
    for file in files:
        listbox.insert(tk.END, file)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SD Upload Tool")

    upload_button = tk.Button(root, text="Upload File", command=browse_file)
    upload_button.pack()

    list_files_button = tk.Button(root, text="List Files", command=show_files)
    list_files_button.pack()

    listbox = Listbox(root)
    listbox.pack()

    root.mainloop()

