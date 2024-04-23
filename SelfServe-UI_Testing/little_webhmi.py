from flask import Flask, render_template
import sys
import os
from send_gcode import send_command
from dds import publisher

app = Flask(__name__)

@app.route('/')
def printer_hmi():
    # Example printer details
    printer_details = {
        'status': 'Printing',
        'current_job': 'ExampleModel.gcode',
        'progress': 75,
        'temperature': {
            'nozzle': 215,
            'bed': 60
        }
    }
    return render_template('index.html', details=printer_details)

@app.route('/home_printer')
def home_printer():
    send_command(publisher, 'G28')  # Assuming 'G28' is the command for homing the printer
    return 'Printer homing command sent'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_gcode', methods=['POST'])
def send_gcode():
    gcode = request.form['gcode']
    # Handle G-code sending here, e.g., using MQTT or SSH
    # For example, using the MQTT shell script from the codebase:
    # subprocess.run(["/path/to/gcode_mqtt_ex.sh", gcode], shell=True)
    return jsonify({'status': 'success', 'gcode': gcode})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
