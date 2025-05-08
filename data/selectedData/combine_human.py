import pickle
import json

# Load length data
with open('length_combine_data.pkl', 'rb') as file:
    length = pickle.load(file)

# Load initial dataset
with open('AllDataMatch.pkl', 'rb') as file:
    data = pickle.load(file)

# Define the file mappings
map = {
    "book2": "selected_list_processedBook2.json",
    "PubMed": "selected_PUBMED_title_abstracts_2019_baseline.jsonl",
    "wiki": "selected_wiki.json",
    "hn": "selected_HackerNews.json"
}

# Process each file in the map
for i in map:
    min_offset = 0  # Define default min_offset
    if i == "book2":
        min_offset = 9
    elif i == "PubMed":
        min_offset = 7
    elif i == "wiki":
        min_offset = 7
    elif i == "hn":
        min_offset = 8
    
    # Read the corresponding JSON file
    new = []
    with open(map[i], 'rb') as file:
        raw = json.load(file)
    # Process the content
    normal =0
    print(len(raw))
    for index in range(0, 240000, 4):
            new.append(" ".join(raw[index].split()[length[i]["zeroshot"][normal] - min_offset ::]))
            normal+=1
    data[i]["human"] =new

with open('final_dataset.pkl', 'wb') as file:
      pickle.dump(data,file)

