
# Print the data
import json

# Open and read the JSON file
with open('book2_Open.json', 'r') as file:
    data = json.load(file)
print(data[0])
# Flatten the list of lists and create a set to get the unique words (vocabulary)
vocab = set(word for sublist in data for word in sublist)

# Print the vocabulary
print(len(vocab))

