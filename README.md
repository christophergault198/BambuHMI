![hmi_interface](https://github.com/christophergault198/BambuHMI/assets/116657484/00042aee-bcd0-4a71-a7ce-912b3d272a31)
# BambuHMI_v2
 Dedicated HMI for Bambu printers running on HA and X1Plus firmware.


PreReqs:
1) X1C Printer connected to a HA instance (https://github.com/greghesp/ha-bambulab)
2) X1Plus Firmware installed on your X1C Printer (https://github.com/X1Plus/X1Plus/wiki/Installation-Guide)
3) pyInstaller installed. (pip install pyinstaller)

# How to use:
1) Launch setup.py and configure the HA and X1C printer settings and credentials.
2) Click 'Save Config' then 'Install Files to Printer'.
3) Optional - Create single app with "pyinstaller main_wCamera.py --icon geometric.ico", be sure to move the fonts & functions folder to the root of the newly built exe.

*Make sure to set static addresses for both your printer and HA instance.
