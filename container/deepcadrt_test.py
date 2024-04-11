#!/usr/bin/env python3

import argparse
import sys
from deepcad.test_collection import testing_class

# Command line arguments parser
parser = argparse.ArgumentParser(description='Test a DeepCadRT model')
parser.add_argument('--overlap_factor',default=0.6,type=float,help='The overlap factor between two adjacent patches')
parser.add_argument('--datasets_path',required=True,help='Dataset path')
parser.add_argument('--fmap',default=16,type=int,help='The number of feature maps')
parser.add_argument('--output_dir',required=True,help='Result file root path')
parser.add_argument('--pth_dir',required=True,help='The path file root path')
parser.add_argument('--batch_size',default=1,type=int,help='Batch size')
parser.add_argument('--patch_t',default=150,type=int,help='The time dimension (frames) of 3D patches')
parser.add_argument('--patch_x',default=150,type=int,help='The width of 3D patches')
parser.add_argument('--patch_y',default=150,type=int,help='The height of 3D patches')
parser.add_argument('--gap_y',default=40,type=int,help='')
parser.add_argument('--gap_x',default=40,type=int,help='')
parser.add_argument('--gap_t',default=4,type=int,help='')
parser.add_argument('--GPU',default=0,type=int,help='the index of GPU you will use for computation')
parser.add_argument('--ngpu',default=1,type=int,help='ngpu')
parser.add_argument('--num_workers',default=4,type=int,help='if you use Windows system, set this to 0.')
parser.add_argument('--scale_factor',default=1,type=int,help='The factor for image intensity scaling')
parser.add_argument('--test_datasize',default=1000000,type=int,help='the number of frames to be tested (test all frames if the number exceeds the total number of frames in a .tif file')
parser.add_argument('--denoise_model',required=True,help='Denoise model')
parser.add_argument('--visualize_images_per_epoch',action="store_true",default=False,help='Whether to show result images after each epoch')
parser.add_argument('--colab_display',default=False,help='colab display')
parser.add_argument('--result_display',default='',help='result display')


args = parser.parse_args()
#args = parser.parse_args('--datasets_path="" --pth_dir=""'.split())

tc = testing_class(vars(args))
tc.run()
