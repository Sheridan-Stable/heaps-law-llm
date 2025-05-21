import argparse
import json
import random
from transformers import GPT2Tokenizer
from abc import ABC, abstractmethod
import os
import tqdm

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


# Function to choose randomly from the data
def select_random_elements(array, k):
    if len(array) < k:
        return "Array does not contain enough elements"
    return random.sample(array, k)


class PromptStrategy(ABC):
    @abstractmethod
    def generate_prompt_array(self, prompts, document_type, length):
        pass

    def save_prompt(self, prompt, file_name):
        # Extract the directory name from the file_name
        name_data = file_name.split("_")[2]
        # Ensure the directory exists
        dir_path = os.path.abspath(f"project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/prompt/{name_data}")
        os.makedirs(dir_path, exist_ok=True)
        # Create a full file path (with a filename, not just a directory)
        file_path = os.path.join(dir_path, f"{file_name}.json")
        # Save the prompt to the file
        with open(file_path, 'w') as file:
            json.dump(prompt, file, indent=4)
        print(f"Prompt saved to {file_path}")


class ZeroShot(PromptStrategy):

    def generate_prompt_array(self, prompts, document_type, length):
        prompt_list = prompts[0:60000]
        zero_shot = []
        for i in tqdm.tqdm(range(len(prompt_list))):
            token_prompt = divide_data(length, prompt_list[i])
            zero_shot_prompt = f"Please complete the unfinished {document_type}. {token_prompt[0]} =>"
            zero_shot.append(zero_shot_prompt)
        return zero_shot


class OneShot(PromptStrategy):

    def generate_prompt_array(self, prompts, document_type, length):
        one_shot_prompts = []
        one_shot_example = prompts[60000:120000]
        prompt_list = prompts[0:60000]
        for i in tqdm.tqdm(range(len(prompt_list))):
            example = divide_data(length, one_shot_example[i])
            prompt = divide_data(length, prompt_list[i])
            one_shot_prompts.append(
                f"The following is an excerpt from a(n) {document_type}, followed by a completion of that excerpt. Please complete the unfinished {document_type} excerpt. {example[0]} => {example[1]} .{prompt[0]} =>")
        return one_shot_prompts


class FewShot(PromptStrategy):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    def generate_prompt_array(self, prompts, document_type, length):
        few_shot_prompts = []
        few_shot_example = prompts[60000::]
        prompt_list = prompts[0:60000]
        number_of_example = 3
        starting_point = 0
        end_point = 3
        for i in tqdm.tqdm(range(len(prompt_list))):
            example = ""
            for j in range(starting_point, end_point):
                ex = divide_data(50, few_shot_example[j])
                example += f"{ex[0]} => {ex[1]}. "
            starting_point += number_of_example
            end_point += number_of_example
            prompt = divide_data(length, prompt_list[i])
            few_shot_prompts.append(
                f"The following is an excerpt from a(n) {document_type}, followed by a completion of that excerpt. Please complete the unfinished {document_type} excerpt. {example} .{prompt[0]} =>")
        return few_shot_prompts


class PromptContext:
    def __init__(self, strategy: PromptStrategy):
        self.strategy = strategy

    def generate_prompt_array(self, prompts, document_type, length):
        return self.strategy.generate_prompt_array(prompts, document_type, length)

    def save_strategy_output(self, prompt, file_name):
        return self.strategy.save_prompt(prompt, file_name)


def LoadData(file_path):
    with open(file_path, 'r') as file:
        h = json.load(file)
        print(len(h))
        return h


def divide_data(number_of_token, prompt):
    token_ids = tokenizer.encode(" ".join(prompt.split()))
    prompt_text = tokenizer.decode(token_ids[:number_of_token])
    example_text = tokenizer.decode(token_ids[number_of_token:200])
    return [prompt_text, example_text]


def generate_all_prompt(prompts, name, document_type, length):
    strategies = [ZeroShot(), OneShot(), FewShot()]
    # strategies = [FewShot()]
    # strategy_names = [ "few_shot_"]
    strategy_names = ["zero_shot_", "one_shot_", "few_shot_"]

    for strategy, strategy_name in zip(strategies, strategy_names):
        context = PromptContext(strategy=strategy)
        generated_prompts = context.generate_prompt_array(prompts, document_type, length)
        context.save_strategy_output(generated_prompts, strategy_name + name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate prompts based on different strategies")
    parser.add_argument('--datasource', type=str, required=True, help='Path to the data source')
    parser.add_argument('--name', type=str, required=True, help='Name for the output file')
    parser.add_argument('--document_type', type=str, required=True, help='Command to generate prompts')

    args = parser.parse_args()

    prompt_data = LoadData(args.datasource)

    generate_all_prompt(prompt_data, args.name, args.document_type, 50)
