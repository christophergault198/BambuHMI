import re
from api_client import APIClient
from config import LIVE_CAMERA_PRINTER_IP

def extract_camera_token(log_text):
    # Regular expression to find HMS ERRORS lines
    token_pattern = re.compile(r'"access_token":"([a-f0-9]+)"')
    tokens = token_pattern.findall(log_text)

    last_token = None  # Initialize last_token to store the last found token
    for token in tokens:
        last_token = token  # Update last_token with the current token

    return last_token  # Return the last token found or None if no tokens were found

# Example usage
if __name__ == "__main__":
    # Assuming 'log_text' contains the content from the provided log
    log_text = APIClient.fetchCameraTokens(f'camera.{LIVE_CAMERA_PRINTER_IP}')
    extract_camera_token(log_text)

