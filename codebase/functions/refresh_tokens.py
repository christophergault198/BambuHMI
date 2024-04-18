from functions.fetch_tokens import extract_camera_token
from api_client import APIClient
from config import LIVE_CAMERA_PRINTER_IP

# Initialize a variable to store the last good token outside the function
last_good_token = None

def refresh_camera_tokens():
    global last_good_token  # Use the global keyword to modify the global variable
    update_token = extract_camera_token(APIClient.fetchCameraTokens(f'camera.{LIVE_CAMERA_PRINTER_IP}'))
    if update_token is not None:
        last_good_token = update_token  # Update the last good token if a new one is fetched
    else:
        update_token = last_good_token  # Use the last good token if the new fetch returns None
  #  print(f"Debug: Refresh token updated to: {update_token}")  # Added debug print statement
    return update_token

print(f"{refresh_camera_tokens()}")