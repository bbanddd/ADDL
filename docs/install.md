# Installation
The ADDL project are based on Bash, R and Python programming lauanguage. The local algorithm and interface develop in Python. Plenty of third party tools are involved in this project, the Bash, R and Python work as script language. The project only support Linux. And the CentOS7 is our working operation system(OS). 

The installation is very easy, just copy source, but the third party tools setting up cost a lot. The project pends on two types of tool set, the neuroimaging processing tool set and deep learning(DL) tool set. Considering the complex dependency of software versions, OS and hardware, this section introduces a full setup process to setup all the required tools based on the CentOS7 minimal installed.

***The 3rd Party Tools Structure***
* Deep learning tool set
  * GPU venders
    * Driver
    * CUDA
    * cuDNN
  * Deep learning framework
    * Anaconda
    * TensorFlow
    * TFLearn
* Neuroimaging processing tool set
  * FSL
  * ANTsR
  * Nibabel
  * OpenCV

# Deep Learning Tool Set
Currently, GPU is the most commen computation accelarator for DL algorithm. The DL tool set is typically devided into two suits, hardward vender provided tool and deep learning framework. The hardware vender provied tools contains driver interface of device and OS; CUDA the general GPU computation framework; cuDNN the DL algorithm optimization library. The DL framework connects developer and hardware, it help develper achieve DL application easily and fast, at the same time making the hardward work efficiently. There are lots of DL frameworks such as TensorFlow, Caffe2, PyTorch, etc. This project is using TensorFlow the most commen one.

## Determain Versions
There are native dependency and lantency between hardward vender provide tool and DL framework, so the latest version of DL framwork is a bit older then the latest version of hardware vender provided tools. One should take care of the versons of DL tools. Building a local version of DL framework pends on your local hardware vender provided tool for the edge features is out of scope of this document.

The TensorFlow official provides detail requiments, please check [here](https://www.tensorflow.org/install/install_linux#NVIDIARequirements).
Till this document, the TensorFlow version is [1.6](https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0), and the GPU requirement are shown below.
* CUDA = 9.0
* cuDNN = 7.0

Note the CUDA and cuDNN should be exactly match.

## GPU Venders
### Driver
### CUDA
### cuDNN
## Deep Learning Framework
### Anaconda
### TensorFlow
### TFLearn
# Neuroimaging Processing Tool Set
## FSL
## ANTsR
## Nibabel
## OpenCV