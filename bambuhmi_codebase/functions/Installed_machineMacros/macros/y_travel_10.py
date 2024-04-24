import json, subprocess, os, time,re

#Input a set temperature and run the script
#Chamber temp is monitored until the set temperature is reached
#The chamber temp you'll reach without active heating is 45-55C depending on 
#the ambient temperature of your workspace
setTemp = 45 #Target chamber temp
logData = False #Save chamber temp values to file
savefile = "/tmp/chamber_temp" #save location for chamber temp data

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
        print(f"error {e}")
def save_log(strs,sfile):
    with open(sfile, "a") as sf:
        sf.write(strs)
        
def printJson(key):
    try:
        with open('/config/screen/printer.json', 'r') as file:
            data = json.load(file)
         
            return data.get(key, False)
    except FileNotFoundError:
        print("printer.json doesn't exist")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
        
def main():
    gcode_str_on = "G91\nG1 Y10\nG90"
    
    send_gcode(gcode_str_on)

    time.sleep(5)
if __name__ == "__main__":
    main()


