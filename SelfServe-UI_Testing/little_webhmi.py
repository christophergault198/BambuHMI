from flask import Flask, render_template, send_file
import sys
import os
from send_gcode import send_command
from dds import publisher, subscribe
import subprocess
import json
import threading
import time

app = Flask(__name__)

# Global variable to hold the current job name
current_job_name = "None"

def update_current_job():
    global current_job_name
    while True:
        try:
            with open('/userdata/Metadata/plate_1.json', 'r') as file:
                data = json.load(file)
                # Assuming the structure of the JSON remains consistent
                name = data['bbox_objects'][0]['name']
                current_job_name = name
        except Exception as e:
            print(f"Error reading or parsing JSON file: {e}")
        time.sleep(10)

@app.route('/')
def printer_hmi():
    # Example printer details
    printer_details = {
        'status': 'Printing',
        'current_job': current_job_name,  # Use the global variable
        'progress': 75,
        'temperature': {
            'nozzle': 215,
            'bed': 60
        }
    }
    return render_template('index.html', details=printer_details)

@app.route('/home_xyz_func', methods=['GET','POST'])
def home_xyz_func():
    subprocess.run(["/usr/bin/home_xyz.sh"], shell=False)
    return 'G-code command sent successfully'

@app.route('/current_image')
def current_image():
    image_path = '/userdata/log/cam/capture/calib_14.jpg'
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/current_model_image')
def current_model_image():
    image_path = '/userdata/log/cam/flc/report/ref_model.png'
    return send_file(image_path, mimetype='image/png')


if __name__ == '__main__':
    # Start the background thread
    threading.Thread(target=update_current_job, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

