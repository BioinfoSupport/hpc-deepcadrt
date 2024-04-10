
# Readme deepcadrt


### 1. Open the terminal


### 2. Connecting on hpc Baobab or Yggdrdasil
```bash
ssh 'unige_id'@baobab2.hpc.unige.ch
ssh 'unige_id'@login1.yggdrasil.hpc.unige.ch
```


### 3. Build NAS on login nod 
```bash
ps -u $USER | awk '$4=="dbus-daemon"{print $1}' | xargs kill
dbus-launch bash
gio mount "smb://ISIS;$USER@nasac-m2.unige.ch/m-GHoltmaat"
```


### 4. Snychrnonise files '.tif' for training and testing
```bash
  rsync -av \
  --no-perms \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/Model_trial \
  ~/scratch/
```


### 5. Change working directory
```bash	
cd ~/scratch
```


### 6. Run the training
```bash	
sbatch deepcadrt.sbatch deepcadrt_train.py --datasets_path=Model_trial/Train --pth_dir=Model_trial/Model.out --n_epochs=4 --patch_x=100 --patch_y=100 --patch_t=10
```


### 7. Run the testing 
```bash	
sbatch deepcadrt.sbatch deepcadrt_test.py --datasets_path=Model_trial/Test --pth_dir=Model_trial/Model.out --denoise_model=datasets_test_'training_number' --output_dir=Out/ --patch_x=100 --patch_y=100 --patch_t=10
```


### 8. Close the vm and Baobab. Restore local terminal
```bash	 
2x ctrl+D
```