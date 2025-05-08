import json
import glob
import os
import numpy as np
from datetime import datetime
from scipy.optimize import curve_fit
from collections import Counter
import argparse

def process_json(file_path, p, n):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Flatten the list of lists and create a list for all words
    all_words = [word for sublist in data for word in sublist]
    total_words = len(all_words)
    
    # Calculate the length of each section based on the proportion p
    section_length = int(p * total_words)

    # Determine the step size to equally space the n sections (allowing overlap)
    if n > 1:
        step_size = (total_words - section_length) // (n - 1)
    else:
        step_size = 0

    results = []
    
    # Process text in equally spaced sections
    for i in range(n):
        start_idx = i * step_size
        if start_idx + section_length > total_words:
            break  # Ensure we don't exceed the file length
        section = all_words[start_idx:start_idx + section_length]
        vocab = set(section)
        mean_word_count, std_dev_word_count, word_counts, alpha, beta, num_singletons = process_section(section)
        results.append({
            "start_idx": start_idx,
            "vocab_size": len(vocab),
            "total_words": len(section),
            "mean_word_count": mean_word_count,
            "std_dev_word_count": std_dev_word_count,
            "alpha": alpha,
            "beta": beta,
            "num_singletons": num_singletons
        })
    
    return results

def process_section(section):
    word_frequencies = Counter(section)

    # Calculate statistics for the section
    mean_word_count = np.mean([len(word) for word in section])
    std_dev_word_count = np.std([len(word) for word in section])

    # Identify singletons (words that appear exactly once)
    singletons = [word for word, count in word_frequencies.items() if count == 1]
    num_singletons = len(singletons)

    # Prepare data for alpha-beta calculation
    alpha, beta = alpha_beta(process(section))

    return mean_word_count, std_dev_word_count, len(section), alpha, beta, num_singletons

def process(data):
    newarray = []
    overall_total_words = 0
    overall_unique_words = set()

    for word in data:
        overall_total_words += 1
        overall_unique_words.add(word)
        newarray.append([overall_total_words, len(overall_unique_words)])

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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Process text sections from JSON files.")
    parser.add_argument('-p', type=float, required=True, help="Proportion of text to take for each section (e.g., 0.5 for 50%)")
    parser.add_argument('-n', type=int, required=True, help="Number of sections to take from each file")
    
    args = parser.parse_args()
    p = args.p
    n = args.n

    # Pattern to match all JSON files in the current directory
    json_files = glob.glob('*.json')

    # Store the results for each file
    results = []

    # Get the current date to use in the output file name
    current_date = datetime.now().strftime('%d_%m_%Y')
    output_file = f"statistics_{current_date}.txt"

    # Open the file in append mode
    with open(output_file, 'a') as f:
        for file_path in json_files:
            # Process the JSON and calculate statistics for sections
            sections_stats = process_json(file_path, p, n)
            file_name = os.path.basename(file_path)

            for section_stat in sections_stats:
                # Append results including alpha and beta
                results.append((file_name, section_stat["start_idx"], section_stat["mean_word_count"], section_stat["std_dev_word_count"], 
                                section_stat["vocab_size"], section_stat["total_words"], section_stat["alpha"], section_stat["beta"], section_stat["num_singletons"]))

                # Write the result to the file
                f.write(f"{file_name} (section starting at {section_stat['start_idx']}): "
                        f"Mean = {section_stat['mean_word_count']:.2f}, s.d = {section_stat['std_dev_word_count']:.2f}, "
                        f"Vocab Size = {section_stat['vocab_size']}, Total Words = {section_stat['total_words']}, "
                        f"Alpha = {section_stat['alpha']:.4f}, Beta = {section_stat['beta']:.4f}, Singleton Count = {section_stat['num_singletons']}\n")

    # Print the results (optional, still printing to console)
    for file_name, start_idx, mean, std_dev, vocab_size, total_words, alpha, beta, num_singletons in results:
        print(f"{file_name} (section starting at {start_idx}): Mean = {mean:.2f}, s.d = {std_dev:.2f}, "
              f"Vocab Size = {vocab_size}, Total Words = {total_words}, Alpha = {alpha:.4f}, Beta = {beta:.4f}, Singleton Count = {num_singletons}")

if __name__ == '__main__':
    main()

