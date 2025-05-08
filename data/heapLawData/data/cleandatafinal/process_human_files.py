import os
import json
from tqdm import tqdm  # For progress bar

def parse_human_filename(filename):
    """
    Parse the 'human' filename to extract metadata.

    Expected filename format:
    Dataset_human_Type.json
    Example: PubMed_human_Open.json
    """
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    parts = name.split('_')

    if len(parts) != 3:
        print(f"Warning: Filename '{filename}' does not match the expected 'human' pattern. Skipping.")
        return None

    dataset = parts[0]
    model_name = parts[1]
    type_part = parts[2]

    # Assign default values for missing fields
    model_size = "unknown"
    prompt_type = "unknown"

    type_ = type_part.capitalize()  # Ensure consistency (e.g., 'open' -> 'Open')

    return {
        "dataset": dataset,
        "model_name": model_name,
        "model_size": model_size,
        "prompt_type": prompt_type,
        "type": type_
    }

def process(data):
    """
    Process the data to create newarray which contains cumulative total words
    and unique vocabulary size.

    Parameters:
    - data: List[List[str]] - A list where each item is a list of words.

    Returns:
    - newarray: List[List[int, int]] - Each sublist contains [total_words_so_far, vocab_size_so_far]
    """
    newarray = []
    overall_total_words = 0
    overall_unique_words = set()

    for idx, word_array in enumerate(data):
        if word_array is not None and isinstance(word_array, list):
            # Update total words
            overall_total_words += len(word_array)
            # Update unique vocabulary
            for word in word_array:
                if isinstance(word, str):
                    overall_unique_words.add(word)
                else:
                    print(f"Warning: Non-string word at index {idx}. Skipping this word.")

            # Append the current state to newarray
            newarray.append([overall_total_words, len(overall_unique_words)])
        else:
            print(f"Warning: Expected a list of words at index {idx}, but got {type(word_array)}. Skipping this item.")

    return newarray

def insert_into_nested_dict(nested_dict, keys, data):
    """
    Insert data into a nested dictionary based on the provided keys.

    Parameters:
    - nested_dict: dict - The dictionary to insert data into.
    - keys: list - A list of keys representing the path in the nested dictionary.
    - data: list - The newarray to insert at the deepest level.

    Example:
    insert_into_nested_dict(d, ['PubMed', 'human', 'unknown', 'unknown', 'Open'], [[100, 50], [200, 80]])
    """
    current_level = nested_dict
    for key in keys[:-1]:
        if key not in current_level:
            current_level[key] = {}
        current_level = current_level[key]

    type_key = keys[-1]
    if type_key not in current_level:
        current_level[type_key] = []

    # Append the newarray to the list under the specific type
    current_level[type_key].append(data)

def main():
    """
    Main function to process 'human' JSON files and update aggregated_output.json.
    """
    aggregated_output_filename = 'aggregated_output.json'

    # Check if aggregated_output.json exists
    if not os.path.exists(aggregated_output_filename):
        print(f"Error: '{aggregated_output_filename}' does not exist. Please run the main aggregation script first.")
        return

    # Load the existing aggregated_output.json
    try:
        with open(aggregated_output_filename, 'r', encoding='utf-8') as f:
            aggregated_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading '{aggregated_output_filename}': {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading '{aggregated_output_filename}': {e}")
        return

    # Identify all 'human' JSON files
    human_json_files = [file for file in os.listdir('.') if file.endswith('.json') and '_human_' not in file and '_human' in file]

    if not human_json_files:
        print("No 'human' JSON files found to process.")
        return

    # Process each 'human' JSON file with a progress bar
    for filename in tqdm(human_json_files, desc="Processing 'human' JSON files", unit="file"):
        metadata = parse_human_filename(filename)
        if metadata is None:
            continue  # Skip files that don't match the 'human' pattern

        # Read JSON content
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Expecting a list of lists of words
        except json.JSONDecodeError as e:
            print(f"Error reading '{filename}': {e}")
            continue
        except Exception as e:
            print(f"Unexpected error reading '{filename}': {e}")
            continue

        # Ensure the JSON content is a list
        if not isinstance(data, list):
            print(f"Warning: The content of '{filename}' is not a list. Skipping.")
            continue

        # Process the data to create newarray
        newarray = process(data)

        # Prepare the path in the nested dictionary
        keys = [
            metadata["dataset"],
            metadata["model_name"],
            metadata["model_size"],
            metadata["prompt_type"],
            metadata["type"]
        ]

        # Insert the newarray into the nested dictionary
        insert_into_nested_dict(aggregated_data, keys, newarray)

    # Save the updated aggregated data back to aggregated_output.json
    try:
        with open(aggregated_output_filename, 'w', encoding='utf-8') as f_out:
            json.dump(aggregated_data, f_out, indent=2)
        print(f"\n'aggregated_output.json' has been successfully updated with 'human' data.")
    except Exception as e:
        print(f"Error writing to '{aggregated_output_filename}': {e}")

if __name__ == "__main__":
    main()

