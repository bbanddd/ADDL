#!/usr/bin/env python

##### Generate labels

from __future__ import print_function


import argparse
from common import exec_cmd, adniMergeCsvTempDir


parser = argparse.ArgumentParser(description='Generate label. \
1. Select columns of interest from ADNIMERGE.csv \
2. Filter selected ADNIMERGE.csv according to common rules \
3. Generate label file. Labels are organized as dictionary data structure, KEY:PTID -> VAULE:DX')

parser.add_argument('inputFile',
                    help='Path to file ADNIMERGE.csv')

parser.add_argument('outputFile',
                    help='Path to output label file')

args = parser.parse_args()


inputFile  = args.inputFile
outputFile = args.outputFile

ADNIMERGEcsv_01_sortByPTID         = 'ADNIMERGEcsv_01_sortByPTID.py'
ADNIMERGEcsv_02_filterByCommonRule = 'ADNIMERGEcsv_02_filterByCommonRule.py'
ADNIMERGEcsv_03_genLabel           = 'ADNIMERGEcsv_03_genLabel.py'

ADNIMERGE_NO_QUOTATION_sorted      = adniMergeCsvTempDir + 'ADNIMERGE_NO_QUOTATION_sorted.csv'
ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX = adniMergeCsvTempDir + 'ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX.csv'


print('\n' + '='*20 + ' Stage1: sort ADNIMERGE.csv by PTID ' + '='*20)
cmd = 'python ' + ADNIMERGEcsv_01_sortByPTID + ' ' + inputFile + ' ' + ADNIMERGE_NO_QUOTATION_sorted
exec_cmd(cmd)

print('\n' + '='*20 + ' Stage2: filter sorted ADNIMERGE.csv by common rule ' + '='*20)
cmd = 'python ' + ADNIMERGEcsv_02_filterByCommonRule + ' ' + ADNIMERGE_NO_QUOTATION_sorted + ' ' + ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX
exec_cmd(cmd)

print('\n' + '='*20 + ' Stage3: generate label file ' + '='*20)
cmd = 'python ' + ADNIMERGEcsv_03_genLabel + ' ' + ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX + ' ' + outputFile
exec_cmd(cmd)


print('\n!!! Label file generated:', outputFile, '!!!\n')

exit(0)

