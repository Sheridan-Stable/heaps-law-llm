import json
import glob
import os
import numpy as np
from datetime import datetime
from scipy.optimize import curve_fit
from collections import Counter
import random
import csv
import os
import re
from tqdm import tqdm

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    random.shuffle(data)

    all_words = []

    # Limit each sublist to a maximum of 300 words
    capped_data = [sublist[:225] for sublist in data]

    # Flatten the list of lists after capping
    all_words = [word for sublist in capped_data for word in sublist]

    vocab = set(all_words)
    total_words = len(all_words)

    # Calculate the length of each sublist (number of words in each list)
    word_counts = [len(sublist) for sublist in capped_data]
    mean_word_count = np.mean(word_counts)
    std_dev_word_count = np.std(word_counts)

    # Count occurrences of each word
    word_frequencies = Counter(all_words)

    # Identify singletons (words that appear exactly once)
    singletons = [word for word, count in word_frequencies.items() if count == 1]
    num_singletons = len(singletons)

    # Prepare data for alpha-beta calculation
    alpha, beta,r = alpha_beta(process(capped_data))

    return mean_word_count, std_dev_word_count, len(vocab), total_words, word_counts, alpha, beta, num_singletons,r

def process(data):

    newarray = []
    overall_total_words = 0
    overall_unique_words = set()

    for word_array in data:
        if word_array is not None:  # Ensure the entry is not None

            overall_total_words += len(word_array)
            overall_unique_words.update(word_array)
            newarray.append([overall_total_words,len(overall_unique_words)])

    return newarray
import numpy as np
from scipy.optimize import curve_fit

def alpha_beta(data):
    # Assuming data is a list of (x, y) pairs where x is the index and y is the word count
    x = np.array([pair[0] for pair in data], dtype=float)
    y = np.array([pair[1] for pair in data], dtype=float)

    # Define the power-law function
    def power_law(x, alpha, beta):
        return alpha * np.power(x, beta)

    # Fit the power-law function to the data
    params, _ = curve_fit(power_law, x, y, p0=[1, 1])
    alpha, beta = params

    # Compute fitted values
    y_pred = power_law(x, alpha, beta)

    # Compute R^2 value
    ss_res = np.sum((y - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)   
    return alpha, beta, r_squared

def main():
    # Pattern to match all JSON files in the current directory
	json_files = glob.glob('*.json')
#        json_files = glob.glob('*_human_*.json')
    # Store the results for each file
	results = []
	# Define the CSV column headers
	csv_headers = [
	    "file_name",  # Keeping file name for reference
	    "corpus",
	    "model_name",
	    "model_size",
	    "prompt",
	    "vocab",
	    "mean",
	    "s.d",
	    "vocab_size",
	    "total_words",
	    "alpha",
	    "beta",
	    "singleton_count",
            "r"
	]

	# Regular expression pattern for parsing filenames
	filename_pattern = re.compile(
	    r'^(?P<corpus>[^_]+)_'                   # Corpus: PubMed or hn
	    r'(?P<model_name>[^-_]+)'                # Model Name: human or pythia
	    r'(?:-'                                  # Start optional group for non-human models
	    r'(?P<model_size>[\d\.]+[bBmM])_'        # Model Size: 2.8b
	    r'(?P<prompt>[^_]+)_'                    # Prompt Type: fewshot
	    r')?'                                    # End optional group
	    r'(?P<vocab>[^\.]+)\.json$'              # Vocab Setting: Open or Close
	)

	output_file = f"heap_law_data_fix.csv"

	# Define fixed seeds for reproducibility
	fixed_seeds = [42, 123, 999]  # These seeds ensure the same shuffling each time

	# Open the CSV file in append mode (outside the loop)
	with open(output_file, 'a', newline='') as f:
	    writer = csv.writer(f)

	    # Write the header only if the file is empty
	    if os.stat(output_file).st_size == 0:
	        writer.writerow(csv_headers)

	    for file_path in tqdm(json_files):
	        file_name = os.path.basename(file_path)

	        for i in range(3):  # Three different shuffled versions per file
	            seed = fixed_seeds[i]  # Use a pre-defined seed for reproducibility
	            random.seed(seed)  # Set the seed before shuffling

	            # Extract components from the filename
	            match = filename_pattern.match(file_name)
	            if match:
	                corpus = match.group("corpus").lower()
	                model_name = match.group("model_name").lower()
	                model_size = match.group("model_size").lower() if match.group("model_size") else None
	                prompt = match.group("prompt").lower() if match.group("prompt") else None
	                vocab = match.group("vocab").lower()
	            else:
	                corpus, model_name, model_size, prompt, vocab = None, None, None, None, None

	            # Process the JSON and calculate statistics with the shuffled data
	            mean, std_dev, vocab_size, total_words, word_counts, alpha, beta, singleton_count, r = process_json(file_path)

	            # Debugging print statement to confirm iteration and seed used

	            # Append results including the seed used
	            results.append((file_name.lower(), corpus, model_name, model_size, prompt, vocab,
	                            mean, std_dev, vocab_size, total_words, alpha, beta, singleton_count, r))

	            # Write the result to the CSV file (convert all string values to lowercase, keep missing as None)
	            writer.writerow([
	                file_name.lower(), corpus, model_name, model_size, prompt, vocab,
	                mean, std_dev, vocab_size, total_words,
	                alpha, beta, singleton_count, r
	            ])

if __name__ == '__main__':
    main()
