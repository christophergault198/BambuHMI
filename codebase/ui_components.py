import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QProgressBar, QMessageBox, QDialog, QVBoxLayout, QCheckBox, QMenu, QAction, QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import QTimer  # Import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Add this import at the beginning
from PyQt5.QtCore import QUrl
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from api_client import APIClient
from functions.refresh_status import refresh_status
from functions.start_print import start_print
from functions.fan_control import toggle_fan
from functions.runaway_protect import runaway_protect
from functions.stateSpeed import SelectionWindow
from functions.fetch_errors import extract_hms_errors
from functions.refresh_tokens import refresh_camera_tokens
import subprocess  # Import subprocess at the beginning of the file

class BambuLabHMI(QWidget):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont("./fonts/Roboto-Regular.ttf")

        QApplication.setFont(QFont('Roboto', 11))  # Set the application-wide font to Roboto, size 11
        self.initUI()
        self.initRefreshTimer()  # Initialize the refresh timer
        self.showMQTTModePopup()  # Show MQTT mode popup at startup
        self.refresh_status()  # Initial call to refresh status

        # Initialize the label for the indicator light
        self.indicatorLight = QLabel(self)
        self.indicatorLight.setStyleSheet("background-color: green")
        self.indicatorLight.setFixedSize(2500, 8)  # Adjust size as needed

        # Setup a timer for the blinking effect
        self.blinkTimer = QTimer(self)
        self.blinkTimer.timeout.connect(self.toggleIndicator)
        self.blinkTimer.start(1000)  # Blinking interval in milliseconds

    def toggleIndicator(self):
        # Check if the printer is not idle
        if not self.isPrinterIdle():
            # Toggle the visibility of the indicator light
            self.indicatorLight.setVisible(not self.indicatorLight.isVisible())
        else:
            # Ensure the indicator is off when the printer is idle
            self.indicatorLight.setVisible(False)

    def isPrinterIdle(self):
        current_stage = APIClient.get_state('sensor.x1c_00m09a351100110_current_stage')
        return current_stage == 'idle'
        return False

    def initUI(self):
        self.setWindowTitle('BambuHMI 2.0')
        self.setGeometry(100, 100, 440, 680)
        self.setStyleSheet("QWidget { background-color: #333; color: #999; } QPushButton { font-weight: bold; } QLabel { font-size: 14px; }")

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        
        self.setupControls(mainLayout)
        self.setupTemperatureGraph(mainLayout)
        self.setupProgressGauge(mainLayout)  # Add this line to setup the temperature gauge
        self.setupEStopButton(mainLayout)
        
        # Create a horizontal layout for the bottom labels
        bottomLabelsLayout = QHBoxLayout()
        bottomLabelsLayout.setSpacing(10)
        
        # Add the error state label to your layout
        self.errorStateLabel = QLabel('HMS Errors: --')
        self.errorStateLabel.setStyleSheet("QLabel { color: #FF6347; }")  # Use a color that indicates an error (e.g., tomato red)
        bottomLabelsLayout.addWidget(self.errorStateLabel)  # Assuming your main layout variable is named mainLayout
        
        # Add the fancy label for displaying the current stage
        self.currentStageLabel = QLabel('Current Stage: --')
        self.updateStageLabelAppearance('--')  # Initial call to set the label's appearance
        bottomLabelsLayout.addWidget(self.currentStageLabel)  # Assuming your main layout variable is named mainLayout
        
        # Add a QLabel for displaying remaining time
        self.remainingTimeLabel = QLabel('Remaining Time: --')
        bottomLabelsLayout.addWidget(self.remainingTimeLabel)  # Add the label to your layout

        # G-code filename path label
        self.gcodeFilenameLabel = QLabel('G-code File: --')  # Placeholder text
        bottomLabelsLayout.addWidget(self.gcodeFilenameLabel)

        # Add the bottom labels layout to the main layout
        mainLayout.addLayout(bottomLabelsLayout)

        # Create a horizontal layout for the bottom buttons
        bottomButtonsLayout = QHBoxLayout()
        bottomButtonsLayout.setSpacing(10)
        
        self.speedSelectButton = QPushButton('Select Speed', self)
        self.speedSelectButton.clicked.connect(self.showSpeedSelection)
        bottomButtonsLayout.addWidget(self.speedSelectButton)
        
        self.openCameraButton = QPushButton('Open Live Camera', self)
        self.openCameraButton.clicked.connect(self.showLiveCamera)
        bottomButtonsLayout.addWidget(self.openCameraButton)
        
        self.setupLightToggleButton(bottomButtonsLayout)
        
        # Add the bottom buttons layout to the main layout
        mainLayout.addLayout(bottomButtonsLayout)	

        # Create a horizontal layout for the top right buttons
        topRightLayout = QHBoxLayout()
        self.setupLogsPageButton(topRightLayout)  # Add the "Show Error Log" button
        self.setupToolsMenuButton(topRightLayout)  # Add the "Tools" button
        mainLayout.addLayout(topRightLayout)  # Add the top right layout to your main layout

        self.setLayout(mainLayout)

        print("HMI Initialized")

    def setupToolsMenuButton(self, layout):
        # Create the main button that will host the menu
        self.toolsMenuButton = QPushButton('Tools', self)
        layout.addWidget(self.toolsMenuButton)  # Add the button to your layout

        # Create a QMenu
        self.toolsMenu = QMenu(self)
        
        # Add actions to the menu
        self.startVNCAction = QAction('Start VNC', self)
        self.startVNCAction.triggered.connect(self.startVNCInitializer)
        self.toolsMenu.addAction(self.startVNCAction)
        
        self.startSSHAction = QAction('Open Commander', self)
        self.startSSHAction.triggered.connect(self.startBambuHMISSHCommander)
        self.toolsMenu.addAction(self.startSSHAction)

        self.startRIVAction = QAction('Start RIV', self)
        self.startRIVAction.triggered.connect(self.startRIV)
        self.toolsMenu.addAction(self.startRIVAction)
        
        # Attach the menu to the button
        self.toolsMenuButton.setMenu(self.toolsMenu)

    def startVNCInitializer(self):
        # Method to start the hmi_vncinit.py script
        subprocess.Popen(['python', 'functions/hmi_vncinit.py'], shell=False)

    def startBambuHMISSHCommander(self):
        # Method to start the hmi_vncinit.py script
        subprocess.Popen(['python', 'functions/BambuHMI_SSHCommander/main.py'], shell=False)

    def startRIV(self):
        # Method to start the hmi_vncinit.py script
        subprocess.Popen(['python', 'functions/RIV/bhmi_riv-0.1.py'], shell=False)

    def setupLightToggleButton(self, layout):
        # Create a QPushButton for toggling the light
        self.lightToggleButton = QPushButton('Toggle Chamber Light', self)
        self.lightToggleButton.clicked.connect(self.toggleChamberLight)
        layout.addWidget(self.lightToggleButton)  # Add the button to your layout
        self.updateLightToggleButton()  # Update button text based on light state

    def toggleChamberLight(self):
        # Call the APIClient method to toggle the light state
        APIClient.toggle_light('light.x1c_00m09a351100110_chamber_light')
        self.updateLightToggleButton()  # Update the button after toggling the light
        print("Toggled chamber light")

    def updateLightToggleButton(self):
        light_state = APIClient.get_light_state('light.x1c_00m09a351100110_chamber_light')
        if light_state == 'on':
            self.lightToggleButton.setText("Turn Chamber Light Off")
        elif light_state == 'off':
            self.lightToggleButton.setText("Turn Chamber Light On")
        else:
            self.lightToggleButton.setText("Toggle Chamber Light")

    def showSpeedSelection(self):
        self.speedSelectionWindow = SelectionWindow()
        self.speedSelectionWindow.show()

    def showMQTTModePopup(self):
        mqtt_mode = APIClient.get_state('sensor.solidus_printer_mqtt_connection_mode')
        QMessageBox.information(self, "MQTT Connection Mode", f"MQTT Mode: {mqtt_mode}", QMessageBox.Ok)
        print(f"MQTT Mode: {mqtt_mode}")

    def setupEStopButton(self, layout):
        # Create a large Emergency Stop button
        self.eStopButton = QPushButton('E-STOP')
        self.eStopButton.setStyleSheet("QPushButton { background-color: #FF0000; color: #FFFFFF; font-size: 20px; padding: 20px; }")  # Red color for the button, with increased font size and padding for larger appearance
        self.eStopButton.clicked.connect(self.activateEmergencyStop)
        layout.addWidget(self.eStopButton)

    def activateEmergencyStop(self):
        # Function to activate the emergency stop
        print(f"{datetime.now()} !!!EMERGENCY STOP ACTIVATED!!!\n"
              f"Operator has activated the emergency stop. The print will be stopped immediately.")
        APIClient.statePOST('button.x1c_00m09a351100110_stop_printing')  # Assuming APIClient.button.x1c_00m09a351100110_stop_printing is the correct way to call the stop printing function
        QMessageBox.information(self, "Emergency Stop Activated", "The print has been stopped.", QMessageBox.Ok)

    def initRefreshTimer(self):
        self.refreshTimer = QTimer(self)  # Create a QTimer instance
        self.refreshTimer.timeout.connect(self.refresh_status)  # Connect timeout signal to refresh_status
        self.refreshTimer.start(5000)  # Set the timer to call refresh_status every 5000 milliseconds (5 seconds)

    def setupControls(self, layout):
        controlLayout = QHBoxLayout()
        controlLayout.setSpacing(10)
        
        self.status_label = QLabel('Status: Unknown')
        self.status_label.setStyleSheet("QLabel { color: #FFFFFF; }")  # White color for the status label
        controlLayout.addWidget(self.status_label)

        self.print_button = QPushButton('Prepare Printer')
        self.print_button.setStyleSheet("QPushButton { background-color: #28A745; color: #FFF; }")  # Green color for the button
        self.print_button.clicked.connect(self.showPrintChecklistDialog)
        controlLayout.addWidget(self.print_button)
        
        # Resume Print Button
        self.resumePrintButton = QPushButton('Resume Print')
        self.resumePrintButton.setStyleSheet("QPushButton { background-color: #008000; color: #FFF; }")  # Green color for the button
        self.resumePrintButton.clicked.connect(self.resume_print)
        controlLayout.addWidget(self.resumePrintButton)

        # Pause Print Button
        self.pausePrintButton = QPushButton('Pause Print')
        self.pausePrintButton.setStyleSheet("QPushButton { background-color: #FFA500; color: #FFF; }")  # Orange color for the button
        self.pausePrintButton.clicked.connect(self.pause_print)
        controlLayout.addWidget(self.pausePrintButton)
        
        
        
        self.fan_button = QPushButton('RFS')
        self.fan_button.setStyleSheet("QPushButton { background-color: #6c757d; color: #FFF; }")  # Grey color for the button
        self.fan_button.clicked.connect(self.toggle_fan)
        controlLayout.addWidget(self.fan_button)

        self.errorFetchButton = QPushButton('Fetch Errors')
        self.errorFetchButton.setStyleSheet("QPushButton { background-color: #6c757d; color: #FFF; }")  # Grey color for the button
        self.errorFetchButton.clicked.connect(self.fetch_errors)
        #controlLayout.addWidget(self.errorFetchButton)

        self.errorLogButton = QPushButton('HMS Error')
        self.errorLogButton.setStyleSheet("QPushButton { background-color: #6c757d; color: #FFF; }")  # Grey color for the button
        self.errorLogButton.clicked.connect(self.showErrorLog)
        controlLayout.addWidget(self.errorLogButton)

        self.refresh_button = QPushButton('Force Refresh')
        self.refresh_button.setStyleSheet("QPushButton { background-color: #007BFF; color: #FFF; }")  # Blue color for the button
        self.refresh_button.clicked.connect(self.refresh_status)
        controlLayout.addWidget(self.refresh_button)

        layout.addLayout(controlLayout)
        
        self.setupTemperatureDisplays(layout)  # Replace individual temperature display adds with this method call

    def setupTemperatureDisplays(self, layout):
        # Create a horizontal layout for the temperature displays
        tempDisplayLayout = QHBoxLayout()
        tempDisplayLayout.setSpacing(10)

        # Create QLabel for each temperature display and add to the horizontal layout
        self.heatbreak_label = QLabel('Heatbrake: --%')
        tempDisplayLayout.addWidget(self.heatbreak_label)

        self.nozzle_temp_label = QLabel('Nozzle Temp: --°C')
        tempDisplayLayout.addWidget(self.nozzle_temp_label)

        self.plate_temp_label = QLabel('Build Plate Temp: --°C')
        tempDisplayLayout.addWidget(self.plate_temp_label)

        self.chamber_temp = QLabel('Chamber Temp: --°C')
        tempDisplayLayout.addWidget(self.chamber_temp)

        self.chamber_label = QLabel('RFS: --%')
        tempDisplayLayout.addWidget(self.chamber_label)

        # Add the horizontal layout to the main layout
        layout.addLayout(tempDisplayLayout)

    def refresh_status(self):
        refresh_status(self)
    
    def start_print(self):
        start_print(self)

    def runAwayProtect(self):
        runaway_protect()

    def refresh_camera_tokens(self):
        refresh_camera_tokens()

    
    def fetch_errors(self):
        log_text = APIClient.fetchErrors()
        extract_hms_errors(log_text)

    def setupTemperatureGauge(self, layout):
        # Create a QLabel to display the text for the temperature gauge
        self.temperatureGauge = QProgressBar(self)
        self.temperatureGauge.setMaximum(300)  # Assuming 300°C as the maximum temperature for demonstration
        self.temperatureGauge.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk {background-color: white; width: 20px; }")
        layout.addWidget(self.temperatureGauge)

    def setupProgressGauge(self, layout):
        # Create a QLabel to display the text for the progress gauge
        self.progressGaugeLabel = QLabel()
        self.progressGaugeLabel.setStyleSheet("QLabel { color: #FFF; font-size: 12px; }")  # Customize the label appearance
        layout.addWidget(self.progressGaugeLabel)

        # Create a QProgressBar as a simple linear gauge for progress
        self.ProgressGauge = QProgressBar(self)
        self.ProgressGauge.setMaximum(100)
        self.ProgressGauge.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk {background-color: white; width: 20px; }")
        layout.addWidget(self.ProgressGauge)

    def setupGCodeFilenameDisplay(self, layout):
        # Create a QLabel to display the GCode filename
        self.gcodeFilenameLabel = QLabel('GCode Filename: --')
        self.gcodeFilenameLabel.setStyleSheet("QLabel { color: #ADD8E6; font-size: 12px; }")  # Light blue color for the label
        layout.addWidget(self.gcodeFilenameLabel)  # Add the label to the layout
 
    def toggle_fan(self):
        toggle_fan(self)

    def refresh_temperatures(self):
        nozzle_temp = APIClient.get_temperature('sensor.x1c_00m09a351100110_nozzle_temperature')
        plate_temp = APIClient.get_temperature('sensor.x1c_00m09a351100110_bed_temperature')
        heatbrake_speed = APIClient.get_temperature('sensor.x1c_00m09a351100110_heatbreak_fan_speed')
        chamber_temp = APIClient.get_temperature('sensor.x1c_00m09a351100110_chamber_temperature')

        self.heatbreak_label.setText(f"Heatbrake: {heatbrake_speed}%")
        self.nozzle_temp_label.setText(f"Nozzle Temp: {nozzle_temp}°C")
        self.plate_temp_label.setText(f"Build Plate Temp: {plate_temp}°C")
        self.chamber_label.setText(f"RFS: {APIClient.get_temperature('sensor.x1c_00m09a351100110_chamber_fan_speed')}%")
        self.chamber_temp.setText(f"Chamber Temp: {chamber_temp}°C")
        

    def setupTemperatureGraph(self, layout):
        # Replace the existing setupTemperatureGraph method with this
        self.temperatureGraphWebView = QWebEngineView()
        url = "http://homeassistant.local:8123/solidus-printer/0"
        self.temperatureGraphWebView.load(QUrl(url))
        layout.addWidget(self.temperatureGraphWebView)
        self.temperatureGraphWebView.show()

    def setupLogsPageButton(self, layout):
        # Create a QPushButton to change the WebView to the logs page
        self.logsPageButton = QPushButton('View Logs', self)
        self.logsPageButton.clicked.connect(self.showLogsPage)
        layout.addWidget(self.logsPageButton)  # Add the button to your layout

    def showLogsPage(self):
        # Change the WebView to show the logs page
        url = "http://homeassistant.local:8123/config/logs"
        self.temperatureGraphWebView.load(QUrl(url))

    def updateProgressGauge(self):
        self.ProgressGauge.setValue(int(APIClient.get_state('sensor.x1c_00m09a351100110_print_progress')))

    def updateStageLabelAppearance(self, stage):
        # Customize the appearance based on the stage
        if stage == 'printing':
            self.currentStageLabel.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; font-size: 16px; }")
        elif stage == 'paused':
            self.currentStageLabel.setStyleSheet("QLabel { color: #FFEB3B; font-weight: bold; font-size: 16px; }")
        elif stage == 'error':
            self.currentStageLabel.setStyleSheet("QLabel { color: #F44336; font-weight: bold; font-size: 16px; }")
        else:  # Default appearance
            self.currentStageLabel.setStyleSheet("QLabel { color: #9E9E9E; font-weight: normal; font-size: 14px; }")
    
    def showPrintChecklistDialog(self):
        dialog = PrintChecklistDialog(self)
        if dialog.exec_():
            self.start_print()
            print(f"{datetime.now()} Operator has confirmed the print checklist and started the print.")
            # Proceed with starting the print

    def pause_print(self):
        # Call the API client's method to pause the print
        APIClient.statePOST('button.x1c_00m09a351100110_pause_printing')
        QMessageBox.information(self, "Print Paused", "The print has been paused.", QMessageBox.Ok)
        print("Print paused")
    
    def resume_print(self):
        # Adjusted API call to match Home Assistant's expected service call format
        APIClient.statePOST('button.x1c_00m09a351100110_resume_printing')
        QMessageBox.information(self, "Print Resumed", "The print has been resumed.", QMessageBox.Ok)
        print("Print resumed")

    def showErrorLog(self):
        self.errorLogDialog = ErrorLogDialog(self)
        self.errorLogDialog.show()

    def showLiveCamera(self):
        from main_wCamera import LiveCameraView
        self.liveCameraView = LiveCameraView()
        self.liveCameraView.show()
        self.liveCameraView.play()

