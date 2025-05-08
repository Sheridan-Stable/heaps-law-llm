import os
import pickle
from transformers import GPT2Tokenizer, AutoTokenizer
from tqdm import tqdm

# Define base directory for all subdirectories and corrected dataset folder names
base_directory = "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/generatedData"
dataset_folders = [ "wiki"]
model_identifier_map = {
    "pythia": "EleutherAI/pythia-{param}-deduped",
}

# Target directory to save the final pickle file
output_path = "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/generatedData/decode_data/wiki+_results.pkl"

# Function to load pickle files from a directory
def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

# Function to initialize the correct tokenizer based on model name and parameters
def get_tokenizer(model_name, parameters):
    # Validate the model_name and parameters before proceeding
    if not model_name or not parameters:
        print(f"Skipping initialization for model '{model_name}' with empty parameters.")
        return None

    # Construct the appropriate model path based on the model type
    try:
        if "pythia" in model_name:
            return AutoTokenizer.from_pretrained(
                model_identifier_map["pythia"].format(param=parameters),
                revision="step143000",
                cache_dir=f"./pythia-{parameters}-deduped/step143000"
            )
    except Exception as e:
        print(f"Failed to initialize tokenizer for '{model_name}' with parameters '{parameters}': {e}")
        return None

# Function to decode content using the appropriate tokenizer
def decode_content(tokenizer, encoded_data):
    if tokenizer is not None and isinstance(encoded_data, list):
        return tokenizer.batch_decode(encoded_data, skip_special_tokens=True)
    return []

# Dictionary to store the final decoded results
decoded_results = {}

# Iterate through each dataset folder
for dataset in dataset_folders:
    # Construct the full path to the dataset directory
    dataset_path = os.path.join(base_directory, dataset)
    
    # Check if the dataset directory exists
    if not os.path.exists(dataset_path):
        print(f"Warning: Directory '{dataset_path}' does not exist. Skipping...")
        continue

    # Iterate through each file in the dataset directory
    for file_name in tqdm(os.listdir(dataset_path)):
        file_path = os.path.join(dataset_path, file_name)

        # Check if the file is a pickle file
        if os.path.isfile(file_path):
            # Extract metadata (shot type, model name, parameters) from the file name
            try:
                # Remove ".pkl" extension and split the remaining file name by "-"
                base_name = file_name  # Remove .pkl extension
                # Example format: book2-fewshot-gptneo-125m.pkl -> ["book2", "fewshot", "gptneo", "125m"]
                _, shot_type, model_name, parameters = base_name.split("-")
                
                # Validate extracted values
                if not model_name or not parameters:
                    print(f"Skipping file due to missing model or parameters: {file_name}")
                    continue
            except ValueError:
                print(f"Skipping unrecognized file format: {file_name}")
                continue

            # Initialize tokenizer based on model and parameters
            tokenizer = get_tokenizer(model_name, parameters)
            
            # If tokenizer could not be initialized, skip this file
            if tokenizer is None:
                print(f"Tokenizer initialization failed for '{file_name}'. Skipping...")
                continue

            # Load encoded content from pickle file
            encoded_content = load_pickle(file_path)

            # Decode content using the tokenizer
            decoded_content = decode_content(tokenizer, encoded_content)

            # Store in the decoded_results dictionary with dataset information
            if dataset not in decoded_results:
                decoded_results[dataset] = {}
            model_key = f"{model_name}-{parameters}"
            if model_key not in decoded_results[dataset]:
                decoded_results[dataset][model_key] = {}
            if shot_type not in decoded_results[dataset][model_key]:
                decoded_results[dataset][model_key][shot_type] = []
            decoded_results[dataset][model_key][shot_type].extend(decoded_content)

# Save the final decoded results as a pickle file at the specified path
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "wb") as output_file:
    pickle.dump(decoded_results, output_file)

print(f"Decoding completed and results saved in '{output_path}'")

