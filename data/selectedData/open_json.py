import json

# Open and read the JSON file
with open('selected_PUBMED_title_abstracts_2019_baseline.jsonl', 'r') as file:
    data = json.load(file)

# The content of the JSON file is now stored in 'data'
print(data)

