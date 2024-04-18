from api_client import APIClient
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from config import PRINTER_ID

def stateSpeed(speed):
    if speed == 'standard':
        APIClient.stateSelect(f'select.x1c_{PRINTER_ID}_printing_speed', 'standard')
    elif speed == 'silent':
        APIClient.stateSelect(f'select.x1c_{PRINTER_ID}_printing_speed', 'silent')

class SelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Speed')
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        self.btnStandard = QPushButton('Standard', self)
        self.btnStandard.clicked.connect(lambda: self.selectSpeed('standard'))
        layout.addWidget(self.btnStandard)
        print(f"Debug: stateSpeed: Standard")

        self.btnSilent = QPushButton('Silent', self)
        self.btnSilent.clicked.connect(lambda: self.selectSpeed('silent'))
        layout.addWidget(self.btnSilent)
        print(f"Debug: stateSpeed: Silent")

        self.setLayout(layout)

    def selectSpeed(self, speed):
        print(f"Selected: {speed}")
        stateSpeed(speed)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelectionWindow()
    ex.show()
    sys.exit(app.exec_())
