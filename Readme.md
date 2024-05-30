
# hpc-deepcadrt
[DeepCAD-RT](https://github.com/cabooster/DeepCAD-RT) is a tool to denoise timelapse imaging data.
This repository contains code and instructions to run the tool on the HPC cluster of the University of Geneva.


# Instructions

### 1. Create a folder on the NAS with the following structure

* `Model_trial/`
  - `Train/`
  - `Test/`
  - [`deepcadrt.sbatch`] (https://github.com/BioinfoSupport/hpc-deepcadrt/blob/main/deepcadrt.sbatch) # Found in repository root folder, edit if necessary
  - [`Tif_2_tif.py`] (https://github.com/BioinfoSupport/hpc-deepcadrt/blob/main/Tif_2_tif.py) # Optional: if you encounter problems with your tif files. Found in repository root folder. Help at the bottom of the page.


### 2. Connect the HPC cluster

> [!WARNING]
> In the following commands, replace 'unige_id' with your personal login identifier

* Either by opening a terminal on your machine and connect via SSH (either Baobab or Yggdrasil):
```bash
ssh 'unige_id'@baobab2.hpc.unige.ch
ssh 'unige_id'@login1.yggdrasil.hpc.unige.ch
```

* Or by connecting to http://ondemand.baobab.hpc.unige.ch/


### 3. Mount NAS on the login node (do it once)
```bash
ps -u $USER | awk '$4=="dbus-daemon"{print $1}' | xargs kill
dbus-launch bash
gio mount "smb://ISIS;$USER@nasac-m2.unige.ch/m-GHoltmaat"
```


### 4. Synchrnonise NAS folder ('.tif' files for training and testing)
```bash
rsync -av \
  --no-perms \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/Model_trial \
  ~/scratch/
```


### 5. Run the training step
```bash
cd ~/scratch/Model_trial
sbatch deepcadrt.sbatch deepcadrt_train.py \
  --n_epochs=2 --patch_x=100 --patch_y=100 --patch_t=10 \
  --datasets_path=Train \
  --pth_dir=Model.out
```


**optional arguments:**
```
  -h, --help            show this help message and exit
  --overlap_factor OVERLAP_FACTOR
                        Overlap factor (Default=0.4)
  --datasets_path DATASETS_PATH
                        Folder containing files for training (required)
  --n_epochs N_EPOCHS   Number of training epochs (Default=5)
  --fmap FMAP           Model complexity (Default=16)
  --output_dir OUTPUT_DIR
                        Output directory (Default='./results')
  --pth_dir PTH_DIR     The path for pth file and result images (required)
  --onnx_dir ONNX_DIR   Directory onnx model (Default='./onnx')
  --batch_size BATCH_SIZE
                        Batch size (Default=1)
  --patch_t PATCH_T     The time dimension (frames) of 3D patches (Default=150)
  --patch_x PATCH_X     The width of 3D patches (Default=150)
  --patch_y PATCH_Y     The height of 3D patches (Default=150)
  --gap_y GAP_Y         (Default=60)
  --gap_x GAP_X         (Default=60)
  --gap_t GAP_T         (Default=6)
  --lr LR               Learning rate (Default=0.00005)
  --b1 B1               Adam: bata1 (Default=0.5)
  --b2 B2               Adam: bata2 (Default=0.999)
  --GPU GPU             GPU index (Default=0)
  --ngpu NGPU           ngpu (Default=1)
  --num_workers NUM_WORKERS
                        if you use Windows system, set this to 0. (Default=8)
  --scale_factor SCALE_FACTOR
                        The factor for image intensity scaling (Default=1)
  --train_datasets_size TRAIN_DATASETS_SIZE
                        Datasets size for training (how many 3D patches) (Default=3000)
  --select_img_num SELECT_IMG_NUM
                        Select the number of frames used for training (Default=1000000)
  --test_datasize TEST_DATASIZE
                        test data size (Default=400)
  --visualize_images_per_epoch
                        Whether to show result images after each epoch (Default=False)
  --save_test_images_per_epoch
                        Whether to save result images after each epoch (Default=False)
  --colab_display COLAB_DISPLAY
                        colab display (Default=False)
  --result_display RESULT_DISPLAY
                        result display (Default='')
```


### 6. Run the testing step

> [!WARNING]
> In the following commands, replace 'training_number' with the correct training number

```bash
cd ~/scratch/Model_trial
sbatch deepcadrt.sbatch deepcadrt_test.py \
  --patch_x=100 --patch_y=100 --patch_t=10 \
  --datasets_path=Test \
  --pth_dir=Model.out \
  --output_dir=Test.out \
  --denoise_model=datasets_test_'training_number'
```

**optional arguments:**
```
  -h, --help            show this help message and exit
  --overlap_factor OVERLAP_FACTOR
                        The overlap factor between two adjacent patches (Default=0.6)
  --datasets_path DATASETS_PATH
                        Dataset path (required)
  --fmap FMAP           The number of feature maps (Default=16)
  --output_dir OUTPUT_DIR
                        Result file root path (required)
  --pth_dir PTH_DIR     The path file root path (required)
  --batch_size BATCH_SIZE
                        Batch size (Default=1)
  --patch_t PATCH_T     The time dimension (frames) of 3D patches (Default=150)
  --patch_x PATCH_X     The width of 3D patches (Default=150)
  --patch_y PATCH_Y     The height of 3D patches (Default=150)
  --gap_y GAP_Y         (Default=40)
  --gap_x GAP_X         (Default=40)
  --gap_t GAP_T         (Default=4)
  --GPU GPU             the index of GPU you will use for computation (Default=0)
  --ngpu NGPU           ngpu (Default=1)
  --num_workers NUM_WORKERS
                        if you use Windows system, set this to 0.(Default=4)
  --scale_factor SCALE_FACTOR
                        The factor for image intensity scaling (Default=1)
  --test_datasize TEST_DATASIZE
                        the number of frames to be tested (test all frames if the number exceeds the total number of frames in a .tif file (Default=1000000)
  --denoise_model DENOISE_MODEL
                        Denoise model (required)
  --visualize_images_per_epoch
                        Whether to show result images after each epoch (Default=False)
  --colab_display COLAB_DISPLAY
                        colab display (Default=False)
  --result_display RESULT_DISPLAY
                        result display (Default='')
```

### 7. Copy the trained model back to the NAS
```bash
rsync -av \
  --no-perms \
  ~/scratch/Model_trial/*.out \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/Model_trial/
```


### 8. Close the vm and Baobab. Restore local terminal
```bash	 
ctrl+D
```


### Helper problem with tif files

If you encounter problems with your tif files during testing, this may be due to problems with the encoding of your tif files. To re-encode your files you can use the python script tif_2_tif.py

Open a terminal and log on to baobab
```bash
ssh 'unige_id'@baobab2.hpc.unige.ch
```
Get a gpu node
```bash	
salloc --time=1:00:00 --partition=shared-gpu --ntasks=1 --gpus-per-task=1 --cpus-per-task=8 --mem=64G
```
Launch the virtual machine
```bash	
singularity exec --nv --cleanenv --no-home --env PYTHONPATH=/usr/local/lib/ --env MPLCONFIGDIR=/scratch --scratch /scratch --bind $(realpath ~/
scratch/) /acanas/m-BioinfoSupport/singularity/deepcadrt_v2.sif bash
```
Change directory with linux command
```bash	
cd # use to change directories
ls # lists directory contents of files and directories
cd .. # go back to the previous directory
```
Execute the python script
```bash	
python3 Tif_2_tif.py <Directory_with_input_files> <Name_output_directory>
```
To exit and return to the terminal
```bash	 
2x ctrl+D
```





