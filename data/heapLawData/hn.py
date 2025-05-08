import argparse
import json
import re
import unicodedata
import pandas as pd
import contractions
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn
import tqdm
from multiprocessing import Pool, cpu_count
from datasets import load_dataset
import os
import pickle


# Ensure WordNet corpus is loaded before threading
wn.ensure_loaded()

class DataProcessing:
    def process(self, data: str):
        pass

class OpenVocab(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(
               self.expand_contractions(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data)))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        data = re.sub(r'[.\']', '', data)
        return re.sub(r'[^\w\s]|_', ' ', data).strip()

    def expand_contractions(self, text: str):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class CloseVocab(DataProcessing):
    def process(self, data: str):
        return self.filter_words_in_vocab_database(
               self.split_by_space(
               self.expand_contractions(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data))))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        data = re.sub(r'[.\']', '', data)
        return re.sub(r'[^\w\s]|_', ' ', data).strip()


        return ' '.join(corrected_text)

    def filter_words_in_vocab_database(self, words):
        return [word for word in words if len(wn.synsets(word)) > 0]

    def expand_contractions(self, text):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class SimpleProcessing(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        data = re.sub(r'[.\']', '', data)
        return re.sub(r'[^\w\s]', ' ', data).strip()

    def split_by_space(self, data: str):
        return data.split(" ")

class CleanData:
    def __init__(self, strategy: DataProcessing = None):
        self._strategy = strategy

    def set_strategy(self, strategy: DataProcessing):
        self._strategy = strategy

    def clean(self, data: str):
        if self._strategy:
            return self._strategy.process(data)
        else:
            raise Exception('DataProcessing strategy not set')

    def cleanTheArray(self, data):
        with Pool(cpu_count()) as pool:
            results = list(tqdm.tqdm(pool.imap(self.clean, data), total=len(data)))
        return results

    def saveData(self, data: str, name: str):
        # Define the directory and file path
        directory = 'data/cleandatafinal/'
        file_path = os.path.join(directory, f'{name}.json')
        # Create the directory if it does not exist
        os.makedirs(directory, exist_ok=True)
        # Save the data to the file
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Data has been saved to {file_path} successfully.")
if __name__ == "__main__":

    with open('final_dataset.pkl', 'rb') as file:
          data = pickle.load(file)
    name = "book2"
    for model_name in data[name]:
         if model_name == "human":
            df = pd.DataFrame(data[name]["human"], columns=['Entry'])
#            cleaner = CleanData(OpenVocab())
#            clean_data = cleaner.cleanTheArray(df['Entry'])
#            cleaner.saveData(clean_data,name +"_human"+ "_Open")
            cleaner = CleanData(CloseVocab())
            clean_data = cleaner.cleanTheArray(df['Entry'])
            cleaner.saveData(clean_data,name+"_human"+ "_Close")
#         else:
#            group =data[name][model_name]
#            for prompt_type in data[name][model_name]:
#                df = pd.DataFrame(group[prompt_type], columns=['Entry'])
#                cleaner = CleanData(OpenVocab())
#                clean_data = cleaner.cleanTheArray(df['Entry'])
#                cleaner.saveData(clean_data,name+ "_"+model_name+"_"+prompt_type+ "_Open")
#                cleaner = CleanData(CloseVocab())
#                clean_data = cleaner.cleanTheArray(df['Entry'])
#                cleaner.saveData(clean_data,name+"_" +model_name+"_"+prompt_type+ "_Close")

