import json

# Function to read a JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to write data to a JSON file
def write_json(data, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)  # indent=4 for pretty formatting

# Example usage
data5 = read_json('wikipedia_output/wikipedia-en-0.json')
data1 = read_json('wikipedia_output/wikipedia-en-1.json')
data2 = read_json('wikipedia_output/wikipedia-en-2.json')
data3 = read_json('wikipedia_output/wikipedia-en-3.json')
data4 = read_json('wikipedia_output/wikipedia-en-4.json')

write_json(data1+data2+data3+data4+data5, 'wiki.json')
