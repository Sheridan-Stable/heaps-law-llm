# A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law

This repository contains computer code for reproducing the results described in the manuscript “A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law” (under review with [Computational Linguistics](https://direct.mit.edu/coli)).

## Getting Started

Clone this repository by running the command
```
git clone https://github.com/Sheridan-Stable/heaps-law-llm.git
```
and `cd` into the repository root folder `heaps-law-llm`.

## Human-Written Text

We selected corpora from the Pile ([Arxiv preprint](https://arxiv.org/abs/2101.00027)) for emulation: Wikipedia, PubMed Abstracts, BookCorpus2, and Hacker News. As the Pile is no longer supported, feel free to contact the corresponding author for more information on obtaining the corpora. After obtaining the corpora, save them in the folder `heaps-law-llm\text-emulation\processing-data\original-data\all-data`.

## Text Emulation

Text emulation code is written in Python `3.12.4`.  Run the following command to install all of the required libraries: 
```
pip install -r requirements.txt
```
We used Narval with 2 A100 40GB GPU and 100GB RAM from [Digital Research Alliance of Canada](https://ccdb.alliancecan.ca/security/login) to emulate human-authored text using different LLMs on a large scale. However, since every system enforces its own access policies and environment settings, this guide focuses solely on the Python commands you’ll need and does not include any Narval-specific instructions.

### Preprocessing

The raw human-written text that we used was subject to nonuniform formats. To convert all textual data into a consistent schema, `cd` into the `/text-emulation/original-data/all-data` folder and run the command:
```
python data-combination.py
```

This command is will give basic statistic about each corpus (e.g.,: number of documents, and average document length):
```
python data-analysis.py
```

### Data Selection

We only use a subset of corpus documents in our experiments. Run this command to randomly select a subset of 240,000 documents from each corpus:
```
python choose-data.py
```

### Prompt Creation

To create prompts for our experiment based on the data we have selected in `/data/text-emulation/all-data`, run the command:
```
python create-prompt.py  --datasource 'Path to the data source' --name 'Name for the output file' --document-type  'Command to generate prompts'
```

### Emulation

After creating the prompts we can proceed with the text emulation. We created different file for different LLM due to the fact that they set up differently.
We can specify each model differently in the parameter:
```
--model: Specify which model we want to choose
--input: The file contain the prompts we want to choose from
--output: location of the output file
--start_point: we read the file as an array so the start point will the the specific starting location 
--end_point: end point 
--batch: depend on your hardware it will help youy speed up the generating process however if you dont have a GPU card please set it to 1
```

Here is one way to set them up however we can change it accordingly.

For Pythia:
```
python pythia.py  --model "EleutherAI/pythia-160m-deduped" --input "/your-dir/few_shot_pubmed.json" --output "/your-dir/Pubmed-few-shot-pythia-160m" --start_point 0 --end_point 60000 --batch 48
```

For GPT-Neo:
```
python gpt-neo.py  --model "EleutherAI/gpt-neo-1.3B" --input "/your-dir/zero_shot_wiki.json" --output "/your-dir/wiki-zero-shot-gptneo-1.3B.json" --start_point 0 --end_point 60000  --batch 32
```

For OPT:
```
python opt.py  --model "facebook/opt-2.7b" --input "/your-dir/few_shot_pubmed.json" --output "/your-dir/Pubmed-few-shot-opt-2.7b.json" --start_point 0 --end_point 60000 --batch 20
```

### Calculation of Basic Numerical Statistics 

After emulating the text, `cd` into the `\heaps-law-llm\text-emulation\generated-data` folder and run this script to some statistics required for our various numerical analyses:
```
python cal-data-suf.py
```

For the PCA we need a different type of data. To obtain it, `cd` into the `cd \heaps-law-llm\text-emulation\generated-data` folder and run the command:
```
python cal-data-pca-suf.py
```

## Statistical Analysis

All code is written in R version `4.4.2`. We’ll use RStudio to run everything.
We tell our story in two main parts:
```
1: Folder `tables` contains our Multiple Regression Analysis
2: Folder `figures` contains our plots and visualizations
```

### Multiple Regression Analysis Tables

Here is a general procedure for reproducing the multiple linear regression analysis tables:

1. Navigate to the `tables` subfolder of interest
2. Open the `.Rmd` file for the table you want to produce
3. Run each code block (they include detailed instructions)
4. When all chunks finish, the table will appear 


### Figures

Here is a general procedure for reproducing selected manuscript figures:

1. Navigate to the `figures` subfolder of interest
2. Open the `.Rmd` file for the figure you want to produce
3. Run each code block (they include detailed instructions)
4. When all chunks finish, your figure will appear

## Citation

If you find anything useful please cite our work using:
```
@misc{Lai2025,
  author = {Uyen Lai and Dylan C. P. Lewis and Paul Sheridan and Gurjit S. Randhawa and Aitazaz A. Farooque},
  title = {A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law},
  year = {2025}
}
```
