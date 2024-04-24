from api_client import APIClient
from PyQt5.QtWidgets import QMessageBox
from config import PRINTER_ID

def runaway_protect():
    nozzle_temperature = APIClient.get_temperature(f'sensor.x1c_{PRINTER_ID}_nozzle_temperature')
    if nozzle_temperature is not None and nozzle_temperature > 300:
        APIClient.statePOST(f'button.x1c_{PRINTER_ID}_stop_printing')
        show_popup("Emergency stop activated due to high nozzle temperature!")

def show_popup(message):
    # Implementation depends on your application's environment.
    # This could be a GUI dialog, a web-based notification, or a log message.
    QMessageBox.information(None, "THERMAL ISSUE", "E-STOP ACTIVATED", QMessageBox.Ok)
    print(f"Popup: {message}")
