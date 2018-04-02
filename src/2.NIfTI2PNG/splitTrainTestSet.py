#!/usr/bin/env python

from __future__ import print_function

import re
import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Split organized png files into training and testing set according to train and test data list')
parser.add_argument('inputDir',
                    help='Input directory containing organized png files')
parser.add_argument('trainList',
                    help='Training data list file')
parser.add_argument('testList',
                    help='Test data list file')
parser.add_argument('outputDir',
                    help='Output directory containing split training and testing set')
args = parser.parse_args()

inputDir = args.inputDir
trainList = args.trainList
testList = args.testList
outputDir = args.outputDir
if inputDir[-1]  != '/': inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'


##### input file dictionary: filebasename -> [label, filepath]
inputFilesDict = {}


trainDataList = []
testDataList  = []


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)

def fillDataList(dList, listContainer):
  with open(dList, 'r') as ifile:
    for line in ifile:
      bsname = os.path.basename(line)
      fnamebase = os.path.splitext(bsname)[0]
      fnamebase = fnamebase.replace('\n', '')
      fnamebase = fnamebase.replace('\r', '')
      listContainer.append(fnamebase)


if not os.path.exists(trainList) or not os.path.exists(testList):
  print('ERROR: data list missing.')
  sys.exit(-1)


exec_cmd('rm -rf ' + outputDir)
exec_cmd('mkdir  ' + outputDir)

trainADDir = outputDir + 'train/AD/'
trainNLDir = outputDir + 'train/NL/'
testADDir  = outputDir + 'test/AD/'
testNLDir  = outputDir + 'test/NL/'
exec_cmd('mkdir -p ' + trainADDir)
exec_cmd('mkdir -p ' + trainNLDir)
exec_cmd('mkdir -p ' + testADDir )
exec_cmd('mkdir -p ' + testNLDir )

fillDataList(trainList, trainDataList)
fillDataList(testList , testDataList )


for root,dirs,files in os.walk(inputDir):
  if dirs:
    for dd in dirs:
      if re.search(r'_S_', dd) != None:
        iidx = dd.find(r'_struc_')
        kk = dd[:iidx]
        vv1 = os.path.basename(root)
        vv2 = os.path.join(root,dd)
        assert not kk in inputFilesDict
        inputFilesDict[kk] = list([vv1, vv2])


dataNotFoundList = []
for item in trainDataList:
  if item in inputFilesDict:
    exec_cmd('cp -r ' + inputFilesDict[item][1] + ' ' + outputDir + 'train/' + inputFilesDict[item][0] + '/')
  else:
    dataNotFoundList.append(item)

for item in testDataList:
  if item in inputFilesDict:
    exec_cmd('cp -r ' + inputFilesDict[item][1] + ' ' + outputDir + 'test/' + inputFilesDict[item][0] + '/')
  else:
    dataNotFoundList.append(item)


print('Total number of data:', len(inputFilesDict))
print('Total number of training data to select:', len(trainDataList))
print('Total number of testing  data to select:', len(testDataList ))
print('Total number of data selected :', len(trainDataList) + len(testDataList) - len(dataNotFoundList))
print('Number of data not found:', len(dataNotFoundList))
for item in dataNotFoundList:
  print(item)


sys.exit(0)

