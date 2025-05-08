import json

# Open and read the JSON file
with open('wiki_gptneo-1.3b_fewshot_Close.json', 'r') as file:
    data = json.load(file)

# Display the data

print(data[0])
