# Heaps-Law-In-LLMs-Paper

[intro]

## Getting Started

Clone this repository by running the command
```
git clone [link]
```
and `cd` into the repository root folder [name].

## Running Repository Code

Repository code is written in Python 3.12.4 in Pycharm IDE. 
## Data

### The Pile

The Pile is not currently available publicly now. However it can be found 
[magnet:?xt=urn:btih:0d366035664fdf51cfbe9f733953ba325776e667&dn=EleutherAI_ThePile_v1]

### Common Stopwords

We compiled a list of 989 English stopwords by pooling stopwords from

- The nltk 3.8.1 Python library (179 stopwords)
- The Terrier IR Platform (733 stopwords, [download page](https://www.kaggle.com/datasets/rowhitswami/stopwords?resource=download "Kaggle: All English Stopwords (700+)")) stored locally at `genia/0-raw-data/terrier-stopwords.txt` 
- MyISAM (543 stopwords, [download page](https://dev.mysql.com/doc/refman/8.0/en/fulltext-stopwords.html "12.9.4 Full-Text Stopwords: Stopwords for MyISAM Search Indexes")) stored locally at `genia/0-raw-data/myisam-stopwords.txt` 

The subset of 417 (out of 989) stopwords occurring in the GENIA data is used in an exploratory analysis described below. No preprocessing is required.

## GENIA Data Numerical Experiments

### IDF vs. ICF Plot

Run the `genia/2-figure/figure-1-script.ipynb` notebook to generate the plot of Figure 1 from the manuscript.

### Term Burstiness Score Evaluation

To reproduce performance evaluation results from Table 4 from the manuscript:
1. Run the `genia/3-keybert/keybert-scores.ipynb` notebook to generate KeyBERT term scores. Scores are output to the `genia/3-keybert/keybert-scores.json` JSON file.
2. Run the `genia/3-burstiness-evaluation/burstiness-evaluation.ipynb` notebook to generate the Church Gale (CG), Irvine and Callison-Burch (ICB), Derivation of Proportions (DOP), Chi-square test, and Resicual ICF (RICF) term burstiness scores. Data used for the table is output to the `genia/3-main-results` folder.

### Stopwords Exploratory Analysis

Run the `genia/3-burstiness-evaluation/burstiness-evaluation.ipynb` notebook to reproduce the results of the stopwords analysis in Tables 5 and 6 from the manuscript. Data used for the tables is output to the `genia/3-main-results` folder.

## Citation
If you find anything useful please cite our work using:
```
@misc{SarriaHurtado2023,
  author = {Samuel Sarria Hurtado and Todd Mullen and Taku Onodera and Paul Sheridan},
  title = {A Statistical Significance Testing Approach for Measuring Term Burstiness with Applications to Domain-Specific Terminology Extraction},
  year = {2023},
  eprint = {arXiv:2310.15790}
}
```