class PrintChecklistDialog(QDialog):
    def __init__(self, parent=None):
        super(PrintChecklistDialog, self).__init__(parent)
        self.setWindowTitle("Print Checklist")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Checklist items
        self.checklistLabel = QLabel("Please confirm the following before starting the print:")
        self.bedLeveledCheck = QCheckBox("Print bed leveled")
        self.filamentLoadedCheck = QCheckBox("Filament loaded")
        self.nozzleCleanCheck = QCheckBox("Nozzle clean")
        self.chamberTempCheck = QCheckBox("Chamber temperature within 30-45c")
        self.axiswarmupCheck = QCheckBox("Axis warmup gcode run complete")
        self.heaterCheck = QCheckBox("Heater check complete")
        self.coolingCheck = QCheckBox("Cooling fan running")
        
        # Material usage display
        self.materialUsageLabel = QLabel("Estimated Material Usage: --")
        # Assuming you have a method to calculate or retrieve material usage
        # self.materialUsageLabel.setText(f"Estimated Material Usage: {calculateMaterialUsage()}g")
        
        # Start print button
        self.startPrintButton = QPushButton("Printer Prepared")
        self.startPrintButton.clicked.connect(self.on_start_print)
        
        # Adding widgets to the layout
        layout.addWidget(self.checklistLabel)
        layout.addWidget(self.bedLeveledCheck)
        layout.addWidget(self.filamentLoadedCheck)
        layout.addWidget(self.nozzleCleanCheck) 
        layout.addWidget(self.chamberTempCheck)
        layout.addWidget(self.axiswarmupCheck)
        layout.addWidget(self.heaterCheck)
        layout.addWidget(self.coolingCheck)
        layout.addWidget(self.materialUsageLabel)
        layout.addWidget(self.startPrintButton)
        
        self.setLayout(layout)
    
    def on_start_print(self):
        # Check if all checklist items are checked
        if self.bedLeveledCheck.isChecked() and self.filamentLoadedCheck.isChecked() and self.nozzleCleanCheck.isChecked():
            self.accept()  # Close the dialog and proceed
            
            # Save completion timestamp to a text file
            with open('checklist_completion_log.txt', 'a') as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"Checklist completed at: {timestamp}\n")
        else:
            # Show a message or indication that all items must be checked
            QMessageBox.warning(self, "Checklist Incomplete", "Please complete all checklist items before starting the print.")

class ErrorLogDialog(QDialog):
    def __init__(self, parent=None):
        super(ErrorLogDialog, self).__init__(parent)
        self.setWindowTitle("Error Log")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.errorLogLabel = QLabel("Fetching error log...")
        layout.addWidget(self.errorLogLabel)
        
        self.setLayout(layout)
        self.resize(400, 300)  # Adjust size as needed
        self.fetchAndDisplayErrorLog()
    
    def fetchAndDisplayErrorLog(self):
        log_text = extract_hms_errors(APIClient.fetchErrors())
        self.errorLogLabel.setText(log_text)

