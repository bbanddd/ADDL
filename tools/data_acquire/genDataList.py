#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse

parser = argparse.ArgumentParser(description='Generate data list from data')
parser.add_argument('input_dir',
                    help='Input directory containing NiFTI files')
args = parser.parse_args()

input_dir = args.input_dir


data_list = []
for root,dirs,files in os.walk(input_dir):
  if files:
    for ff in files:
      if re.search(r'_struc.nii', ff) != None: 
        data_list.append(ff)


data_list.sort()
for ff in data_list:
  print(ff)

exit(0)
