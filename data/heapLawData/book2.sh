#!/bin/bash
#SBATCH --account=def-sheridan
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=3
#SBATCH --mem=80GB
#SBATCH --time=2:00:00
export HF_HOME=/project/def-sheridan
source /project/def-sheridan/paraGenAI/bin/activate
module load StdEnv/2020 gcc python/3.10 cuda/11.4 faiss/1.7.3 arrow

python book2.py 
