import threading

def screen_restart_service(self):
        restart_cmd = "/etc/init.d/S99screen_service restart"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(restart_cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")


def CameraDebug(self):                   #NEED TO FIX - BROKEN
        cmd = "/usr/bin/camera_debug.sh -opt 10"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HomeXYZ(self):                      
        cmd = "/usr/bin/home_xyz.sh"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HeatBed_Set100c(self):              
        cmd = "/usr/bin/heatbed_set.sh -s 100"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HeatBed_Set0c(self):               
        cmd = "/usr/bin/heatbed_set.sh -s 0"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def MoveXNegative(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/x_travel_-10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def MoveXPositive(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/x_travel_10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")
def MoveYNegative(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/y_travel_-10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")
def MoveYPositive(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/y_travel_10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")
def MoveZNegative(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/z_travel_-10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")
def MoveZPositive(self):
        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/z_travel_10.py"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

















           