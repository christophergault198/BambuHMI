from api_client import APIClient
from PyQt5.QtWidgets import QMessageBox

def runaway_protect():
    nozzle_temperature = APIClient.get_temperature('sensor.x1c_00m09a351100110_nozzle_temperature')
    if nozzle_temperature is not None and nozzle_temperature > 300:
        APIClient.statePOST('button.x1c_00m09a351100110_stop_printing')
        show_popup("Emergency stop activated due to high nozzle temperature!")

def show_popup(message):
    # Implementation depends on your application's environment.
    # This could be a GUI dialog, a web-based notification, or a log message.
    QMessageBox.information(None, "THERMAL ISSUE", "E-STOP ACTIVATED", QMessageBox.Ok)
    print(f"Popup: {message}")
