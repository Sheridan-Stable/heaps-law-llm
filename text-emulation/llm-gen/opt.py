import torch
import json
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, OPTForCausalLM
import argparse
import pickle
import os

class VarrianDataset(Dataset):
    def __init__(self, input_ids):
        self.input_ids = input_ids

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx]

class LLMsGeneration:
    def __init__(self, model, tokenizer, device, start_point, end_point, batch_size):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.startPoint = start_point
        self.endPoint = end_point
        self.rawDoc = None
        self.batch_size = batch_size
        self.tokenizer.padding_side = 'left'

    def loadArray(self, file_path, batch_size):
        # Load input data from the provided file path and slice it based on start/end points
        with open(file_path, 'r') as f:
            data = json.load(f)[self.startPoint:self.endPoint]
        
        prompts = data

        # Tokenize the prompts with dynamic padding to reduce unnecessary tokens
        all_input_ids = self.tokenizer(prompts, return_tensors="pt", truncation=True, padding="longest").input_ids
        all_input_ids = all_input_ids.to(self.device)

        # Create a dataset and dataloader
        dataset = VarrianDataset(all_input_ids)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        outputs = []
        
        # Generate text in batches
        for batch_input_ids in dataloader:
            generated = self.model.generate(
                batch_input_ids,
                max_new_tokens=300,
                pad_token_id=self.tokenizer.pad_token_id,
                do_sample=True,
                top_p=0.9,
                temperature=1.0,
                top_k=50
            )
            
            # Collect generated output
            outputs.extend(generated.cpu().numpy())

        # Store the raw generated document
        self.rawDoc = self.decode(outputs)

    def decode(self, data):
        # Decode the generated token ids into human-readable text
        return self.tokenizer.decode(data, skip_special_tokens=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help="Input JSON file path")
    parser.add_argument('--output', type=str, help="Output file path to save generated results")
    parser.add_argument('--model', default=None, type=str, help="Pretrained model path")
    parser.add_argument('--batch', default=8, type=int, help="Batch size for generation")
    parser.add_argument('--start_point', default=0, type=int, help="Start index of the prompts in the input file")
    parser.add_argument('--end_point', default=None, type=int, help="End index of the prompts in the input file")
    args = parser.parse_args()

    # Set the device to GPU if available, otherwise CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the model and tokenizer
    model = OPTForCausalLM.from_pretrained(args.model).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # Set the padding token
    tokenizer.pad_token = tokenizer.eos_token

    # Initialize LLMsGeneration instance
    llms_generation = LLMsGeneration(model, tokenizer, device, args.start_point, args.end_point, args.batch)

    # Load input data and generate text
    llms_generation.loadArray(args.input, args.batch)

    # Define the output directory and ensure it exists
    output_dir = os.path.dirname(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the generated raw data to the output file
    with open(args.output, 'wb') as file:
        pickle.dump(llms_generation.rawDoc, file)

    print("Generation completed and output saved.")

