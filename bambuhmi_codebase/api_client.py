import requests
from config import HA_URL, HEADERS

class APIClient:
    @staticmethod
    def get_state(entity_id):
        response = requests.get(f'{HA_URL}/api/states/{entity_id}', headers=HEADERS)
        if response.status_code == 200:
            return response.json()['state']
        return "Error"

    @staticmethod
    def toggle_fan(entity_id):
        data = {
            "entity_id": entity_id,
        }
        response = requests.post(f'{HA_URL}/api/services/fan/turn_on', headers=HEADERS, json=data)
        return response.status_code in [200, 201]
    
    @staticmethod
    def set_fan(entity_id, percentage):
        data = {
            "entity_id": entity_id,
            "percentage": percentage
        }
        response = requests.post(f'{HA_URL}/api/services/fan/set_percentage', headers=HEADERS, json=data)
        return response.status_code in [200, 201]
    
    @staticmethod
    def statePOST(entity_id):
        data = {
            "entity_id": entity_id,
        }
        response = requests.post(f'{HA_URL}/api/services/button/press', headers=HEADERS, json=data)
        return response.status_code in [200, 201]
    
    @staticmethod
    def stateSelect(entity_id, option):
        data = {
            "entity_id": entity_id,
            "option": option
        }
        response = requests.post(f'{HA_URL}/api/services/select/select_option', headers=HEADERS, json=data)
        return response.status_code in [200, 201]
    
    @staticmethod
    def get_temperature(entity_id):
        response = requests.get(f'{HA_URL}/api/states/{entity_id}', headers=HEADERS)
        if response.status_code in [200, 201]:
            data = response.json()
            # Extract the 'state' value and convert it to float
            state_float = float(data['state'])
            return state_float
        else:
            return f"Error: {response.status_code}"  # Return more detailed error
        
    @staticmethod
    def fetchErrors():
        response = requests.get(f'{HA_URL}/api/error_log', headers=HEADERS)
        if response.status_code == 200:
            # Directly return the response text without parsing it as JSON
            return response.text
        else:
            # Handle error status code appropriately
            return f"Error: {response.status_code}"
    
    @staticmethod
    def fetchCameraTokens(entity_id):
        response = requests.get(f'{HA_URL}/api/states/{entity_id}', headers=HEADERS)
        if response.status_code == 200:
            # Directly return the response text without parsing it as JSON
            return response.text
        else:
            # Handle error status code appropriately
            return f"Error: {response.status_code}"

    @staticmethod
    def toggle_light(light_id):
        # No data payload is needed for toggling the light on or off
        response = requests.post(f'{HA_URL}/api/services/light/toggle', headers=HEADERS, json={"entity_id": light_id})
        return response.status_code in [200, 201]
        
    @staticmethod
    def get_light_state(light_id):
        response = requests.get(f'{HA_URL}/api/states/{light_id}', headers=HEADERS)
        if response.status_code == 200:
            state_data = response.json()
            return state_data['state']  # This will return 'on' or 'off'
        return None
