import os
import csv
import re

# Define the input text files
input_files = [
#    "statistics_07_01_2025.txt",
#    "statistics_07_01_2025_1.txt",
#    "statistics_07_01_2025_2.txt"
"statistics_24_01_2025_human.txt"
]

# Define the output CSV file
output_csv = "combined_statistics_human.csv"

# Define the CSV column headers
csv_headers = [
    "Dataset",
    "Model",
    "Model Size",
    "Prompt Type",
    "Vocab Setting",
    "Mean",
    "s.d",
    "Vocab Size",
    "Total Words",
    "Alpha",
    "Beta",
    "Singleton Count"
]

# Initialize a list to hold all rows
combined_data = []

# Regular expression patterns
#filename_pattern = re.compile(
#    r'^(?P<dataset>[^_]+)_'          # Dataset: hn
#    r'(?P<model>[^-_]+)-'            # Model: pythia
#    r'(?P<model_size>[\d\.]+[bBmM])_'# Model Size: 2.8b
#    r'(?P<prompt_type>[^_]+)_'       # Prompt Type: fewshot
#    r'(?P<vocab_setting>[^\.]+)\.json$' # Vocab Setting: Close.json
#)

# Regular expression patterns
filename_pattern = re.compile(
    r'^(?P<dataset>[^_]+)_'                     # Dataset: PubMed
    r'(?P<model>[^-_]+)'                        # Model: human or pythia
    r'(?:-'                                    # Start optional group for non-human models
    r'(?P<model_size>[\d\.]+[bBmM])_'          # Model Size: 2.8b
    r'(?P<prompt_type>[^_]+)_'                 # Prompt Type: fewshot
    r')?'                                      # End optional group
    r'(?P<vocab_setting>[^\.]+)\.json$'        # Vocab Setting: Open
)


stats_pattern = re.compile(
    r'Mean\s*=\s*(?P<Mean>[\d\.]+),\s*'
    r's\.d\s*=\s*(?P<s_d>[\d\.]+),\s*'
    r'Vocab\s+Size\s*=\s*(?P<Vocab_Size>\d+),\s*'
    r'Total\s+Words\s*=\s*(?P<Total_Words>\d+),\s*'
    r'Alpha\s*=\s*(?P<Alpha>[\d\.]+),\s*'
    r'Beta\s*=\s*(?P<Beta>[\d\.]+),\s*'
    r'Singleton\s+Count\s*=\s*(?P<Singleton_Count>\d+)'
)

# Function to parse a single line
def parse_line(line):
    try:
        # Split the line into filename and statistics
        filename_part, stats_part = line.strip().split(":", 1)
        
        # Match the filename pattern
        filename_match = filename_pattern.match(filename_part)
        if not filename_match:
            print(f"Filename format incorrect: {filename_part}")
            return None
        
        # Extract filename components
        dataset = filename_match.group("dataset")
        model = filename_match.group("model")
        model_size = filename_match.group("model_size")
        prompt_type = filename_match.group("prompt_type")
        vocab_setting = filename_match.group("vocab_setting")
        
        # Match the statistics pattern
        stats_match = stats_pattern.search(stats_part)
        if not stats_match:
            print(f"Statistics format incorrect: {stats_part}")
            return None
        
        # Extract statistics
        mean = stats_match.group("Mean")
        s_d = stats_match.group("s_d")
        vocab_size = stats_match.group("Vocab_Size")
        total_words = stats_match.group("Total_Words")
        alpha = stats_match.group("Alpha")
        beta = stats_match.group("Beta")
        singleton_count = stats_match.group("Singleton_Count")
        
        # Create a dictionary for the row
        row = {
            "Dataset": dataset,
            "Model": model,
            "Model Size": model_size,
            "Prompt Type": prompt_type,
            "Vocab Setting": vocab_setting,
            "Mean": mean,
            "s.d": s_d,
            "Vocab Size": vocab_size,
            "Total Words": total_words,
            "Alpha": alpha,
            "Beta": beta,
            "Singleton Count": singleton_count
        }
        
        return row
    
    except ValueError as ve:
        print(f"Line split error: {line}")
        return None
    except Exception as e:
        print(f"Unexpected error parsing line: {line}\nError: {e}")
        return None

# Process each input file
for file in input_files:
    if not os.path.exists(file):
        print(f"File {file} does not exist. Skipping.")
        continue
    
    with open(file, 'r', encoding='utf-8') as infile:
        for line_number, line in enumerate(infile, start=1):
            if line.strip() == "":
                # Skip empty lines
                continue
            parsed_row = parse_line(line)
            if parsed_row:
                combined_data.append(parsed_row)
            else:
                print(f"Failed to parse line {line_number} in file {file}.")

# Write the combined data to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(combined_data)

print(f"\nAll data has been combined into {output_csv} successfully!")

