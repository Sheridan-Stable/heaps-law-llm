import os
import json
from tqdm import tqdm
import re

# def sanitize_filename(filename: str) -> str:
#     """Sanitize the filename by removing invalid characters."""
#     return re.sub(r'[<>:"/\\|?*]', '_', filename)
#
# def process_books_to_dict_and_save(folder_path: str, output_filename: str = 'processedBook3.json'):
#     # Dictionary to hold the processed data
#     books_dict = {}
#
#     # Get list of all .txt files in the epubtxt folder
#     txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
#
#     for txt_file in tqdm(txt_files, desc="Processing books"):
#         file_path = os.path.join(folder_path, txt_file)
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.readlines()
#
#         # Use the sanitized filename without the extension as the key
#         base_filename = sanitize_filename(os.path.splitext(txt_file)[0])
#         books_dict[base_filename] = content
#
#     # Define the path where the dictionary will be saved
#     output_path = os.path.join(folder_path, output_filename)
#
#     # Save the dictionary as a JSON file
#     with open(output_path, 'w', encoding='utf-8') as json_file:
#         json.dump(books_dict, json_file, ensure_ascii=False, indent=4)
#
#     print(f"Processed data saved to {output_path}")
#
# # Example usage:
# process_books_to_dict_and_save('AllData/books1/epubtxt')

import os
import json
from tqdm import tqdm

def combine_json_files(folder_path: str, output_filename: str = 'wikipedia_output.json'):
    combined_data = []

    # Get list of all .json files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    for json_file in tqdm(json_files, desc="Combining JSON files"):
        file_path = os.path.join(folder_path, json_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Ensure the data is a list before extending combined_data
            if isinstance(data, list):
                combined_data.extend(data)
            else:
                print(f"Warning: {json_file} does not contain a list and will be skipped.")

    # Define the path where the combined data will be saved
    output_path = os.path.join("D:\Heaps-Law-In-LLMs-Paper\data\originalData", output_filename)

    # Save the combined list as a JSON file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

    print(f"Combined data saved to {output_path}")

# Example usage:
# combine_json_files('AllData/wikipedia_output-20240729T150327Z-001')

import os
import json
from tqdm import tqdm


def is_text_file(file_path):
    """Attempt to open the file and decode it as UTF-8 text."""
    try:
        with open(file_path, 'rb') as file:
            # Try reading as binary and decode
            raw_data = file.read()
            text_data = raw_data.decode('utf-8')
            return text_data
    except Exception as e:
        # If decoding fails, it's likely not a text file
        print(f"Skipping file {file_path}: {str(e)}")
        return None


def combine_files_to_string_and_save(folder_path: str, output_filename: str = 'HackerNews.json'):
    combined_text = []

    # Get list of all files in the folder
    files = [f for f in os.listdir(folder_path)]

    for file_name in tqdm(files, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)

        text_data = is_text_file(file_path)
        if text_data:
            combined_text.append(text_data)    # Add newline to separate contents of different files


    # Define the path where the combined string will be saved
    output_path = os.path.join(r"E:\Heaps-Law-In-LLMs-Paper\data\originalData\AllData", output_filename)

    # Save the combined string as a JSON file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(combined_text, outfile, ensure_ascii=False, indent=4)

    print(f"Combined text saved to {output_path}")


# Example usage:
combine_files_to_string_and_save(r'E:\Heaps-Law-In-LLMs-Paper\data\originalData\data')
