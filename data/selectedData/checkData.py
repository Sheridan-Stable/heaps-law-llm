# Python program to read
# json file

import json

# Opening JSON file
f = open('selected_HackerNews.json')

# returns JSON object as 
# a dictionary
data = json.load(f)
print(data[0])
