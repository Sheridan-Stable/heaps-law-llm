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



# Ensure WordNet corpus is loaded before threading
wn.ensure_loaded()

class DataProcessing:
    def process(self, data: str):
        pass

class OpenVocab(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(
               self.expand_contractions(
               self.correct_spelling(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data))))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
       data = re.sub(r'[.\']', '', data)
       return re.sub(r'[^\w\s]|', ' ', data).strip()

    def correct_spelling(self, text: str):
        spell = SpellChecker()
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word
                corrected_text[idx] = corrected_word

        return ' '.join(corrected_text)

    def expand_contractions(self, text: str):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class CloseVocab(DataProcessing):
    def process(self, data: str):
        return self.filter_words_in_vocab_database(
               self.split_by_space(
               self.expand_contractions(
               self.correct_spelling(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data)))))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        data = re.sub(r'[.\']', '', data)
        return re.sub(r'[^\w\s]|_', ' ', data).strip()

    def correct_spelling(self, text):
        spell = SpellChecker()
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word
                corrected_text[idx] = corrected_word

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
        directory = 'data/cleandata/'
        file_path = os.path.join(directory, f'{name}.json')

        # Create the directory if it does not exist
        os.makedirs(directory, exist_ok=True)

        # Save the data to the file
        with open(file_path, 'w') as file:
            json.dump(data, file)

        print(f"Data has been saved to {file_path} successfully.")
def loadData(type):
    if type == 1:
        # Assuming 'load_dataset' is from Hugging Face's datasets library
        my_dataset = load_dataset(args.inputdata)
        df = pd.DataFrame(my_dataset['train'])
        # Returning a subset of the data (first 10,000 rows)
        return df[args.choosedata][0:10000]
    elif type == 0:
        # Loading JSON data from a file and converting it to a DataFrame
        with open(args.inputdata, 'r') as json_file:
            data = json.load(json_file)
        # Assuming the JSON data can be converted into a DataFrame directly
        
        df = pd.DataFrame(data, columns=['Entry'])
        return df['Entry']
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the sourse of data')
    parser.add_argument('--inputdata', type=str, help='what is the name of the data')
    parser.add_argument('--choosedata', type=str, help='what is the name of the column?')
    parser.add_argument('--name', type=str, help='choose name for the outputfile')
    args = parser.parse_args()

    data = loadData(args.datasourse)
    cleaner = CleanData(OpenVocab())
    clean_data = cleaner.cleanTheArray(data)
    cleaner.saveData(clean_data,args.name+ "_Open")
    cleaner = CleanData(CloseVocab())
    clean_data = cleaner.cleanTheArray(data)
    cleaner.saveData(clean_data,args.name+ "_Close")



