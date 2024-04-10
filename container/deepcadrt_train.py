#!/usr/bin/env python3

import argparse
import sys
from deepcad.train_collection import training_class

# Command line arguments parser
parser = argparse.ArgumentParser(description='Train a DeepCadRT model')
parser.add_argument('--overlap_factor',default=0.4,type=int,help='Overlap factor')
parser.add_argument('--datasets_path',required=True,help='Folder containing files for training')
parser.add_argument('--n_epochs',default=5,type=int,help='Number of training epochs')
parser.add_argument('--fmap',default=16,type=int,help='Model complexity')
parser.add_argument('--output_dir',default='./results',help='Output directory')
parser.add_argument('--pth_dir',required=True,help='The path for pth file and result images')
parser.add_argument('--onnx_dir',default='./onnx',help='Directory onnx model')
parser.add_argument('--batch_size',default=1,type=int,help='Batch size')
parser.add_argument('--patch_t',default=150,type=int,help='The time dimension (frames) of 3D patches')
parser.add_argument('--patch_x',default=150,type=int,help='The width of 3D patches')
parser.add_argument('--patch_y',default=150,type=int,help='The height of 3D patches')
parser.add_argument('--gap_y',default=60,type=int,help='')
parser.add_argument('--gap_x',default=60,type=int,help='')
parser.add_argument('--gap_t',default=6,type=int,help='')
parser.add_argument('--lr',default=0.00005,type=float,help='Learning rate')
parser.add_argument('--b1',default=0.5,type=float,help='Adam: bata1')
parser.add_argument('--b2',default=0.999,type=float,help='Adam: bata2')
parser.add_argument('--GPU',default=0,type=int,help='GPU index')
parser.add_argument('--ngpu',default=1,type=int,help='ngpu')
parser.add_argument('--num_workers',default=8,type=int)
parser.add_argument('--scale_factor',default=1,type=int,help='The factor for image intensity scaling')
parser.add_argument('--train_datasets_size',default=3000,type=int,help='Datasets size for training (how many 3D patches)')
parser.add_argument('--select_img_num',default=1000000,type=int,help='Select the number of frames used for training')
parser.add_argument('--test_datasize',default=400,type=int,help='test data size')
parser.add_argument('--visualize_images_per_epoch',action="store_true",default=False,help='Whether to show result images after each epoch')
parser.add_argument('--save_test_images_per_epoch',action="store_true",default=False,help='Whether to save result images after each epoch')
parser.add_argument('--colab_display',default=False,help='colab display')
parser.add_argument('--result_display',default='',help='result display')

args = parser.parse_args()
#args = parser.parse_args('--datasets_path="" --pth_dir=""'.split())

tc = training_class(vars(args))
tc.run()




