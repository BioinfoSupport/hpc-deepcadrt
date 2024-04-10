#!/bin/bash

salloc --time=3:00:00 --partition=shared-gpu --ntasks=1 --gpus-per-task=1 --cpus-per-task=8 --mem=64G

singularity exec --nv --cleanenv --no-home --env PYTHONPATH=/usr/local/lib/ --env MPLCONFIGDIR=/scratch --scratch /scratch --bind $(realpath ~/scratch/) ~/acanas/m-BioinfoSupport/singularity/deepcadrt_latest.sif bash









