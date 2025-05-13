# Heaps-Law-In-LLMs-Paper

[intro]

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

Repository code is written in Python 3.12.4 in Pycharm IDE. 

## Data
Our data are selected from the Pile <https://arxiv.org/abs/2101.00027>.  If you have any questions or would like further information about the dataset or our methodology, please email us at Paul Sheridan <paul.sheridan.stats@gmail.com>.

## Text Emulation
Due to the fact that we will emulating Human author text using different LLMs in a large scale. A pernonal computer will unable to to that task therefore we use Narval from Digital Research Alliance of Canada <https://ccdb.alliancecan.ca/security/login> to conduct these experiment. However, since every supercomputer enforces its own access policies and environment settings, this guide focuses solely on the Python commands you’ll need and does not include any Narval-specific instructions.


### Preprocessing [Optional]
Because our data come from multiple sources, they arrive in different, non‐uniform formats. In this section, I demonstrate how to convert all inputs into a consistent schema, making downstream processing and analysis much easier. You can skip this step if the data you have is already in an uniform format.

Before  running any of the command please put the data you collect in /data/originalData/AllData

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
In this section, we are going to create prompt for our experiment based on the data we have selected in /data/originalData/AllData.
Then we run this command to create prompts.

```
python create_prompt.py  --datasource 'Path to the data source' --name 'Name for the output file' --document_type  'Command to generate prompts'
```


## Results

### Statistical Analysis




## Figures
Under the Figures folder, are the code which is written in R we used to create these figures for our paper. 


