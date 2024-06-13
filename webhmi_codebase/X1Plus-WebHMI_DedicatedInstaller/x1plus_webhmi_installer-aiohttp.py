import os
import tkinter as tk
from tkinter import messagebox
import paramiko
import subprocess
from config import PRINTER_USERNAME

username = PRINTER_USERNAME

def upload_file_to_server(local_path, server_folder, server_address, username, password):
    transport = paramiko.Transport((server_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    file_name = os.path.basename(local_path)
    server_path = f"{server_folder}/{file_name}"

    # Read the file, convert line endings, and write to a temporary file
    with open(local_path, 'rb') as file:
        content = file.read().replace(b'\r\n', b'\n')
    
    # Use StringIO to simulate a file object with Unix line endings
    from io import BytesIO
    file_obj = BytesIO(content)

    # Upload the file
    sftp.putfo(file_obj, server_path)

    sftp.close()
    transport.close()

def upload_directory_to_server(local_directory, server_directory, server_address, username, password):
    transport = paramiko.Transport((server_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Ensure the base server directory exists and create it if it does not
    try:
        sftp.stat(server_directory)
    except IOError:
        sftp.mkdir(server_directory)

    for root, dirs, files in os.walk(local_directory):
        relative_root = os.path.relpath(root, start=local_directory)
        server_root = f"{server_directory}/{relative_root.replace('\\', '/')}"

        # Create the directory on the server if it does not exist
        try:
            sftp.stat(server_root)
        except IOError:
            sftp.mkdir(server_root)

        for file in files:
            local_path = os.path.join(root, file)
            server_path = f"{server_root}/{file}"  # Use forward slashes directly

            sftp.put(local_path, server_path)

    sftp.close()
    transport.close()

def change_permission(server_path, server_address, username, password):
    transport = paramiko.Transport((server_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.chmod(server_path, 0o755)  # Equivalent to 'chmod +x'

    sftp.close()
    transport.close()

def notify_user(message):
    messagebox.showinfo("Notification", message)

def execute_remote_command(command, server_address, username, password):
    # Establish an SSH connection to the server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_address, username=username, password=password)

    # Execute the remote command
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read().decode())  # Optionally print command output
    print(stderr.read().decode())  # Optionally print error output

    ssh.close()

def full_installation(ip, password):
    notify_user("Starting Installation, this may take some time...")
    print("Connected Successfully. Installing dependencies...")
    upload_directory_to_server('webhmi', '/usr/etc/system/webhmi/', ip, username, password)
    print("webhmi folder created and dependencies uploaded. Uploading scripts...")
    upload_file_to_server('heatbed_set.sh', '/usr/bin', ip, username, password)
    upload_file_to_server('home_xyz.sh', '/usr/bin', ip, username, password)
    upload_file_to_server('S98webhmi', '/etc/init.d', ip, username, password)
    upload_file_to_server('get-pip.py', '/usr/bin', ip, username, password)
    print("Scripts uploaded. Setting executable permissions...")
    change_permission('/usr/bin/heatbed_set.sh', ip, username, password)
    change_permission('/usr/bin/home_xyz.sh', ip, username, password)
    change_permission('/etc/init.d/S98webhmi', ip, username, password)
    print("Installing pip and requirements. This may take a few minutes...")
    # Execute Python and Pip installation commands on the remote server
    execute_remote_command('/opt/python/bin/python3 /usr/bin/get-pip.py', ip, username, password)
    #execute_remote_command('/opt/python/bin/python3 -m pip install aiohttp', ip, username, password)
    execute_remote_command('/opt/python/bin/python3 -m pip install aiohttp_jinja2', ip, username, password)

    notify_user("Installation Complete. Reboot your printer to enable the web interface on port 5001.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("HMI Installer")

    ip_label = tk.Label(root, text="Printer IP:")
    ip_label.pack()
    ip_entry = tk.Entry(root)
    ip_entry.pack()

    password_label = tk.Label(root, text="Printer Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def start_installation():
        ip = ip_entry.get()
        password = password_entry.get()
        full_installation(ip, password)

    install_button = tk.Button(root, text="Install", command=start_installation)
    install_button.pack()

    root.mainloop()
