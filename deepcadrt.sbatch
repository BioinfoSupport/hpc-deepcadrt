#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --partition=shared-gpu
#SBATCH --time=3:00:00
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8 
#SBATCH --mem=64G

set -x

echo $(realpath ~/scratch/)
echo $(realpath ./) 

singularity exec --nv \
  --cleanenv \
  --no-home \
  --env PYTHONPATH=/usr/local/lib/ \
  --env MPLCONFIGDIR=/scratch \
  --scratch /scratch \
  --bind $(realpath ~/scratch/) \
  --pwd $(realpath ./) \
  /acanas/m-BioinfoSupport/singularity/deepcadrt_v2.sif $@



