from PyQt5.QtWidgets import QMessageBox
from api_client import APIClient
from functions.fetch_errors import extract_hms_errors  # Import the function
from functions.refresh_tokens import refresh_camera_tokens

def refresh_status(self):
    state = APIClient.get_state('sensor.x1c_00m09a351100110_print_status')
    if state:
        self.status_label.setText(f"Status: {state}")
    else:
        self.status_label.setText("Status: Error")
    
    error_state = APIClient.get_state('binary_sensor.x1c_00m09a351100110_hms_errors')
    if error_state == 'on':
        log_text = extract_hms_errors(APIClient.fetchErrors())
        self.errorStateLabel.setText("HMS Errors: Detected")
        self.errorStateLabel.setStyleSheet("QLabel { color: #FF6347; }")
        QMessageBox.warning(self, 'Error Detected', f'An error has been detected by the HMS. Please check the system immediately. {log_text}', QMessageBox.Ok)
    else:
        self.errorStateLabel.setText("HMS Errors: None")
        self.errorStateLabel.setStyleSheet("QLabel { color: #90EE90; }")

    current_stage = APIClient.get_state('sensor.x1c_00m09a351100110_current_stage')
    self.currentStageLabel.setText(f"Current Stage: {current_stage}")
    self.updateStageLabelAppearance(current_stage)

    remaining_time = APIClient.get_state('sensor.x1c_00m09a351100110_remaining_time')
    self.remainingTimeLabel.setText(f"Remaining Time: {remaining_time}")

    gcode_filename = APIClient.get_state('sensor.x1c_00m09a351100110_task_name')
    if gcode_filename:
        self.gcodeFilenameLabel.setText(f"GCode Filename: {gcode_filename}")
    else:
        self.gcodeFilenameLabel.setText("GCode Filename: --")


    self.refresh_temperatures()
    #self.updateTemperatureGraph()
    self.updateProgressGauge()
    self.runAwayProtect()
    self.refresh_camera_tokens()