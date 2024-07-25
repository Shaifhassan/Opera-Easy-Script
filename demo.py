import json
from opera_tc_codes import generate

# Load the JSON payload
with open("payload.json", 'r') as file:
    data = json.load(file)

# Generate the file
generate(data)