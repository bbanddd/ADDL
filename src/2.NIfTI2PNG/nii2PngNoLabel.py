#!/usr/bin/env python

from __future__ import print_function

import os
import argparse


parser = argparse.ArgumentParser(description='Decompose 3D MRI into 2D PNG files. \
1. Decompose 3D MRI data along Axial axis and store in PNG files \
2. Select PNG files that cover brain range')

parser.add_argument('inputDir',
                    help='Input directory containing preprocessed MRI data')

parser.add_argument('outputDir',
                    help='Output directory to contain png files')

parser.add_argument('pngLowIndex', 
                    help='Png file index from which to select, include')

parser.add_argument('pngHighIndex',
                    help='Png file index till which to select, exclude')

parser.add_argument('--scriptsDir', default='./',
                    help='Directory where decompose scripts locate, relative to working directory')

args = parser.parse_args()


inputDir  = args.inputDir
outputDir = args.outputDir
pngLowIndex  = args.pngLowIndex
pngHighIndex = args.pngHighIndex
scriptsDir = args.scriptsDir
if inputDir[-1] != '/' : inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'
if scriptsDir[-1] != '/': scriptsDir += '/'


tmpDir = '/tmp/adNii2Png/'
niiNorm2Png        = scriptsDir + '1.niiNorm2Png.py'
selectPng          = scriptsDir + '3.selectPng.py'

niiNorm2PngOutdir        = tmpDir + 'niiNorm2PngOutdir/'


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


exec_cmd('rm -rf ' + tmpDir)
exec_cmd('mkdir '  + tmpDir)


print('\n' + '='*20 + ' Stage1: Normalize 3D MRI Data and Decompose into 2D png files ' + '='*20)
cmd = 'python ' + niiNorm2Png + ' ' + inputDir + ' ' + niiNorm2PngOutdir
exec_cmd(cmd)

print('\n' + '='*20 + ' Stage2: Select Png Files ' + '='*20)
cmd = 'python ' + selectPng + ' ' + niiNorm2PngOutdir + ' ' + outputDir + ' ' + pngLowIndex + ' ' + pngHighIndex
exec_cmd(cmd)


exec_cmd('rm -rf ' + tmpDir)


exit(0)

