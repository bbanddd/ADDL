#!/usr/bin/env python

##### Decompose MRI data to 2D (x,y) matrices, and save to PNG files


from __future__ import print_function

import os
import re
import argparse
import numpy as np
import nibabel as nib
import cv2


parser = argparse.ArgumentParser(description='Decompose MRI data to 2D (x,y) matrices, and save to PNG files')
parser.add_argument('inputDir',
                    help='Input directory containing preprocessed MRI data')
parser.add_argument('outputDir',
                    help='Output directory to contain decomposed png files')
args = parser.parse_args()

inputDir  = args.inputDir
outputDir = args.outputDir
if outputDir[-1] != '/': outputDir += '/'


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)

def nii2png(input_file):
  out_dir = str.split(input_file, '/')[-1][:-7]
  out_dir = outputDir + out_dir
  if not os.path.exists(out_dir):
    exec_cmd('mkdir ' + out_dir)

  mri_img = nib.load(input_file)
  mri_img_data = mri_img.get_data()

  mean, stddev = cv2.meanStdDev(mri_img_data.flatten())
  mri_img_data = (mri_img_data - mean[0][0]) / stddev[0][0]
  mri_img_data_norm = cv2.normalize(mri_img_data.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

  # shape is (X,Y,Z)
  num_z = mri_img_data_norm.shape[2]
  for ii in xrange(num_z):
    mri_img_data_slice_norm = np.rot90(mri_img_data_norm[:,:,ii])
    output_file = out_dir + '/z' + str(ii).zfill(4) + '.png'
    cv2.imwrite(output_file, mri_img_data_slice_norm * 255)


if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)


input_files = []
for root,dirs,files in os.walk(inputDir):
  if files:
    for ff in files:
      if re.search(r'_struc_GM_to_template_GM_mod_s3.nii.gz', ff) != None:
        input_files.append( os.path.join(root, ff) )

for item in input_files:
  nii2png(item)

print(len(input_files))

exit(0)

