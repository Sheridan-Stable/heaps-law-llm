import json
import random
import os
import random


def read_json_or_jsonl(file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    elif file_path.endswith('.jsonl'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return [json.loads(line)['text'] for line in file if 'text' in json.loads(line)]
    else:
        raise ValueError("Unsupported file type. Please provide a '.json' or '.jsonl' file.")


def select_random_items(strings, num_items, seed=None):
    if seed is not None:
        random.seed(seed)

    # Filter strings to only include those with 50 or more words
    long_strings = [s for s in strings if len(s.split()) >= 75]

    if num_items > len(long_strings):
        raise ValueError("num_items cannot be greater than the number of items in the filtered list.")

    return random.sample(long_strings, num_items)


import random


def select_random_items_from_dict(data_dict, num_items, seed=None):
    if seed is not None:
        random.seed(seed)

    selected_book = {}
    keys = list(data_dict.keys())

    for _ in range(num_items):
        selected_items = []
        selected_key = random.choice(keys)  # Randomly select a key

        # Filter strings with 50 or more words
        long_strings = [s for s in data_dict[selected_key] if len(s.split()) >= 75]

        if not long_strings:
            continue  # Skip this key if no strings meet the condition

        for _ in range(4):
            selected_string = random.choice(long_strings)  # Randomly select a string from the filtered list
            while selected_string == '\n':
                selected_string = random.choice(long_strings)
            selected_items.append(selected_string)

        if selected_key in selected_book:
            selected_book[selected_key].extend(selected_items)
        else:
            selected_book[selected_key] = selected_items

    return selected_book


def process_and_save(file_path, num_items, seed=None):
    # Read the input file
    data = read_json_or_jsonl(file_path)

    print(len(data))

    if file_path.endswith('processedBook3.json'):
        # Handle the special case for processedBook3.json
        if not isinstance(data, dict):
            raise ValueError("The content of the processedBook3.json file must be a dictionary to select items from.")

        total_size = 0
        # Iterate through the dictionary and sum the lengths of the lists
        for key, value in data.items():
            total_size += len(value)
        # Print the total size of the lists
        print("Total size of all lists in the dictionary:", total_size)


print("start")
process_and_save('data/originalData/AllData/HackerNews.json', 240000, seed=62643)
print("done")
process_and_save('data/originalData/AllData/wiki.json', 240000, seed=62643)
print("done")
process_and_save('data/originalData/AllData/PUBMED_title_abstracts_2019_baseline.jsonl', 240000, seed=62643)
print("done")
process_and_save('data/originalData/AllData/processedBook3.json', 70000, seed=62643)  # Special case for dictionary
