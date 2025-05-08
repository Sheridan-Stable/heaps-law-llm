import json
import os
import argparse

def json_to_txt(json_file):
    # Check if the input file exists and has a .json extension
    if not os.path.exists(json_file) or not json_file.endswith('.json'):
        print(f"Error: The file '{json_file}' does not exist or is not a JSON file.")
        return
    
    # Read the JSON file
    with open(json_file, 'r') as file:
        try:
            data = json.load(file)  # Parse the JSON data
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from '{json_file}'.")
            return
    
    # Create output filename with .txt extension
    txt_file = f"{os.path.splitext(json_file)[0]}.txt"
    
    # Write the JSON data to the txt file
    with open(txt_file, 'w') as file:
        json.dump(data, file, indent=4)  # Pretty print JSON with indentation
    
    print(f"Successfully converted '{json_file}' to '{txt_file}'.")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert a JSON file to a TXT file with the same name.')
    parser.add_argument('json_file', help='The path to the JSON file that you want to convert.')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function to convert JSON to TXT
    json_to_txt(args.json_file)


# This block ensures the script is being run directly from the command line
if __name__ == "__main__":
    main()

