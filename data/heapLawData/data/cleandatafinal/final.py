import os
import json
import pickle
from tqdm import tqdm  # For progress bar

def parse_filename(filename):
    """
    Parse the filename to extract metadata.

    Handles two patterns:
    1. Dataset_ModelName-ModelSize_PromptType_Type.json
       Example: PubMed_pythia-410m_fewshot_Close.json

    2. Dataset_human_Type.json (for 'human' model without ModelSize and PromptType)
       Example: PubMed_human_Open.json

    Returns a dictionary with metadata or None if the filename doesn't match expected patterns.
    """
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    parts = name.split('_')

    if len(parts) == 3:
        # Possible 'human' pattern: Dataset_human_Type.json
        dataset, model_name, type_part = parts
        if model_name.lower() == 'human':
            # Assign default values for missing ModelSize and PromptType
            model_size = "unknown"
            prompt_type = "unknown"
            type_ = type_part.lower()  # Ensure consistency (e.g., 'Open' -> 'open')
            return {
                "dataset": dataset,
                "model_name": model_name,
                "model_size": model_size,
                "prompt_type": prompt_type,
                "type": type_
            }
        else:
            print(f"Warning: Filename '{filename}' does not match expected 'human' pattern. Skipping.")
            return None
    elif len(parts) == 4:
        # Regular pattern: Dataset_ModelName-ModelSize_PromptType_Type.json
        dataset, model_part, prompt_type, type_part = parts
        if '-' in model_part:
            model_name, model_size = model_part.split('-', 1)
        else:
            model_name = model_part
            model_size = "unknown"  # Assign 'unknown' if ModelSize is missing

        type_ = type_part.lower()  # Ensure consistency (e.g., 'Close' -> 'close')
        return {
            "dataset": dataset,
            "model_name": model_name,
            "model_size": model_size,
            "prompt_type": prompt_type,
            "type": type_
        }
    else:
        print(f"Warning: Filename '{filename}' does not match expected patterns. Skipping.")
        return None

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
            # Limit word_array to the first 225 words if it exceeds 225 words
            if len(word_array) > 225:
                word_array = word_array[:225]

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
    Main function to aggregate data from JSON files into a nested dictionary structure with a progress bar.
    Handles both regular and 'human' JSON files and saves the output as a Pickle file.
    """
    aggregated_data = {}
    output_filename = 'aggregated_output.pkl'  # Saving as Pickle

    # Check if aggregated_output.pkl exists
    if os.path.exists(output_filename):
        # Load existing aggregated_output.pkl
        try:
            with open(output_filename, 'rb') as f:
                aggregated_data = pickle.load(f)
            print(f"Loaded existing '{output_filename}'.")
        except Exception as e:
            print(f"Error reading '{output_filename}': {e}")
            return
    else:
        print(f"Note: '{output_filename}' does not exist. A new one will be created.")

    # Get a list of all JSON files in the current directory
    json_files = [file for file in os.listdir('.') if file.endswith('.json')]

    if not json_files:
        print("No JSON files found in the current directory.")
        return

    # Initialize the progress bar with the total number of files
    for filename in tqdm(json_files, desc="Processing JSON files", unit="file"):
        metadata = parse_filename(filename)
        if metadata is None:
            continue  # Skip files that don't match the pattern

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

    # Save the aggregated data to a Pickle file
    try:
        with open(output_filename, 'wb') as f_out:
            pickle.dump(aggregated_data, f_out)
        print(f"\nAggregated data has been saved to '{output_filename}'.")
    except Exception as e:
        print(f"Error writing to '{output_filename}': {e}")

if __name__ == "__main__":
    main()

