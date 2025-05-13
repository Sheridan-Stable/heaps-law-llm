import torch
import json
from torch.utils.data import Dataset, DataLoader
from transformers import GPTNeoXForCausalLM, AutoTokenizer
import argparse
import pickle
import os
import json

class VarrianDataset(Dataset):
    def __init__(self, input_ids):
        self.input_ids = input_ids

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx]

class LLMsGeneration:
    def __init__(self, model, tokenizer, device, start_point, end_point,batch_size):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.startPoint = start_point
        self.endPoint = end_point
        self.rawDoc = None
        self.batch_size  = batch_size
        self.tokenizer.padding_side = 'left'

    def loadArray(self, file_path,batch_size):
        with open(file_path, 'r') as f:
            data = json.load(f)[self.startPoint:self.endPoint]

        prompts = data

        all_input_ids = self.tokenizer(prompts, return_tensors="pt", truncation=True, padding="max_length", max_length=854).input_ids
        all_input_ids = all_input_ids.to(self.device)

        dataset = VarrianDataset(all_input_ids)
        dataloader = DataLoader(dataset, batch_size = batch_size, shuffle=False)
        outputs = []
        max_position_embeddings = self.model.config.max_position_embeddings

        for batch_input_ids in dataloader:
            generated = self.model.generate(batch_input_ids,
                                            max_new_tokens = 300,
                                            pad_token_id=self.tokenizer.pad_token_id,
                                            do_sample=True,  # Enable sampling
                                            top_p=0.9,  # Use nucleus sampling (top-p)
                                            temperature=1,  # Increase temperature for more randomness
                                            top_k=50
                                                     )

            outputs.extend(generated.cpu().numpy())

        self.rawDoc = self.decode(outputs)

    def decode(self, data):
        return self.tokenizer.decode(data, skip_special_tokens=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type = str)
    parser.add_argument('--output',type=str)
    parser.add_argument('--model', default=None, type=str)
    parser.add_argument('--batch', default=None, type=int)
    parser.add_argument('--start_point', default=None, type=int)
    parser.add_argument('--end_point', default=None, type=int)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize model and tokenizer
    #model = GPTNeoForCausalLM.from_pretrained(args.model).to(device)
    #tokenizer = GPT2Tokenizer.from_pretrained(args.model)
    model_name = args.model.split("/")[1]
    model = GPTNeoXForCausalLM.from_pretrained(
      args.model,
      revision="step143000",
      cache_dir=f"./{model_name}/step143000",
      ).to(device)
    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
                args.model,
                revision="step143000",
                cache_dir=f"./{model_name}/step143000",
                )

    # Set padding token
    tokenizer.pad_token = tokenizer.eos_token

    # Initialize LLMsGeneration instance
    llms_generation = LLMsGeneration(model, tokenizer, device, args.start_point, args.end_point,args.batch)

    # Load array and generate text
    llms_generation.loadArray(args.input,args.batch)

    # Define the output directory and file path
    output_dir = os.path.dirname(args.output)

    # Create the directory if it does not exist
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    with open(args.output, 'wb') as file:
        pickle.dump(llms_generation.rawDoc, file)
    print("done")
