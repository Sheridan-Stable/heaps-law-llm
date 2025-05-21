# A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law

This repository contains computer code for reproducing the results described in the manuscript “A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law” (under review with Computational Linguistics).

## Getting Started

Clone this repository by running the command
```
git clone https://github.com/Sheridan-Stable/heaps-law-llm.git
```

and `cd` into the repository root folder "heaps-law-llm".
```
cd heaps-law-llm
```

## Running Repository Code

Repository code is written in `Python 3.12.4`, you can use any IDE however in this experiment we will use Pycharm. 
After that we install all of the requirements. 

```
pip install -r requirements.txt
```

## Data
Our data are selected from the Pile ([Arxiv preprint](https://arxiv.org/abs/2101.00027)). If you have any questions or would like further information about the dataset, contact the corresponding author.

## Text Emulation
Due to the fact that we will emulating Human author text using different LLMs in a large scale. A pernonal computer will unable to to that task therefore we use Narval with 2 A100 40GB GPU and 100GB RAM from [Digital Research Alliance of Canada](https://ccdb.alliancecan.ca/security/login) to conduct these experiment. However, since every supercomputer enforces its own access policies and environment settings, this guide focuses solely on the Python commands you’ll need and does not include any Narval-specific instructions.


### Preprocessing [Optional]
Because our data come from multiple sources, they arrive in different, non‐uniform formats. In this section, I demonstrate how to convert all inputs into a consistent schema, making downstream processing and analysis much easier. You can skip this step if the data you have is already in an uniform format.

Before  running any of the command please put the data you collect in `/data/originalData/`AllData

```
cd /data/originalData/AllData
python data_combination.py
```

This command is going to give you basic statistic about the data (eg: number of documents, Average length)

```
python data_analysis.py
```

### Emulation

#### Data Selection
Due to the fact that in this experiment, we only use a subset of our data. Therefore we are going to randomize and take a subset which is 240000 documents per dataset.  

```
python choose_data.py
```

#### Create Prompt
In this section, we are going to create prompt for our experiment based on the data we have selected in `/data/originalData/AllData`.
Then we run this command to create prompts.

```
python create_prompt.py  --datasource 'Path to the data source' --name 'Name for the output file' --document_type  'Command to generate prompts'
```

#### Text emulation
After we create the prompt we can process with the text emulation part. 
We created different file for different LLM due to the fact that they set up differently.
We can specify each model differently in the parameter:
--model: Specify which model we want to choose
--input: The file contain the prompts we want to choose from
--output: location of the output file
--start_point: we read the file as an array so the start point will the the specific starting location 
--end_point: end point 
--batch: depend on your hardware it will help youy speed up the generating process however if you dont have a GPU card please set it to 1

Here is one way to set them up however we can change it accordingly.

For Pythia
```
python Pythia.py  --model "EleutherAI/pythia-160m-deduped" --input "/your-dir/few_shot_pubmed.json" --output "/your-dir/Pubmed-few-shot-pythia-160m" --start_point 0 --end_point 60000 --batch 48
```

For GPT-Neo
```
python GPT-Neo.py  --model "EleutherAI/gpt-neo-1.3B" --input "/your-dir/zero_shot_wiki.json" --output "/your-dir/wiki-zero-shot-gptneo-1.3B.json" --start_point 0 --end_point 60000  --batch 32
```

For OPT 
```
python OPT.py  --model "facebook/opt-2.7b" --input "/your-dir/few_shot_pubmed.json" --output "/your-dir/Pubmed-few-shot-opt-2.7b.json" --start_point 0 --end_point 60000 --batch 20
```

## Results
After we are done with the text emulation, we run this script to get all of the required stat 

```
cd \heaps-law-llm\data\generatedData
python cal_data_suf.py
```

## Statistical Analysis
All code is written in R (version 4.4.2). We’ll use RStudio to run everything.
We tell our story in two main parts:
```
1: Folder `tables` contains our Multiple Regression Analysis
2: Folder `figures` contains our plots and visualizations
```

### Multiple Regression Analysis 
```
1: Open the `tables` folder in RStudio
2: Open the `.Rmd` file for the table you want to produce
3: Run each code block (they include detailed instructions)
4: When all chunks finish, your table will appear 
```

### Visualizations 
```
1: Open the `figures` folder in RStudio
2: Open the `.Rmd` file for the figure you want to produce
3: Run each code block (they include detailed instructions)
4: When all chunks finish, your figure will appear
```

## Citation
If you find anything useful please cite our work using:
```
@misc{Lai2025,
  author = {Uyen Lai and Dylan C. P. Lewis and Paul Sheridan and Gurjit S. Randhawa and Aitazaz A. Farooque},
  title = {A Comparative Analysis of Lexical Diversity in Human-Written and Large Language Model-Emulated Text Using Heaps’ Law},
  year = {2025}
}
```
