from PyQt5.QtWidgets import QMessageBox, QInputDialog
from api_client import APIClient

#RFS = Recirculating Filter System
def toggle_fan(self):
    # Display a confirmation dialog
    reply = QMessageBox.question(self, 'Confirm Action', 'Are you sure you want to activate the Recirculating Filter System? This can increase VOC levels in the environment. Only activate if the printer is in a well ventilated area.',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        # User confirmed the action, proceed with asking for the fan speed
        percentage, ok = QInputDialog.getInt(self, "Set RFS Speed", "Enter RFS speed percentage:", min=0, max=100)
        if ok:
            # User entered a value and pressed OK, proceed with setting the fan speed
            APIClient.toggle_fan('fan.x1c_00m09a351100110_chamber_fan')
            APIClient.set_fan('fan.x1c_00m09a351100110_chamber_fan', percentage)

        print(f"Debug: RFS updated to: {percentage}") #Debug
            
    else:
        # User declined the action, do nothing
        pass