#!/bin/bash
#SBATCH --account=def-sheridan
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=30G
#SBATCH --time=12:00:00
export HF_HOME=/project/def-sheridan
source /project/def-sheridan/paraGenAI/bin/activate
module load StdEnv/2020 gcc python/3.10 cuda/11.4 faiss/1.7.3 arrow

python decode.py
