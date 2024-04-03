

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Container building process 
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Build the container
docker build -t unigebsp/deepcadrt --platform=linux/amd64 container/

# Push the container to dockerhub
docker push unigebsp/deepcadrt

# On baobab
singularity pull docker://unigebsp/deepcadrt

#-#-#-#-#-#-#-#-#-#-#
# Usage on Baobab
#-#-#-#-#-#-#-#-#-#-#

# Connect to HPC yggdrasil or baobab
ssh prados@baobab2.hpc.unige.ch
ssh prados@login1.yggdrasil.hpc.unige.ch

# Mount NASAC on the login node
ps -u prados | awk '$4=="dbus-daemon"{print $1}' | xargs kill
dbus-launch bash
gio mount 'smb://ISIS;prados@nasac-m2.unige.ch/m-GHoltmaat'

# Copy TIF files from NASAC to scratch
rsync -av \
  --no-perms \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/ModelTrainingNotAlignedAwakeAnesthetizedNoOptoStim \
  ~/scratch/

# Ask Baobab for a GPU node
salloc --time=3:00:00 --partition=shared-gpu --ntasks=1 --gpus-per-task=1 --cpus-per-task=8 --mem=64G

# Run the container on the GPU node
singularity exec --nv \
  --cleanenv --no-home \
  --env PYTHONPATH=/usr/local/lib/ \
  --env MPLCONFIGDIR=/scratch \
  --scratch /scratch \
  --bind $(realpath ~/scratch/) \
  /acanas/m-BioinfoSupport/singularity/deepcadrt_latest.sif bash


cd /srv/beegfs/scratch/users/p/prados
./deepcadrt_train.py --datasets_path=ModelTrainingSmall/ --pth_dir ModelTrainingSmall.out --n_epochs=2 --patch_x=100 --patch_y=100 --patch_t=10


# Run DeepCadRT
sbatch --time=12:00:00 --partition=shared-gpu --ntasks=1 --gpus-per-task=1 --cpus-per-task=8 --mem=64G <<EOF
#!/bin/bash

EOF







# Run the container on a local machine with GPU
docker run --gpus=all --rm -v 'D:\docker\datasets\:/DeepCAD-RT/DeepCAD_RT_pytorch/notebooks/datasets/' -p 8888:8888 unigebsp/deepcadrt

docker run --rm -it unigebsp/deepcadrt bash


docker run --rm -p 8888:8888 unigebsp/deepcadrt


