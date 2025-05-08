import json

# Specify the path to your JSON file
file_path = "selected_list_processedBook2.json"
# Open and read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
print(data[0])
# Now `data` holds the JSON data as a Python dictionary
word_num = 0

for item in data:
     word_num+= len(item.split(" "))

print(word_num/len(data))
