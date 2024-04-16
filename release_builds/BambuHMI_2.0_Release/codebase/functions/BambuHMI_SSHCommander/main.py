import tkinter as tk
from tkinter import scrolledtext
from paramiko import SSHClient, AutoAddPolicy
import threading
from commands import screen_restart_service, CameraDebug, HomeXYZ, HeatBed_Set100c, HeatBed_Set0c

class SSHClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("BambuHMI SSH Commander")
        master.configure(background='#333')  # Set the background color of the main window

        # Connection Frame
        self.conn_frame = tk.Frame(master, bg='#333')  # Set the background color for this frame
        self.conn_frame.pack(pady=10)

        self.host_label = tk.Label(self.conn_frame, text="Host:", bg='#333', fg='white')  # Adjust label background and text color
        self.host_label.pack(side=tk.LEFT)
        self.host_entry = tk.Entry(self.conn_frame, bg='white', fg='black')  # Adjust entry background and text color if needed
        self.host_entry.pack(side=tk.LEFT)

        self.user_label = tk.Label(self.conn_frame, text="Username:", bg='#333', fg='white')  # Adjust label background and text color
        self.user_label.pack(side=tk.LEFT)
        self.user_entry = tk.Entry(self.conn_frame, bg='white', fg='black')  # Adjust entry background and text color if needed
        self.user_entry.pack(side=tk.LEFT)

        self.pass_label = tk.Label(self.conn_frame, text="Password:", bg='#333', fg='white')  # Adjust label background and text color
        self.pass_label.pack(side=tk.LEFT)
        self.pass_entry = tk.Entry(self.conn_frame, show="*", bg='white', fg='black')  # Adjust entry background and text color if needed
        self.pass_entry.pack(side=tk.LEFT)

        self.connect_button = tk.Button(self.conn_frame, text="Connect", command=self.connect, bg='#555', fg='white')  # Adjust button background and text color
        self.connect_button.pack(side=tk.LEFT)

        # Quick Connect as Root Button
        self.quick_connect_root_button = tk.Button(self.conn_frame, text="Quick Connect as Root", command=self.quick_connect_as_root, bg='#555', fg='white')  # Adjust button background and text color
        self.quick_connect_root_button.pack(side=tk.LEFT)

        # Command Frame
        self.cmd_frame = tk.Frame(master, bg='#333')  # Set the background color for this frame
        self.cmd_frame.pack(pady=10)

        self.cmd_entry = tk.Entry(self.cmd_frame, bg='white', fg='black')  # Adjust entry background and text color if needed
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.send_button = tk.Button(self.cmd_frame, text="Send", command=self.send_command, bg='#555', fg='white')  # Adjust button background and text color
        self.send_button.pack(side=tk.LEFT)

        # Restart Service Button
        self.screen_restart_service_button = tk.Button(self.cmd_frame, text="Screen Restart", command=self.screen_restart_service, bg='#555', fg='white')  # Adjust button background and text color
        self.screen_restart_service_button.pack(side=tk.LEFT)

        self.camera_debug_button = tk.Button(self.cmd_frame, text="Camera Debug", command=self.camera_debug, bg='#555', fg='white')  # Adjust button background and text color
        self.camera_debug_button.pack(side=tk.LEFT)

        self.home_xyz_button = tk.Button(self.cmd_frame, text="Home XYZ", command=self.home_xyz, bg='#555', fg='white')  # Adjust button background and text color
        self.home_xyz_button.pack(side=tk.LEFT)

        self.heatbed_set100c_button = tk.Button(self.cmd_frame, text="HeatBed Set100C", command=self.heatbed_set100c, bg='#555', fg='white')  # Adjust button background and text color
        self.heatbed_set100c_button.pack(side=tk.LEFT)

        self.heatbed_setOFF_button = tk.Button(self.cmd_frame, text="HeatBed SetOFF", command=self.heatbed_setOFF, bg='#555', fg='white')  # Adjust button background and text color
        self.heatbed_setOFF_button.pack(side=tk.LEFT)

        # Output Frame
        self.output = scrolledtext.ScrolledText(master, state='disabled', bg='#333', fg='white')  # Adjust scrolledtext background and text color
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.ssh_client = None

    def connect(self):
        host = self.host_entry.get()
        username = self.user_entry.get()
        password = self.pass_entry.get()

        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.ssh_client.connect(hostname=host, username=username, password=password)
            self.append_output("Connected successfully to {}".format(host))
        except Exception as e:
            self.append_output("Failed to connect: {}".format(e))

    def send_command(self):
        if self.ssh_client:
            cmd = self.cmd_entry.get()
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

    def screen_restart_service(self):
        screen_restart_service(self)

    def camera_debug(self):
        CameraDebug(self)

    def home_xyz(self):
        HomeXYZ(self)

    def heatbed_set100c(self):
        HeatBed_Set100c(self)

    def heatbed_setOFF(self):
        HeatBed_Set0c(self)

    def quick_connect_as_root(self):
        self.host_entry.delete(0, tk.END)
        self.host_entry.insert(0, "192.168.9.78")
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, "root")
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, "a8d11ef407b8")
        self.connect()

    def execute_command(self, cmd):
        try:
            self.append_output("Sent command: {}".format(cmd))
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            self.append_output(output + error)
            
        except Exception as e:
            self.append_output("Error executing command: {}".format(e))

    def append_output(self, text):
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state='disabled')
        self.output.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SSHClientGUI(root)
    root.mainloop()
