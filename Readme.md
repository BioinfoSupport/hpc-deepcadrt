
# Readme deepcadrt


### 1. Ouvrir un terminal

### 2. Se connecter sur baobab  
```bash
ssh 'mon_identifiant_unige'@baobab2.hpc.unige.ch
ssh 'mon_identifiant_unige'@login1.yggdrasil.hpc.unige.ch
```

### 3. Monter le nas sur le login node
```bash
ps -u $USER | awk '$4=="dbus-daemon"{print $1}' | xargs kill
dbus-launch bash
gio mount "smb://ISIS;$USER@nasac-m2.unige.ch/m-GHoltmaat"
```



### 4. Copier les fichiers .tif à utiliser pour le train
```bash
  rsync -av \
  --no-perms \
  ~/.gvfs/*/BioinfoSupport/GluSnFR_Data_DeepCad/Model_trial \
  ~/scratch/
```

### 6. Lancer le script bash Launch_vm

### 7. Se placer dans le bon répertoire
	cd ~/scratch

### 8. Lancer le train
	sbatch deepcadrt.sbatch deepcadrt_train.py --datasets_path=Model_trial/Train --pth_dir=Model_trial/Model.out --n_epochs=4 --patch_x=100 --patch_y=100 --patch_t=10

### 9. Lancer le test pour faire le traitement d’images
	sbatch deepcadrt.sbatch deepcadrt_test.py --datasets_path=Model_trial/Test --pth_dir=Model_trial/Model.out --denoise_model=datasets_test_<numero_du_train> --output_dir=Sortie/ --patch_x=100 --patch_y=100 --patch_t=10

### 10. Sortir de la vm et de Baobab pour revenir sur le terminal de l’ordinateur 
	2x ctrl+D
