import csv
import re

# Path to the input file
input_file = 'statistics_11_11_2024_capped_225.txt'
output_file = 'statistics_11_11_2024_capped_225.csv'

# Define a regex pattern to extract the metadata and stats
pattern = re.compile(
    r'(\w+)_([\w\-]+)-([\w\.]+)_([\w]+)_([\w]+)\.json: Mean = ([\d\.]+), s.d = ([\d\.]+), '
    r'Vocab Size = (\d+), Total Words = (\d+), Alpha = ([\d\.]+), Beta = ([\d\.]+), '
    r'Singleton Count = (\d+)'
)

# Alternative pattern for rows with 'human' where 'model size' and 'prompt type' are missing
human_pattern = re.compile(
    r'(\w+)_human_([\w]+)\.json: Mean = ([\d\.]+), s.d = ([\d\.]+), '
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
        else:
            # Check if the line matches the pattern for 'human' rows
            human_match = human_pattern.match(line)
            if human_match:
                # Insert None values for 'model size' and 'prompt type'
                csvwriter.writerow(
                    [human_match.group(1), 'human', None, None, human_match.group(2),
                     human_match.group(3), human_match.group(4), human_match.group(5),
                     human_match.group(6), human_match.group(7), human_match.group(8),
                     human_match.group(9)]
                )

print(f"Data successfully written to {output_file}")

