import threading

def screen_restart_service(self):
        restart_cmd = "/etc/init.d/S99screen_service restart"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(restart_cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")


def CameraDebug(self):
        cmd = "/usr/bin/camera_debug.sh"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HomeXYZ(self):
        cmd = "/usr/bin/homexyz.sh"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HeatBed_Set100c(self):
        cmd = "/usr/bin/heatbed_set100c.sh"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

def HeatBed_Set0c(self):
        cmd = "/usr/bin/heatbed_setOFF.sh"
        if self.ssh_client:
            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))
            command_thread.start()
        else:
            self.append_output("Not connected to any server.")

















           