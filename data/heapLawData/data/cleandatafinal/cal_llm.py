import json
import glob
import os
import numpy as np
from datetime import datetime
from scipy.optimize import curve_fit
from collections import Counter
import random
import csv
import os
import re
import numpy as np
from sklearn.metrics import jaccard_score
import numpy as np
from sklearn.metrics import jaccard_score
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='PubMed', help='data to paraphrase')
args = parser.parse_args()

def main():
	json_files = glob.glob('*_Open.json')

	# Regular expression pattern for parsing filenames
	filename_pattern = re.compile(
	    r'^(?P<corpus>[^_]+)_'                   # Corpus: PubMed or hn
	    r'(?P<model_name>[^-_]+)'                # Model Name: human or pythia
	    r'(?:-'                                  # Start optional group for non-human models
	    r'(?P<model_size>[\d\.]+[bBmM])_'        # Model Size: 2.8b
	    r'(?P<prompt>[^_]+)_'                    # Prompt Type: fewshot
	    r')?'                                    # End optional group
	    r'(?P<vocab>[^\.]+)\.json$'              # Vocab Setting: Open or Close
	)
	list1=[]
	list2=[]
	# Open the CSV file in append mode (outside the loop)
	for file_path in json_files:
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

	            with open(file_path, 'r') as f:
	                   data_json = json.load(f)
	            if model_name != "human":
	             if corpus == args.dataset:
                           for i in data_json:
                               for j in i:
                                 list1.append(j)
	             else:
	                  for i in data_json:
	                      for j in i:
	                         list2.append(j)
	print(len(list1))
	print(jaccard_similarity(list1, list2))
def jaccard_similarity(list1, list2):
    print(len(list1))
    set1 = set(list1)
    set2 = set(list2)
    
    # If both are empty, define similarity as 1
    if not set1 and not set2:
        return 1.0
    
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union)

if __name__ == '__main__':
    main()
