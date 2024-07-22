import json

with open("payload.json",'r') as file:
    content = json.load(file)


print(content)