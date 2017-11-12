import json
from proc_functions import tf_process

with open('app_desc.json', 'r', encoding="utf-8") as infile:
    data = json.load(infile)

processed_text = {}

for name, desc in data.items():
    processed_text[name] = tf_process(desc)


with open("proc_app_desc.json", "w", encoding="utf-8") as outfile:
    json.dump(processed_text, outfile)
