import paramiko
import tkinter as tk
from tkinter import messagebox
import threading  # Import threading at the beginning of your file

def ssh_command_execution(hostname, port, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        client.close()
        if output:
            messagebox.showinfo("Output", output)
        if error:
            messagebox.showerror("Error", error)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_run_command():
    def delayed_start():
        hostname = '192.168.9.78'
        port = 22
        username = 'bblp'  # Replace with the actual username
        password = '4e1cf6eb'  # Replace with the actual password
        command = '/usr/bin/start_bbl_screen_vnc.sh'
        # Run ssh_command_execution in a separate thread
        threading.Thread(target=ssh_command_execution, args=(hostname, port, username, password, command)).start()
        print("VNC Started")

    # Delay VNC start by 1000 milliseconds (1 second) after the UI loads
    root.after(1000, delayed_start)

    # Schedule the application to close 30 seconds after the button is clicked
    root.after(30000, root.destroy)

# Setting up the GUI
root = tk.Tk()
root.title("X1C VNC Start")

run_command_button = tk.Button(root, text="VNC Start", command=on_run_command)
run_command_button.pack(pady=20)

root.mainloop()
