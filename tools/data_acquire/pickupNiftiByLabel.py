#!/usr/bin/env python

import os
import re
import pickle
import argparse
import subprocess


parser = argparse.ArgumentParser(description='Pickup data by subject based on label')
parser.add_argument('inputDir',
                    help='Input directory containing original NIfTI files')
parser.add_argument('outputDir',
                    help='Output directory containing selected NIFTI files')
parser.add_argument('labelFile', 
                    help='Label file from which to search patients')
args = parser.parse_args()

inputDir  = args.inputDir
outputDir = args.outputDir
labelFile = args.labelFile

labels = {}


def exec_cmd(cmd):
  print 'exec_cmd(): cmd = ', cmd 
  ret = os.system(cmd)
  if ret != 0:
    print '!!!FAILED!!!, exit.'
    exit(-1)

if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)

if not os.path.exists(labelFile):
  print 'ERROR: labels file not exist, exit.'
  exit(-1)

with open(labelFile, 'rb') as ifile:
  labels = pickle.load(ifile)
print 'Number of labels: ', len(labels)

niftiFiles = []
for root,dirs,files in os.walk(inputDir):
  if files:
    for ff in files:
      if re.search(r'.nii', ff) != None: 
        ptid = ff[5:15]
        if ptid in labels: niftiFiles.append(os.path.join(root,ff))

for item in niftiFiles:
  cmd = 'cp ' + item + ' ' + outputDir
  exec_cmd(cmd)

print(len(niftiFiles))

exit(0)
