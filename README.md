![Screenshot 2024-04-24 111145](https://github.com/christophergault198/BambuHMI/assets/116657484/90b244ad-0040-4eed-984c-4cef83d6615e)
![hmi_interface](https://github.com/christophergault198/BambuHMI/assets/116657484/00042aee-bcd0-4a71-a7ce-912b3d272a31)


https://github.com/christophergault198/BambuHMI/assets/116657484/96ba1e52-e2a6-44d9-aa73-67ae36cd53a2



# BambuHMI and X1Plus WebHMI
 Dedicated and self served web based HMI for Bambu printers running on HA and/or the X1Plus firmware.
*WebHMI coming soon...

PreReqs:
1) X1C Printer connected to a HA instance (https://github.com/greghesp/ha-bambulab)
2) X1Plus Firmware installed on your X1C Printer (https://github.com/X1Plus/X1Plus/wiki/Installation-Guide)

# How to use:
1) Use pip to install the necessary dependencies from the requirements.txt file (pip install -r requirements.txt)
2) Launch setup.py and configure the HA and X1C printer settings and credentials.
3) Click 'Save Config' then 'Install Files to Printer'.
4) Optional - Create single app with "pyinstaller main_wCamera.py --icon geometric.ico", be sure to move the fonts & functions folder to the root of the newly built exe.

*Make sure to set static addresses for both your printer and HA instance.

# Quick Code References:
The mechanism used to send G-code commands to the printer involves several methods, primarily through MQTT and SSH commands. The process is initiated in different parts of the codebase, depending on the context and the specific action being performed.
1. MQTT for G-code Commands:
G-code commands are sent using MQTT in various macros. This is evident in the send_gcode function within macros like homexyz.py, x_travel_10.py, and others. The mqtt_pub function is called with a JSON payload containing the G-code command.
---
def send_gcode(gcode_line):

    json_payload = {

        "print": {

            "command": "gcode_line",

            "sequence_id": "2001",

            "param": gcode_line

        }

    }

    mqtt_pub(json.dumps(json_payload))



def mqtt_pub(message):

    command = f"source /usr/bin/mqtt_access.sh; mqtt_pub '{message}'"

    try:

        subprocess.run(command, shell=True, check=True, executable='/bin/bash')

    except subprocess.CalledProcessError as e:
---

2. SSH for Remote Command Execution:
SSH is used in the BambuHMI SSH Commander to execute Python scripts on the printer, which in turn send G-code commands. This is seen in the commands.py file where SSH commands are used to execute macros like x_travel_-10.py.

---
def MoveXNegative(self):

        cmd = "/opt/python/bin/python3 /mnt/sdcard/x1plus/macros/x_travel_-10.py"

        if self.ssh_client:

            command_thread = threading.Thread(target=self.execute_command, args=(cmd,))

            command_thread.start()

        else:

            self.append_output("Not connected to any server.")
---
3. Direct G-code Command Sending:
Direct sending of G-code commands is also facilitated through a DDS (Data Distribution Service) publisher in send_gcode.py, where commands are sent over a DDS network.
---
def send_command(pub, cmd):

    """Sends a command using DDS publisher."""

    msg = {"command": "gcode_line", "param": cmd, "sequence_id": 0}

    json_msg = json.dumps(msg)

    pub(json_msg)

    print(f"Command sent: {cmd}")



def main():

    pub = dds.publisher('device/request/print')

    time.sleep(3) 

    while True:

        cmd = input("Enter the gcode command you want to send or type 'exit' to quit: ")

        if cmd.lower() == 'exit':

            print("Exiting command input.")

            break

        send_command(pub, cmd)
---
4. Shell Scripts:
Shell scripts like heatbed_set.sh are used to send G-code commands via MQTT, which can be triggered through SSH or other mechanisms.
---
function set_heatbed_temp() {

    temp=$1

    json="{ \

        \"print\":{\"command\":\"gcode_line\", \"sequence_id\":\"2002\", \"param\":\"M140 S$temp\"} \

    }"
---
