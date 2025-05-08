import json
import glob
import os
import numpy as np
from datetime import datetime
from scipy.optimize import curve_fit
from collections import Counter

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    all_words = []

    # Limit each sublist to a maximum of 36 words: 36 words was the mode of the human book2 dataset
    capped_data = [sublist[:36] for sublist in data]

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
    alpha, beta = alpha_beta(process(capped_data))

    return mean_word_count, std_dev_word_count, len(vocab), total_words, word_counts, alpha, beta, num_singletons

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

def alpha_beta(data):
    # Assuming data is a list of (x, y) pairs where x is the index and y is the word count
    x = np.array([pair[0] for pair in data])
    y = np.array([pair[1] for pair in data])

    # Define the power-law function
    def power_law(x, alpha, beta):
        return alpha * np.power(x, beta)

    # Fit the power-law function to the data
    params, _ = curve_fit(power_law, x, y, p0=[1, 1])
    alpha, beta = params
    return alpha, beta

def main():
    # Pattern to match all JSON files in the current directory
    json_files = glob.glob('*.json')

    # Store the results for each file
    results = []

    # Get the current date to use in the output file name
    current_date = datetime.now().strftime('%d_%m_%Y')
    output_file = f"statistics_{current_date}_CAPPED_AT_36_FOR_HUMAN_BOOK2.txt"

    # Open the file in append mode
    with open(output_file, 'a') as f:
        for file_path in json_files:
            # Process the JSON and calculate statistics
            mean, std_dev, vocab_size, total_words, word_counts, alpha, beta, num_singletons = process_json(file_path)
            file_name = os.path.basename(file_path)

            # Append results including alpha and beta
            results.append((file_name, mean, std_dev, vocab_size, total_words, alpha, beta, num_singletons))

            # Write the result to the file
            f.write(f"{file_name}: Mean = {mean:.2f}, s.d = {std_dev:.2f}, Vocab Size = {vocab_size}, "
                    f"Total Words = {total_words}, Alpha = {alpha:.4f}, Beta = {beta:.4f}, Singleton Count = {num_singletons}\n")

    # Print the results (optional, still printing to console)
    for file_name, mean, std_dev, vocab_size, total_words, alpha, beta, num_singletons in results:
        print(f"{file_name}: Mean = {mean:.2f}, s.d = {std_dev:.2f}, Vocab Size = {vocab_size}, "
              f"Total Words = {total_words}, Alpha = {alpha:.4f}, Beta = {beta:.4f}, Singleton Count = {num_singletons}")

if __name__ == '__main__':
    main()
