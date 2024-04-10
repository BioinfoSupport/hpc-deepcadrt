
# Readme deepcadrt

### 0. Create a folder on the NAS

Follow the structure:

* `Model_trial/`
  - `Train/`
  - `Test/`
  - [`deepcadrt.sbatch`](https://github.com/BioinfoSupport/hpc-deepcadrt/blob/main/deepcadrt.sbatch) # Found in repository root folder, edit if necessary


### 1. Open a terminal

### 2. Connect to hpc (Baobab or Yggdrdasil)
```bash
ssh 'unige_id'@baobab2.hpc.unige.ch
ssh 'unige_id'@login1.yggdrasil.hpc.unige.ch
```


### 3. Mount NAS on the login node
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
sbatch deepcadrt.sbatch deepcadrt_train.py \
  --n_epochs=4 --patch_x=100 --patch_y=100 --patch_t=10 \
  --datasets_path=~/scratch/Model_trial/Train \
  --pth_dir=~/scratch/Model_trial/Model.out
```


### 7. Run the testing step
```bash	
sbatch deepcadrt.sbatch deepcadrt_test.py \
  --patch_x=100 --patch_y=100 --patch_t=10 \
  --datasets_path=~/scratch/Model_trial/Test \
  --pth_dir=~/scratch/Model_trial/Model.out \
  --denoise_model=datasets_test_'training_number' \
  --output_dir=~/scratch/Model_trial/Test.out
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
