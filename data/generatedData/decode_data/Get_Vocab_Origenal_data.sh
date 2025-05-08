#!/bin/bash
#SBATCH --account=def-sheridan
#SBATCH --nodes=1
#SBATCH --cpus-per-task=3
#SBATCH --mem=160G
#SBATCH --time=3:00:00
export HF_HOME=/project/def-sheridan
source /project/def-sheridan/paraGenAI/bin/activate
module load StdEnv/2020 gcc python/3.10 cuda/11.4 faiss/1.7.3 arrow

python  clean_data_strategy_remove.py  --inputdata "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/selectedData/selected_list_processedBook2.json" --name "book2-1"
python  clean_data_strategy_remove.py  --inputdata "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/selectedData/selected_PUBMED_title_abstracts_2019_baseline.jsonl" --name "PubMed-1"
python  clean_data_strategy_remove.py  --inputdata "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/selectedData/selected_wiki.json" --name "wiki-1"
python  clean_data_strategy_remove.py  --inputdata "/project/def-sheridan/rachel66/Heaps-Law-In-LLMs-Paper/data/selectedData/selected_HackerNews.json" --name "hn-1"
