#!/usr/bin/env python

from __future__ import print_function


import re
import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Pickup data by training and testing dataset list')

parser.add_argument('inputDir',
                    help='Input directory containing original NIfTI files')

parser.add_argument('trainList',
                    help='Training data list file')

parser.add_argument('testList',
                    help='Test data list file')

parser.add_argument('outputDir',
                    help='Output directory containing selected NIFTI files')

args = parser.parse_args()

inputDir  = args.inputDir
trainList = args.trainList
testList  = args.testList
outputDir = args.outputDir
if inputDir[-1]  != '/': inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'


##### input file dictionary: filebasename -> filepath
inputFilesDict = {}

##### selected file list containing selected file basename
selectedFileList = []


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)

def fillSelectedFileList(dataList):
  with open(dataList, 'r') as ifile:
    for line in ifile:
      bsname = os.path.basename(line)
      fnamebase = os.path.splitext(bsname)[0]
      fnamebase = fnamebase.replace('\n', '')
      fnamebase = fnamebase.replace('\r', '')
      selectedFileList.append(fnamebase)


if not os.path.exists(trainList) or not os.path.exists(testList):
  print('ERROR: data list missing.')
  sys.exit(-1)


exec_cmd('rm -rf ' + outputDir)
exec_cmd('mkdir  ' + outputDir)

fillSelectedFileList(trainList)
fillSelectedFileList(testList )
print(len(selectedFileList))


for root,dirs,files in os.walk(inputDir):
  if files:
    for ff in files:
      if re.search(r'.nii', ff) != None:
        filePath = os.path.join(root,ff)
        fileBasename = os.path.basename(filePath)
        fileBasename = os.path.splitext(fileBasename)[0]
        assert not fileBasename in inputFilesDict
        inputFilesDict[fileBasename] = filePath
print(len(inputFilesDict))


dataNotFoundList = []
for item in selectedFileList:
  if item in inputFilesDict:
    exec_cmd('cp ' + inputFilesDict[item] + ' ' + outputDir)
  else:
    dataNotFoundList.append(item)


print('Total number of data:', len(inputFilesDict))
print('Total number of data to select:', len(selectedFileList))
print('Total number of data selected :', len(selectedFileList) - len(dataNotFoundList))
print('Number of data not found:', len(dataNotFoundList))
for item in dataNotFoundList:
  print(item)

sys.exit(0)

