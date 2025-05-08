import csv
import re

# Path to the input file
input_file = 'statistics_10_13_2024.txt'
output_file = 'statistics_10_13_2024.txt'

# Updated regex pattern to handle the new format (ignores text between ".json" and "Mean")
pattern = re.compile(
    r'(\w+)_([\w\-]+)-([\w\.]+)_([\w]+)_([\w]+)\.json.*?Mean = ([\d\.]+), s.d = ([\d\.]+), '
    r'Vocab Size = (\d+), Total Words = (\d+), Alpha = ([\d\.]+), Beta = ([\d\.]+), '
    r'Singleton Count = (\d+)'
)

# Open the input file and output CSV
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as csvfile:
    # Define the CSV writer and write the header
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['dataset', 'model', 'model size', 'prompt type', 'vocab type', 'mean', 
                        's.d.', 'vocab size', 'total words', 'alpha', 'beta', 'singleton count'])
    
    # Process each line in the input file
    for line in infile:
        match = pattern.match(line)
        if match:
            # Extract groups and write to CSV
            csvwriter.writerow(match.groups())

print(f"Data successfully written to {output_file}")

