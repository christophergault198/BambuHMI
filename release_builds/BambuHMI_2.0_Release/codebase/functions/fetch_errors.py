import re
from api_client import APIClient

def extract_hms_errors(log_text):
    # Regular expression to find HMS ERRORS lines
    hms_error_pattern = re.compile(r"HMS ERRORS: \{.*?\}", re.DOTALL)
    errors = hms_error_pattern.findall(log_text)

    for error in errors:
        print(error)
        return (error)

# Example usage
if __name__ == "__main__":
    # Assuming 'log_text' contains the content from the provided log
    log_text = APIClient.fetchErrors()
    extract_hms_errors(log_text)




### Regular Expressions ###

#Works - (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?HMS ERRORS: (\{.*?\})", re.DOTALL)
#Works - (r"HMS ERRORS: \{.*?\}", re.DOTALL)
#Works -"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) WARNING \(.*?\) \[custom_components\.bambu_lab\.pybambu\] HMS ERRORS: (\{.*?\})",  re.DOTALL
#works - r"WARNING \(.*?\) \[custom_components\.bambu_lab\.pybambu\] *?HMS ERRORS: (\{.*?\})", re.DOTALL