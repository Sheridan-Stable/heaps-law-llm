import os
import re
import glob
import json
import random
import pickle
from tqdm import tqdm

def process_json(file_path):
    # Load JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Shuffle the data
    random.shuffle(data)
    # Limit each sublist to a maximum of 225 words
    capped_data = [sublist[:225] for sublist in data]
    # Process the data to compute cumulative and unique word counts
    processed_data = process(capped_data)
    return processed_data

def process(data):
    newarray = []
    overall_total_words = 0
    overall_unique_words = set()
    for word_array in data:
        if word_array is not None:  # Ensure the entry is not None
            overall_total_words += len(word_array)
            overall_unique_words.update(word_array)
            newarray.append([overall_total_words, len(overall_unique_words)])
    return newarray

def main():
    # Get all JSON files in the current directory
    json_files = glob.glob('*.json')
    
    # Regular expression pattern for parsing filenames.
    # Expected filename format:
    # <corpus>_<model_name>[-<model_size>_<prompt>_]<vocab>.json
    filename_pattern = re.compile(
        r'^(?P<corpus>[^_]+)_'                   # Corpus: e.g. PubMed or hn
        r'(?P<model_name>[^-_]+)'                 # Model Name: e.g. human or pythia
        r'(?:-'                                  # Start optional group for non-human models
        r'(?P<model_size>[\d\.]+[bBmM])_'         # Model Size: e.g. 2.8b
        r'(?P<prompt>[^_]+)_'                     # Prompt Type: e.g. fewshot
        r')?'                                    # End optional group
        r'(?P<vocab>[^\.]+)\.json$'              # Vocab Setting: e.g. open or close
    )
    
    # Define fixed seeds for reproducibility
    fixed_seeds = [42, 123, 999]
    result = {}
    
    # Process each JSON file
    for file_path in tqdm(json_files, desc="Processing JSON files"):
        file_name = os.path.basename(file_path)
        match = filename_pattern.match(file_name)
        if match:
            corpus = match.group("corpus").lower()
            model_name = match.group("model_name").lower()
            model_size = match.group("model_size").lower() if match.group("model_size") else None
            prompt = match.group("prompt").lower() if match.group("prompt") else None
            vocab = match.group("vocab").lower()
        else:
            corpus, model_name, model_size, prompt, vocab = None, None, None, None, None
        
        # Loop over each fixed seed
        for seed in fixed_seeds:
            random.seed(seed)  # Set the seed before shuffling
            heap_law_data = process_json(file_path)
            
            # Create nested dictionary structure if keys do not exist
            if corpus not in result:
                result[corpus] = {}
            if model_name not in result[corpus]:
                result[corpus][model_name] = {}
            if model_size not in result[corpus][model_name]:
                result[corpus][model_name][model_size] = {}
            if prompt not in result[corpus][model_name][model_size]:
                result[corpus][model_name][model_size][prompt] = {}
            if vocab not in result[corpus][model_name][model_size][prompt]:
                result[corpus][model_name][model_size][prompt][vocab] = {}
            
            result[corpus][model_name][model_size][prompt][vocab][seed] = heap_law_data
            
    # Save the final result as a pickle file
    with open("heap_law_data_fix.pkl", "wb") as pkl_file:
        pickle.dump(result, pkl_file)

if __name__ == '__main__':
    main()
