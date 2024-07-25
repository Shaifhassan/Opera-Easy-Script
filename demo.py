import json
from src.opera import generate_tc_script

# Load the JSON payload
with open("demo/payload.json", 'r') as file:
    data = json.load(file)

# Generate the file
generate_tc_script(data, "demo/trx_code.json")