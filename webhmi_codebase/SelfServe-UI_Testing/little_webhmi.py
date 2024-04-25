from flask import Flask, render_template, send_file, redirect, url_for, request
import sys
import os
from send_gcode import send_command
from dds import publisher, subscribe
import subprocess
import json
import threading
import time
import requests

app = Flask(__name__)

# Global variable to hold the current job name
current_job_name = "None"
# Global variable to hold the latest message
latest_message = ""

def update_current_job():
    global current_job_name
    while True:
        try:
            with open('/userdata/print_ctx.json', 'r') as file:
                data = json.load(file)
                # Adjusted to fetch 'subtask_name' as per the new JSON structure
                subtask_name = data['subtask_name']
                current_job_name = subtask_name
                send_image_for_prediction('/userdata/log/cam/capture/calib_14.jpg')
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
        },
        'latest_message': latest_message,  # Include the latest message
        'prediction': send_image_for_prediction('/userdata/log/cam/capture/calib_14.jpg')  # Get prediction result
    }
    return render_template('index.html', details=printer_details)


@app.route('/home_xyz_func', methods=['GET','POST'])
def home_xyz_func():
    global latest_message
    subprocess.run(["/usr/bin/home_xyz.sh"], shell=False)
    latest_message = 'Home XYZ'
    return redirect(url_for('printer_hmi'))

@app.route('/preheat_100c', methods=['GET','POST']) #Bed Heat 100c ON
def preheat_100c():
    global latest_message
    subprocess.run(["/usr/bin/heatbed_set.sh", "-s", "100"], shell=False)
    latest_message = 'Preheat Activated - 100c'
    return redirect(url_for('printer_hmi'))

@app.route('/preheat_0c', methods=['GET','POST']) #Bed Heat 0c OFF
def preheat_0c():
    global latest_message
    subprocess.run(["/usr/bin/heatbed_set.sh", "-s", "0"], shell=False)
    latest_message = 'Preheat Deactivated'
    return redirect(url_for('printer_hmi'))

@app.route('/start_bbl_screen_vnc', methods=['GET','POST']) #Start VNC
def start_bbl_screen_vnc():
    global latest_message
    try:
        latest_message = 'VNC Started'
        subprocess.run(["/usr/bin/start_bbl_screen_vnc.sh"], shell=True, timeout=3)  # Add a timeout of 3 second and avoid callback because im lazy.
    except subprocess.TimeoutExpired:
        latest_message = 'VNC Started' #This is odd but true, it does start the VNC server. Again, lazy mode.
    return redirect(url_for('printer_hmi'))

@app.route('/current_image')
def current_image():
    image_path = '/userdata/log/cam/capture/calib_14.jpg'
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/current_model_image')
def current_model_image():
    image_path = '/userdata/log/cam/flc/report/ref_model.png'
    return send_file(image_path, mimetype='image/png')

@app.route('/current_depthmap_image')
def current_depthmap_image():
    image_path = '/userdata/log/cam/flc/report/depth_map.png'
    return send_file(image_path, mimetype='image/png')

@app.route('/current_errmapdepth_image')
def current_errmapdepth_image():
    image_path = '/userdata/log/cam/flc/report/errmap_depth.png'
    return send_file(image_path, mimetype='image/png')

def send_image_for_prediction(image_path):  
    try:
        url = 'http://192.168.8.135:5001/predict'
        files = {'image': open(image_path, 'rb')}
        response = requests.post(url, files=files, timeout=5)
        prediction_result = response.json()
        return prediction_result
    except requests.exceptions.RequestException as e:  # This catches all exceptions related to the request
        print(f"Error connecting to the prediction service or timeout occurred: {e}")
        prediction_result = "Prediction server not found on the local network or is not currently running."
        if 'Prediction Server Not Found on Local Network or is not currently running.' in prediction_result:
            prediction_result = prediction_result.replace('Prediction Server Not Found on Local Network or is not currently running.', '')
        return prediction_result

if __name__ == '__main__':
    # Start the background thread
    threading.Thread(target=update_current_job, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
