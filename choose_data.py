import json
import random
import os


def read_json_or_jsonl(file_path):
    """
    Reads a JSON or JSONL file and returns the parsed content.

    Args:
        file_path (str): The path to the JSON or JSONL file.

    Returns:
        list or dict: Parsed JSON data from the file.
    """
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    elif file_path.endswith('.jsonl'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return [json.loads(line)['text'] for line in file if 'text' in json.loads(line)]
    else:
        raise ValueError("Unsupported file type. Please provide a '.json' or '.jsonl' file.")


import random

def select_random_items(strings, num_items, seed=None):
    """
    Randomly selects unique items from a list of strings that have 50 or more words.

    Args:
        strings (list of str): The list of strings to select from.
        num_items (int): The number of items to select.
        seed (int, optional): The random seed for reproducibility.

    Returns:
        list of str: A list of randomly selected unique items with 50 or more words.
    """
    if seed is not None:
        random.seed(seed)

    # Filter strings to only include those with 50 or more words
    long_strings = [s for s in strings if len(s.split()) >= 75]

    if num_items > len(long_strings):
        raise ValueError("num_items cannot be greater than the number of items in the filtered list.")

    return random.sample(long_strings, num_items)


import random

def select_random_items_from_dict(data_dict, num_items, seed=None):
    """
    Randomly selects keys from a dictionary and then randomly selects an item from the list associated with each key,
    ensuring that only items with 50 or more words are selected.

    Args:
        data_dict (dict): The dictionary where each key is associated with a list of strings.
        num_items (int): The number of items to select.
        seed (int, optional): The random seed for reproducibility.

    Returns:
        dict: A dictionary with selected keys and their corresponding selected strings.
    """
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
    """
    Reads a JSON or JSONL file, selects random items, and saves the result to a new JSON file.

    Args:
        file_path (str): The path to the JSON or JSONL file.
        num_items (int): The number of items to select.
        seed (int, optional): The random seed for reproducibility.
    """
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

        # Select random items from the dictionary
#        selected_items = select_random_items_from_dict(data, num_items, seed)
#    else:
        # General case: Check if data is a list, because only a list can be sampled
#        if not isinstance(data, list):
#            raise ValueError("The content of the file must be a list to select items from.")

        # Select random items
#        selected_items = select_random_items(data, num_items, seed)
#        print(len(selected_items))

    # Prepare the output file name
#    base_name = os.path.basename(file_path)
#    output_file_name = f"selected_{base_name}"

    # Save the selected items to a new JSON file
#    with open(output_file_name, 'w', encoding='utf-8') as output_file:
#        json.dump(selected_items, output_file, indent=4)

#    print(f"Selected items have been saved to {output_file_name}")

print("start")
#process_and_save('data/originalData/AllData/HackerNews.json', 240000, seed=62643)
#print("done")
#process_and_save('data/originalData/AllData/wiki.json', 240000, seed=62643)
#print("done")
#process_and_save('data/originalData/AllData/PUBMED_title_abstracts_2019_baseline.jsonl', 240000, seed=62643)
#print("done")
process_and_save('data/originalData/AllData/processedBook3.json', 70000, seed=62643)  # Special case for dictionary
