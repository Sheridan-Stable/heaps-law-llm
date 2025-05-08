import json
import glob
import os
import numpy as np

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Flatten the list of lists and create a set for the vocabulary
    all_words = [word for sublist in data for word in sublist]
    vocab = set(all_words)
    total_words = len(all_words)

    # Calculate the length of each sublist (number of words in each list)
    word_counts = [len(sublist) for sublist in data]
    mean_word_count = np.mean(word_counts)
    std_dev_word_count = np.std(word_counts)

    return mean_word_count, std_dev_word_count, len(vocab), total_words

def main():
    # Pattern to match all JSON files in the current directory
    json_files = glob.glob('*.json')

    # Store the results for each file
    results = []

    for file_path in json_files:
        mean, std_dev, vocab_size, total_words = process_json(file_path)
        file_name = os.path.basename(file_path)
        results.append((file_name, mean, std_dev, vocab_size, total_words))

    # Print the results
    for file_name, mean, std_dev, vocab_size, total_words in results:
        print(f"{file_name}: Mean = {mean:.2f}, s.d = {std_dev:.2f}, Vocab Size = {vocab_size}, Total Words = {total_words}")

if __name__ == '__main__':
    main()

