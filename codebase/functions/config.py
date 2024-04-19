# Home Assistant URL and Token
#Remember to set static IP addresses for the printer and the HA instance.

HA_URL = 'http://192.168.9.62:8123' #Changeme
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzYjBjYWZkNTU3MjI0MDA5OTkxMzg2M2E5MWJiNDVmMSIsImlhdCI6MTcwODYxODkyMiwiZXhwIjoyMDIzOTc4OTIyfQ.JbQGxBKqyhwZX3BcjfOmbOQms_y9H1E8syT4_ZB5eqM' #Changeme
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
}

# Printer Credentials
PRINTER_IP = '192.168.9.78' #Changeme
PRINTER_USERNAME = 'root'
PRINTER_PASSWORD = 'a8d11ef407b8' #Changeme

# Home Assistant Printer Identifyer
PRINTER_ID = '00m09a351100110' #Changeme
HA_FRIENDLY_NAME = 'solidus_printer' #ex. Solidus Printer = solidus_printer

#Live Camera Printer Identifyer
LIVE_CAMERA_PRINTER_IP = '192_168_9_78' #Changeme (Printer IP. Keep the formatting, keep the '_'s)

# Home Assistant Web Views
PRINTER_HA_WEB_VIEW = f'{HA_URL}/solidus-printer/0' #Changeme Change the HA UI URL
LOGS_HA_WEB_VIEW = f'{HA_URL}/config/logs'


