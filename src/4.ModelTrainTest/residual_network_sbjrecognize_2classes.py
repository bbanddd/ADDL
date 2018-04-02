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

import argparse
import tflearn
from tflearn.data_utils import shuffle, to_categorical


parser = argparse.ArgumentParser(description='Subject-Level Classification')

parser.add_argument('inputDataDir',
                    help='Input directory containing testing data')

parser.add_argument('inputModel',
                    help='Trained model')

parser.add_argument('testReport',
                    help='Output test report file')

args = parser.parse_args()


inputDataDir = args.inputDataDir
inputModel   = args.inputModel
testReport   = args.testReport



# Residual blocks
# 32 layers: n=5, 56 layers: n=9, 110 layers: n=18
n = 5

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
model = tflearn.DNN(net)
model.load(inputModel)


##### Code for subject-level classification and decision making

import subject_level_classification_2classes
subject_level_classification_2classes.evaluate(model, inputDataDir, testReport)

