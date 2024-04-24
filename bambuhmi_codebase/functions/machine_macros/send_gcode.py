import dds
import json
import time 


def send_project(pub, plate_number, url):
    """Sends a project file using DDS command."""
    msg = {
    	"command": "project_file", 
    	"param": f"Metadata/plate_{plate_number}.gcode", 
    	"sequence_id": 0,
		"project_id": "0", # Always 0 for local prints
        "profile_id": "0", # Always 0 for local prints
        "task_id": "0", # Always 0 for local prints
        "subtask_id": "0", # Always 0 for local prints
        "subtask_name": "",

        "file": "", # Filename to print, not needed when "url" is specified with filepath
        "url": f"file://{url}", # URL to print. Root path, protocol can vary. E.g., if sd card, "ftp:#/myfile.3mf", "ftp:#/cache/myotherfile.3mf"
        "md5": "",

        "timelapse": True,
        "bed_type": "auto", # Always "auto" for local prints
        "bed_levelling": True,
        "flow_cali": True,
        "vibration_cali": True,
        "layer_inspect": True,
        "ams_mapping": "",
        "use_ams": False
    	}
    json_msg = json.dumps(msg)
    pub(json_msg)
    print(f"File sent: {cmd}")
    
def send_file(pub, cmd):
    """Sends a gcode file using DDS command."""
    msg = {"command": "gcode_file", "param": cmd, "sequence_id": 0}
    json_msg = json.dumps(msg)
    pub(json_msg)
    print(f"File sent: {cmd}")

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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        dds.shutdown()
