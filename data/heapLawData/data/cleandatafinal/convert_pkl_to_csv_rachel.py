import pandas as pd
import numpy as np
import pickle

# Load the data from the pickle file
with open('heap_law_data_fix.pkl', 'rb') as f:
    data = pickle.load(f)

def process_entry(entry, label_info):
    # Access the inner list of pairs if entry is a nested list
    # Instead of checking len(entry), check len(seed_data)
    # because seed_data likely contains the list of pairs
    if isinstance(entry, dict) and len(entry) > 0 and isinstance(list(entry.values())[0], list):
        seed_data = list(entry.values())[0]  # Access the list of pairs
        # Ensure we have exactly 60000 pairs in seed_data
        assert len(seed_data) == 60000, f"Expected 60000 pairs, got {len(seed_data)}"

        # Extract first and second values
        first_values = [pair[0] for pair in seed_data]
        second_values = [pair[1] for pair in seed_data]

        # Combine first and second values for the final row
        combined_values = first_values + second_values
        return label_info + combined_values
    else:
        # Handle cases where entry is not a dictionary or doesn't contain the expected structure
        print(f"Unexpected entry format: {entry}")  # You might want to handle this differently

# List to collect all processed rows
processed_data = []

# Iterate through the dictionary structure
for dataset in data.keys():  # E.g., 'wiki', 'book2', 'PubMed', 'hn'
    for model_type, model_data in data[dataset].items():  # E.g., 'pythia', 'gptneo', 'opt', 'human'
        for model_size, prompt_data in model_data.items():  # E.g., '1.4b', '125m', etc.
            for prompt_type, vocab_data in prompt_data.items():  # E.g., 'fewshot', 'oneshot', etc.
                for vocab_type, entry in vocab_data.items():  # E.g., 'open', 'close'
                    for seed, seed_data in entry.items():  # E.g., '1', '2', etc.
                        # Create label information for the row
                        label_info = [dataset, model_type, model_size, prompt_type, vocab_type, seed]
                        # Process and append the row
                        processed_data.append(process_entry(entry, label_info))

# Convert to DataFrame
column_labels = ['dataset', 'model_type', 'model_size', 'prompt_type', 'vocab_type', 'seed'] + \
                [f'value_{i}' for i in range(1, 120001)]
final_df = pd.DataFrame(processed_data, columns=column_labels)
# Save DataFrame to CSV
final_df.to_csv('/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/heapLawData/data/cleandatafinal/heap_law_data_fix_rachel.csv', index=False)
