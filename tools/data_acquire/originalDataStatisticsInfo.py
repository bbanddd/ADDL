#!/usr/bin/env python

##### Show statistics information of ADNI original dataset
##    1) Total number of subjects
##    2) Total number of NIfTI files


from __future__ import print_function

import os
import re
import argparse


parser = argparse.ArgumentParser(description='Show statistics information of ADNI original dataset')
parser.add_argument('input_dir',
                    help='Input directory containing original ADNI dataset')
args = parser.parse_args()

input_dir   = args.input_dir

cnt_sbj = 0
cnt_nii = 0

for root,dirs,files in os.walk(input_dir):
  if dirs:
    for dd in dirs:
      if re.search(r'_S_', dd) != None: cnt_sbj += 1

  if files:
    for ff in files:
      if re.search(r'.nii', ff) != None: cnt_nii += 1


print('Total number of subjects:',cnt_sbj)
print('Total number of NIfTI files:',cnt_nii)
