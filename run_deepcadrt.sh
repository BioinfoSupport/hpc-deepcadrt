#!/bin/bash

# Etape 1

# Importer le docker dans baobab pour créer le .sif

singularity pull docker://benjamindn/deepcadrt:v2

# Etape 2

# Copier les datas du nas dans le scratch de baobab pour faire les calculs

cp /acanas/m-BioinfoSupport/tmp/ModelTrainingNotAlignedAwakeAnesthetizedNoOptoStim/*.tif ~/scratch/dataset/ 

# Etape 3

# Allouer la mémoire sur baobab

salloc --time=3:00:00 --partition=shared-gpu --ntasks=1 --gpus-per-task=1 --cpus-per-task=8 --mem=64G

# Etape 4

# Lancer la machine virtuel

singularity exec --nv --cleanenv --no-home --env PYTHONPATH=/usr/local/lib/ --env MPLCONFIGDIR=/scratch --scratch /scratch --bind $(realpath ~/scratch/) ~/deepcadrt_v2.sif bash

cd /srv/beegfs/scratch/users/d/dinolfib/

# Etape 5

# Lancer le train.py

deepcadrt_train.py --datasets_path=datasets_test/ --pth_dir ModelTrainingSmall.out --n_epochs=4 --patch_x=100 --patch_y=100 --patch_t=10

# Etape 6

# Lancer le test.py

deepcadrt_test.py --datasets_path=datasets_test/ --pth_dir ModelTrainingSmall.out --denoise_model=datasets_test_202404081136 --output_dir=Sortie/ --patch_x=100 --patch_y=100 --patch_t=10

# Etape 7

# Copier les résultats obtenu sur le nas

cp ~/scratch/dataset/*.tif /acanas/m-BioinfoSupport/tmp/ModelTrainingNotAlignedAwakeAnesthetizedNoOptoStim/



