# BambuHMI_v2
 Dedicated HMI for Bambu printers running on HA and X1Plus firmware.
# How to use:
First, this is a very rough cut of the software and suite of tools. Currently, as configured nearly the entire codebase is nearly non centralized with a need for global variable file to more easily allow end users to connect their Home Assistant instance and X1C printers.

PreReqs:
1) X1C Printer connected to a HA instance (https://github.com/greghesp/ha-bambulab)
2) X1Plus Firmware installed on your X1C Printer (https://github.com/X1Plus/X1Plus/wiki/Installation-Guide)
3) pyInstaller installed. (pip install pyinstaller)

# Modify the Code (REQUIRED):
Modify the codebase files to match your HA and X1C parameters (IP Address of both HA and Printer, BBLP and Root printer credentials, Changing nearly each file with correct HA sensor/device ID (will be global and simple in very near future).
NOTE: You will need to rebuild with the command "pyinstaller main_wCamera.py --icon geometric.ico"
if you wish to create a an "single" app.

# Upload Commander application .sh files to X1C /usr/bin
Will provide the .sh and .py files responsible for this. Still working on some internal tooling.
