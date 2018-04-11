# -*- coding: utf-8 -*-

""" Deep Residual Network.

Applying a Deep Residual Network to CIFAR-10 Dataset classification task.

References:
    - K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image
      Recognition, 2015.
    - Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

Links:
    - [Deep Residual Network](http://arxiv.org/pdf/1512.03385.pdf)
    - [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)

"""

from __future__ import division, print_function, absolute_import

import os
import argparse
import tflearn
from tflearn.data_utils import shuffle, to_categorical


parser = argparse.ArgumentParser(description='Train model')

parser.add_argument('inputDataDir',
                    help='Input directory containing training and testing data')

parser.add_argument('nEpoch', type=int,
                    help='Epoch to train network')

parser.add_argument('batchSize', type=int, default=128,
                    help='Batch size')

parser.add_argument('checkpointPath',
                    help='Directory to contain model')

parser.add_argument('runId',
                    help='Name of tensorboard log file')

parser.add_argument('--tensorboardVerbose', type=int, default=3,
                    help='Tensorboard verbose level, 0 | 1 | 2 | 3')

parser.add_argument('--tensorboardDir', default='/home/python2/tensorboard_data/',
                    help='Directory to contain tensorboard log file')

args = parser.parse_args()

inputDataDir   = args.inputDataDir
checkpointPath = args.checkpointPath
nEpoch         = args.nEpoch
batchSize      = args.batchSize
runId          = args.runId

tensorboardVerbose = args.tensorboardVerbose
tensorboardDir     = args.tensorboardDir

print('inputDataDir:', inputDataDir)
print('nEpoch:', nEpoch)
print('batchSize:', batchSize)
print('checkpointPath:', checkpointPath)
print('runId:', runId)

print('tensorboardVerbose:', tensorboardVerbose)
print('tensorboardDir:', tensorboardDir)


os.system('rm -rf ' + checkpointPath)
os.system('mkdir  ' + checkpointPath)


# Residual blocks
# 32 layers: n=5, 56 layers: n=9, 110 layers: n=18
n = 5

# Data loading
import nidata_mri_by_person
(X, Y), (X_test, Y_test) = nidata_mri_by_person.load_data(inputDataDir, 'MRI')
X, Y = shuffle(X, Y)
Y = to_categorical(Y, 2)
Y_test = to_categorical(Y_test, 2)

# Real-time data preprocessing
img_prep = tflearn.ImagePreprocessing()
img_prep.add_featurewise_zero_center(per_channel=True)

# Real-time data augmentation
img_aug = tflearn.ImageAugmentation()
img_aug.add_random_flip_leftright()

# Building Residual Network
net = tflearn.input_data(shape=[None, 32, 32, 1],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug)
net = tflearn.conv_2d(net, 16, 3, regularizer='L2', weight_decay=0.0001)
net = tflearn.residual_block(net, n, 16)
net = tflearn.residual_block(net, 1, 32, downsample=True)
net = tflearn.residual_block(net, n-1, 32)
net = tflearn.residual_block(net, 1, 64, downsample=True)
net = tflearn.residual_block(net, n-1, 64)
net = tflearn.batch_normalization(net)
net = tflearn.activation(net, 'relu')
net = tflearn.global_avg_pool(net)

net = tflearn.fully_connected(net, 2)
net = tflearn.batch_normalization(net)
net = tflearn.activation(net, 'softmax')

# Regression
mom = tflearn.Momentum(0.1, lr_decay=0.1, decay_step=32000, staircase=True)
net = tflearn.regression(net, optimizer=mom,
                         loss='categorical_crossentropy')
# Training
model = tflearn.DNN(net, tensorboard_verbose=tensorboardVerbose, tensorboard_dir=tensorboardDir,
  checkpoint_path=checkpointPath)

model.fit(X, Y, n_epoch=nEpoch, shuffle=True, validation_set=(X_test, Y_test),
  show_metric=True, batch_size=batchSize, run_id=runId, snapshot_epoch=True)

