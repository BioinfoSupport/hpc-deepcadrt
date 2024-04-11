
# hpc-deepcadrt
[DeepCAD-RT](https://github.com/cabooster/DeepCAD-RT) is a tool to denoise timelapse imaging data.
This repository contains code and instructions to run the tool on the HPC cluster of the University of Geneva.


# Instructions

### 1. Create a folder on the NAS with the following structure

* `Model_trial/`
  - `Train/`
  - `Test/`
  - [`deepcadrt.sbatch`](https://github.com/BioinfoSupport/hpc-deepcadrt/blob/main/deepcadrt.sbatch) # Found in repository root folder, edit if necessary


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

### 6. Run the training step
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
                        Overlap factor
  --datasets_path DATASETS_PATH
                        Folder containing files for training
  --n_epochs N_EPOCHS   Number of training epochs
  --fmap FMAP           Model complexity
  --output_dir OUTPUT_DIR
                        Output directory
  --pth_dir PTH_DIR     The path for pth file and result images
  --onnx_dir ONNX_DIR   Directory onnx model
  --batch_size BATCH_SIZE
                        Batch size
  --patch_t PATCH_T     The time dimension (frames) of 3D patches
  --patch_x PATCH_X     The width of 3D patches
  --patch_y PATCH_Y     The height of 3D patches
  --gap_y GAP_Y
  --gap_x GAP_X
  --gap_t GAP_T
  --lr LR               Learning rate
  --b1 B1               Adam: bata1
  --b2 B2               Adam: bata2
  --GPU GPU             GPU index
  --ngpu NGPU           ngpu
  --num_workers NUM_WORKERS
  --scale_factor SCALE_FACTOR
                        The factor for image intensity scaling
  --train_datasets_size TRAIN_DATASETS_SIZE
                        Datasets size for training (how many 3D patches)
  --select_img_num SELECT_IMG_NUM
                        Select the number of frames used for training
  --test_datasize TEST_DATASIZE
                        test data size
  --visualize_images_per_epoch
                        Whether to show result images after each epoch
  --save_test_images_per_epoch
                        Whether to save result images after each epoch
  --colab_display COLAB_DISPLAY
                        colab display
  --result_display RESULT_DISPLAY
                        result display
```


### 7. Run the testing step
```bash
cd ~/scratch/Model_trial
sbatch deepcadrt.sbatch deepcadrt_test.py \
  --patch_x=100 --patch_y=100 --patch_t=10 \
  --datasets_path=Test \
  --pth_dir=Model.out \
  --denoise_model=datasets_test_'training_number' \
  --output_dir=Test.out
```

**optional arguments:**
```
  -h, --help            show this help message and exit
  --overlap_factor OVERLAP_FACTOR
                        The overlap factor between two adjacent patches
  --datasets_path DATASETS_PATH
                        Dataset path
  --fmap FMAP           The number of feature maps
  --output_dir OUTPUT_DIR
                        Result file root path
  --pth_dir PTH_DIR     The path file root path
  --batch_size BATCH_SIZE
                        Batch size
  --patch_t PATCH_T     The time dimension (frames) of 3D patches
  --patch_x PATCH_X     The width of 3D patches
  --patch_y PATCH_Y     The height of 3D patches
  --gap_y GAP_Y
  --gap_x GAP_X
  --gap_t GAP_T
  --GPU GPU             the index of GPU you will use for computation
  --ngpu NGPU           ngpu
  --num_workers NUM_WORKERS
                        if you use Windows system, set this to 0.
  --scale_factor SCALE_FACTOR
                        The factor for image intensity scaling
  --test_datasize TEST_DATASIZE
                        the number of frames to be tested (test all frames if the number exceeds the total number of frames in a .tif file
  --denoise_model DENOISE_MODEL
                        Denoise model
  --visualize_images_per_epoch
                        Whether to show result images after each epoch
  --colab_display COLAB_DISPLAY
                        colab display
  --result_display RESULT_DISPLAY
                        result display
```

### 8. Copy the trained model back to the NAS
```bash
rsync -av \
  --no-perms \
  ~/scratch/Model_trial/Model.out \
  ~/scratch/Model_trial/Test.out \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/Model_trial/
```


### 9. Close the vm and Baobab. Restore local terminal
```bash	 
2x ctrl+D
```
