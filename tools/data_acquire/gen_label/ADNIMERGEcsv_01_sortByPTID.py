#!/usr/bin/env python

##### Sort 'ADNIMERGE.csv' by patient ID (PTID)


from __future__ import print_function

import os
import sys
import argparse
from common import exec_cmd, adniMergeCsvTempDir


parser = argparse.ArgumentParser(description='Sort ADNIMERGE.csv by PTID')
parser.add_argument('inputFile', 
                    help='Path to file ADNIMERGE.csv')
parser.add_argument('outputFile',
                    help='Path to output file')
args = parser.parse_args()


inputFile  = args.inputFile
outputFile = args.outputFile

columnIndex = { 'PTID': 1 }


if not os.path.exists(inputFile):
  print('ERROR: inputFile not exists,',inputFile)
  sys.exit(-1)

##### Initialize @adniMergeCsvTempDir
exec_cmd('rm -rf ' + adniMergeCsvTempDir)
exec_cmd('mkdir ' + adniMergeCsvTempDir)

##### Remove all quotation(") in 'ADNIMERGE.csv'
fileAmNoQuotation = adniMergeCsvTempDir + 'ADNIMERGE_NO_QUOTATION.csv'
cmd = 'sed ' + '\'s/"//g\' ' + inputFile + ' > ' + fileAmNoQuotation
exec_cmd(cmd)

##### Split 'ADNIMERGE.csv' into files each with all records of one patient
tempDirSbjCsv = adniMergeCsvTempDir + 'csv_subject/'
exec_cmd('mkdir ' + tempDirSbjCsv)

isFirstLine = True
with open(fileAmNoQuotation, 'r') as ifile:
  for line in ifile:
    if isFirstLine: isFirstLine = False; continue

    splitRes = str.split(line, ',')
    ofilename = tempDirSbjCsv + splitRes[columnIndex['PTID']] + '.csv'

    ofile = open(ofilename, 'a')
    ofile.write(line)
    ofile.close()

##### Merge csv files under @tempDirSbjCsv
cmd = 'cat ' + tempDirSbjCsv + '* > ' + outputFile
exec_cmd(cmd)

sys.exit(0)

