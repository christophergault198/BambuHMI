# RIV
RIV is a remote image viewer for Bambu Labs X1C running HA. It's used for taking photos at each layer using the toolhead camera to create amazing timelapses.

PreReqs:
1) X1C Printer connected to a HA instance (https://github.com/greghesp/ha-bambulab)
2) X1Plus Firmware installed on your X1C Printer (https://github.com/X1Plus/X1Plus/wiki/Installation-Guide)

# How to use:
1) Use pip to install the necessary dependencies from the requirements.txt file - `pip install -r requirements.txt`
2) Open config.py configure the HA and X1C printer settings and credentials.
3) Open Bambu Studio, and under the Printer Settings -> Machine G-Code -> Layer Change g-code, paste the g-code from the `slicer_machine_LayerChange_modGcode.txt` file
4) Launch the script - `python bhmi_riv-0.1.py`


*Make sure to set static addresses for both your printer and HA instance.
