import json
from proc_functions import process


with open('app_desc.json', 'r') as myfile:
    data = json.load(myfile)

processed_text = {}

for name,desc in data.items():
    processed_text[name] = process(desc)


with open("proc_app_desc.json", "w", encoding = "utf-8") as file:
    json.dump(processed_text, file)
