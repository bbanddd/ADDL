<a id="toc_content">**Content**</a>
1. [Installation Introduction](#toc1)
1. [After CentOS7 Minimal Installation](#toc2)
1. [Deep Learning Tool Set](#toc3)
   1. [Determination Versions](#toc3.1)
   1. [GPU Vender Provided Tools](#toc3.2)
      1. [Driver](#toc3.2.1)
      1. [CUDN](#toc3.2.2)
      1. [cuDNN](#toc3.2.3)
   1. [Deep Learning Framework](#toc3.3)
      1. [Anaconda](#toc3.3.1)
      1. [TensorFlow](#toc3.3.2)
      1. [TFLearn](#toc3.3.3)
         1. [Set PyPI Mirror](#toc3.3.3.1)
1. [Neuroimaging Processing Tool Set](#toc4)
   1. [FSL](#toc4.1)
   1. [ANTsR](#toc4.2)
      1. [Related Packages](#toc4.2.1)
      1. [Installation](#toc4.2.2)
         1. [R Installation](#toc4.2.2.1)
         1. [Pending R Packages Installation](#toc4.2.2.2)
         1. [ITKR, ANTsRCore and ANTsR Installation](#toc4.2.2.3)
         1. [Extrantsr Installation](#toc4.2.2.4)
   1. [Nibabel](#toc4.3)
   1. [OpenCV](#toc4.4)
1. [All in One Script](#toc5)

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc1">1. Installation Introduction</a>
The ADDL project is based on Bash, R and Python programming language. The project algorithm and interface are developed in Python. Plenty of 3rd party tools are involved in this project. The Bash, R and Python also work as script language. The project only supports Linux. Our working operation system(OS) is CentOS7.

The installation of project is very easy, just source copy. But the 3rd party tools installation and setting up cost a lot. The project pends on two independent types of tool set, the neuroimaging processing tool set and deep learning(DL) tool set. Considering the dependency of software versions, OS and hardware, this section introduces a full process to setup all the required tools based on the CentOS7 minimal installation.

***The 3rd Party Tools Structure***<br>
* [Deep learning tool set](#toc3)
  * [GPU vender provided tools](#toc3.2)
    * [Driver](#toc3.2.1)
    * [CUDA](#toc3.2.2)
    * [cuDNN](#toc3.2.3)
  * [Deep learning framework](#toc3.3)
    * [Anaconda](#toc3.3.1)
    * [TensorFlow](#toc3.3.2)
    * [TFLearn](#toc3.3.3)
* [Neuroimaging processing tool set](#toc4)
  * [FSL](#toc4.1)
  * [ANTsR](#toc4.2)
  * [Nibabel](#toc4.3)
  * [OpenCV](#toc4.4)

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc2">2. After CentOS7 Minimal Installation</a>
Assuming one has installed CentOS7 minimal, enabled the network and the SSH. The project requires some dependency packages and an account named python2.

**Install Project Pending Packages Commands**<br>
```bash
# Necessary  tools.
yum install -y wget
yum install -y git
yum install -y bzip2
yum install -y screen

# Headers for R pending packages build installation.
yum install -y kernel-devel-$(uname -r)
yum install -y kernel-headers-$(uname -r)
yum install -y libXmu-devel
yum install -y libXi-devel
yum install -y libcurl-devel
yum install -y openssl-devel
yum install -y libpng-devel
yum install -y libX11-devel
yum install -y mesa-libGL-devel
yum install -y mesa-libGLU-devel
yum install -y ImageMagick-c++-devel

# Compiler for R pending packages source build.
yum install -y gcc
yum install -y gcc-c++
```

**Create Account Commands**<br>
```bash
# Check a user is valid, e.g. python2
getent passwd python2

# Create a user named python2
useradd python2

# Assign a password to python2, e.g. abc123
echo abc123 | passwd python2 --stdin

# Optional if you want assign python2 sudo with password.
usermod -aG wheel python2
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc3">3. Deep Learning Tool Set</a>
Currently, GPU is the most common computation accelerator for DL algorithm. The DL tool set is typically divided into two suits, the hardware vender provided tools and the DL framework. The hardware vender provided tools contain driver(interface of device and OS), CUDA(the general GPU computation framework) and cuDNN(the DL algorithm optimization library). The DL framework connects developer and hardware, it helps developer achieve DL application easily and fast, and takes the hardware work efficiently. There are lots of DL frameworks such as TensorFlow, Caffe2, PyTorch, etc. This project is using TensorFlow, that is the most common DL framework.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.1">3.1 Determination Versions</a>
There are native dependency and latency between hardware vender provide tools and DL frameworks, so the latest version of DL framework is a bit later than the latest version of hardware vender provided tools. One should take care of the versions of DL tools. Building a local version of DL framework pends on your local hardware vender provided tool for the edge features is out of this document scoping. Driver is usually backward compatible, the latest one should be fine, because the Driver, CUDA and cuDNN are good maintained inside hardware vender.

The TensorFlow official provides detail GPU tools requirement, please check [here](https://www.tensorflow.org/install/install_linux#NVIDIARequirements) for detail information. Till this document, the latest stable TensorFlow version is [1.6](https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0), and the NVIDIA tool set requirement are shown below.
* CUDA = 9.0
* cuDNN = 7.0

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.2">3.2 GPU Vender Provided Tools</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.1">3.2.1 [Driver](http://www.nvidia.com/Download/index.aspx)</a>
Select the suitable driver base on your OS and GPU device from the NVIDIA driver download address(https://www.nvidia.com/drivers). The example GPU is **GeForce GTX 1080**.

Specially, the native GPU driver of CentOS is Noveau, which is a third party open source driver for NVIDIA cards, but poor supports for the DL computation, so we need remove it before install the formal one. The following steps show the download and install detail process.

**Download**<br>
1. Manually find the drivers at [link](https://www.nvidia.com/drivers). Select the matching fields from the drop box listed below; and then click the "SEARCH" button for the search result page.<br><br>
![Figure of Download NVIDIA Driver](images/sc_install_driver1_en.png)<br><br>
1. Click the "DOWNLOAD" button at the search result page for the driver download url.
1. Click the "AGREE & DOWNLOAD" button get the package directly at the download confirmation page, or right click the button for the download url.

Downloaded package is `NVIDIA-Linux-x86_64-390.25.run`.

**Remove Noveau Driver Command**<br>
```bash
# Check nouveau driver is installed.
lsmod | grep nouveau

# Disable nouveau driver.
touch /etc/modprobe.d/blacklist-nouveau.conf
echo "blacklist nouveau
options nouveau modeset=0" > /etc/modprobe.d/blacklist-nouveau.conf
mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
dracut -v /boot/initramfs-$(uname -r).img $(uname -r)
reboot
```

Note: There is reboot process during driver installation.

**Install NVDIA Driver Command**<br>
```bash
# Check nvida driver is installed.
lsmod | grep nvidia

# Install nvida driver without interaction.
bash NVIDIA-Linux-x86_64-390.25.run --silent
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.2">3.2.2 [CUDA](https://developer.nvidia.com/cuda-zone)</a>
Select the suitable CUDA version base on TenorFlow requirement, and select the suitable package base on the OS. The following steps show the download and install detail process.

**Download**<br>
1. Manually find the CUDA 9.0 from the [archive page](https://developer.nvidia.com/cuda-toolkit-archive).
1. Select the matching fields of the check box from the CUDA download page listed below.<br><br>
![Figure of CUDA Select Target Platform](images/sc_install_cuda1_en.png) <br><br>
1. The CUDA and patch packages are listed below, the download url is at the "Download" button.<br><br>
![Figure of CUDA and Patch Packages](images/sc_install_cuda2_en.png)<br><br>

Downloaed Packages
* `cuda_9.0.176_384.81_linux.run`
* `cuda_9.0.176.1_linux.run`
* `cuda_9.0.176.2_linux.run`

**Install CUDA Command**<br>
```bash
bash cuda_9.0.176_384.81_linux.run --silent
bash cuda_9.0.176.1_linux.run --silent --installdir=/usr/local/cuda --accept-eula
bash cuda_9.0.176.2_linux.run --silent --installdir=/usr/local/cuda --accept-eula
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.3">3.2.3 [cuDNN](https://developer.nvidia.com/cudnn)</a>
The cuDNN is a CUDA library used for DL computation, the installation process is a binary copy process, one should exactly select the version basing on your environment. The cuDNN download and installation detail process are listed below.

**Download**<br>
1. Download a cuDNN package requires registration as a NVIDIA Developer. Click "Join" button of the NVIDA developer [main page](https://developer.nvidia.com/) to finished the register process, if one is not assigned.
1. Goto the cuDNN [download page](https://developer.nvidia.com/rdp/cudnn-download), and enable the check box of "cuDNN software license agreement".
1. Select the cuDNN v7.0.5 for CUDA 9.0 as the TensorFlow requirement, and get the dropdown selections.<br><br>
![Figure of cuDNN Download](images/sc_install_cudnn1_en.png)<br><br>
1. Get the download url of the cuDNN package from the "cuDNN v7.0.5 Library for Linux" selection.

Note: If your downloaded package is named `cudnn-9.0-linux-x64-v7.solitairetheme8`, the suffix solitairetheme8 is Microsoft Solitaire Collection caused, rename it to tgz should be fine.

**Install cuDNN Commands**<br>
```bash
# Rename the downloaded cuDNN package.
mv cudnn-9.0-linux-x64-v7.solitairetheme8 cudnn-9.0-linux-x64-v7.tgz

# Install with unpackaging the cuDNN package.
tar xzvf cudnn-9.0-linux-x64-v7.tgz -C /usr/local
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.3">3.3 Deep Learning Framework</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.3.1">3.3.1 [Anaconda](https://www.anaconda.com/)</a>
Anaconda is a freemium open source distribution of the Python and R programming languages for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. Package versions are managed by the package management system conda.

The project uses Anaconda Python environment instead of CentOS7 native python environment to avoid OS dependency. And Anaconda Python2.7 is installed at a normal user account named python2.

**Download**<br>
Select a latest Anaconda2 package base on the OS from the archive [url](https://repo.continuum.io/archive/).

Downloaded package is `Anaconda2-5.1.0-Linux-x86_64.sh`.

**Install Anaconda Commands**<br>
```bash
# Install Anaconda at python2 account.
bash Anaconda2-5.1.0-Linux-x86_64.sh -b

# Assign Anaconda executions the first priority.
echo "export PATH=\"$HOME/anaconda2/bin:\$PATH\"" >> $HOME/.bashrc
source $HOME/.bashrc

# Option: Add nearest conda mirror.
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.3.2">3.3.2 [TensorFlow](https://www.tensorflow.org/)</a>
TensorFlow™ is an open source software library for high performance numerical computation. Its flexible architecture allows easy deployment of computation across a variety of platforms (CPUs, GPUs, TPUs), and from desktops to clusters of servers to mobile and edge devices. Originally developed by researchers and engineers from the Google Brain team within Google’s AI organization, it comes with strong support for machine learning and deep learning and the flexible numerical computation core is used across many other scientific domains.

**Download**<br>
Please check the download [url](https://www.tensorflow.org/install/install_linux#the_url_of_the_tensorflow_python_package), and select "Python2.7" and "GPU support" to get the TensorFlow package url `https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl`.

**Install TensorFlow Commands**<br>
```bash
# The installation process contains some dependency package installation.
# If your pip downloading slowly, please change a fast PyPI mirror.
pip install tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl

# Assign CUDA environment variables suits for TensorFlow GPU.
echo "export PATH=\"/usr/local/cuda/bin:\$PATH\"" >> $HOME/.bashrc
echo "export LD_LIBRARY_PATH=\"/usr/local/cuda/lib64:\$LD_LIBRARY_PATH\"" >> $HOME/.bashrc
echo "export CUDA_HOME=\"/usr/local/cuda\"" >> $HOME/.bashrc
source $HOME/.bashrc
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.3.3">3.3.3 [TFLearn](http://tflearn.org/)</a>
TFLearn is a modular and transparent deep learning library built on top of TensorFlow. It was designed to provide a higher-level API to TensorFlow in order to facilitate and speed-up experimentations, while remaining fully transparent and compatible with it. The PyPI/pip supports TFLearn package installation.

The project implements DL models with TFLearn.

**Install TFLearn Command**<br>
```bash
pip install tflearn
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

#### <a id="toc3.3.3.1">3.3.3.1 Set PyPI Mirror</a>
Please use your prefer PyPI mirror. For example setting mirror `https://pypi.tuna.tsinghua.edu.cn/simple` as the default PyPI mirror.

**Temporary Usage**<br>
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

**Default Setting**<br>
Fill the following context to file `~/.config/pip/pip.conf`.
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc4">4. Neuroimaging Processing Tool Set</a>
The rapid progress of research in the neuroscience and neuroimaging fields has been accompanied by the development of many excellent analysis software tools. These are implemented in a variety of computer languages and programming environments. This project takes use of two packages FSL and ANTsR for brain extraction, registration, grey matter extraction etc.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc4.1">4.1 [FSL](http://www.fmrib.ox.ac.uk/fsl/)</a>
FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI brain imaging data. It runs on Apple and PCs (both Linux, and Windows via a Virtual Machine), and is very easy to install. Most of the tools can be run both from the command line and as GUIs ("point-and-click" graphical user interfaces). To quote the relevant references for FSL tools you should look in the individual tools' manual pages.

The FSL download and install is handled with a FSL install tool named `fslintaller.py` and the FSL install package is more than 2G. We suffered install fail caused by download fail, so we suggest offline download package first. The detail download and install process are listed below.

**Download**<br>
1. Download the FSL install tool from url `https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py`.
1. Get the FSL package url base on OS from FSL install tools.
   1. Search the `download_file()` function defination in the `fslinstaller.py`, adding the print url code.
```python
def download_file(url, localf, timeout=20):
    '''Get a file from the url given storing it in the local file specified'''
    print url # Hey,new adding here!
    try:
        rf = open_url(url, 0, timeout)
    except OpenUrlError, e:
        raise DownloadFileError(str(e))
```

   1. Get the FSL package url by the following command, and then Control-c.
```bash
python fslinstaller.py -o
```

The FSL package url is `https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-5.0.10-centos7_64.tar.gz`.

**Install FSL Command**<br>
```bash
python fslinstaller.py -f fsl-5.0.10-centos7_64.tar.gz -M -d /usr/local/fsl -q
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc4.2">4.2 [ANTsR](https://github.com/ANTsX/ANTsR)</a>
ANTsR is a package providing ANTs features in R as well as imaging-specific data representations, spatially regularized dimensionality reduction and segmentation tools.

ANTsR interfaces state of the art image processing with R statistical methods. The project grew out of the need, at University of Pennsylvania, to develop large-scale analytics pipelines that track provenance from scanner to scientific study. ANTsR wraps an ANTs and ITK C++ core via Rcpp to access these frameworks from within R and support reproducible analyses. Specialized functionality in ANTsR includes image segmentation and registration along imaging specific variations of principal component and canonical correlation analysis.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc4.2.1">4.2.1 Related Packages</a>
**[R](https://www.r-project.org)**<br>
R is a freely available language and environment for statistical computing and graphics which provides a wide variety of statistical and graphical techniques: linear and nonlinear modelling, statistical tests, time series analysis, classification, clustering, etc.

**[ITK](https://itk.org)**<br>
ITK is an open-source software toolkit for performing registration and segmentation. Segmentation is the process of identifying and classifying data found in a digitally sampled representation. Typically, the sampled representation is an image acquired from such medical instrumentation as CT, MRI or ultrasound scanners. Registration is the task of aligning or developing correspondences between data. For example, in the medical environment, a CT scan may be aligned with a MRI scan in order to combine the information contained in both.

**[INKR](http://github.com/stnava/ITKR)**<br>
ITKR provides R-based access to the Insight ToolKit (ITK) for medical image processing, registration and segmentation.

**[ANTs](http://stnava.github.io/ANTs)**<br>
The ANTS framework provides open-source functionality for deformable normalization with large deformations. Small deformation mappings and segmentation tools are also available.  Developer evaluation showed stronger differences with other methodology in neurodegenerative neuroimaging data, where large deformation is required. ANTs serves as both a base for further algorithm development and also as an application-oriented toolkit. ANTS enable diffeomorphic normalization with a variety of transformation models, optimal template construction, multiple types of diffeomorphisms, multivariate similarity metrics, diffusion tensor processing and warping, image segmentation with and without priors and measurement of cortical thickness from probabilistic segmentations. The normalization tools, alone, provide a near limitless range of functionality and allow the user to develop customized objective functions. Objective functions in ANTS are of the form: Deformation Cost + Data Terms, and the command line reflects this balance of two terms. As mentioned above, the data term may combine multiple different measures of similarity that are optimized in parallel, for instance, image similarity and landmark terms.

**[ANTsRCore](https://github.com/ANTsX/ANTsRCore)**<br>
A package providing core features for ANTsR.

**[Extrantsr](https://github.com/muschellij2/extrantsr)**<br>
Extrantsr extends the ANTsR package with simple wrappers and complex processing streams for neuroimaging data.

**[CRAN](https://cran.r-project.org)**<br>
CRAN is a network of ftp and web servers around the world that store identical, up-to-date, versions of code and documentation for R. Please use the CRAN mirror(`https://cran.r-project.org/mirrors.html`) nearest to you to minimize network load.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc4.2.2">4.2.2 Installation</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

#### <a id="toc4.2.2.1">4.2.2.1 R Installation</a>
The R installation package for CentOS7 could be found at EPEL.

**Install Commands**<br>
```bash
yum install -y epel-release
yum install -y R
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

#### <a id="toc4.2.2.2">4.2.2.2 Pending R Packages Installation</a>
The ITKR, ANTsRCore, ANTsR and Extrantsr requires some R packages. The installation of pending R packages are handled by CRAN, and use `install.package()` function. It contains download and source compiling process. Please choose a CPAN mirror nearly to accelerator the download process, and assign more threads for the compiling process. The source compiling needs some header packages for the CentOS7, please refer to the [After CentOS7 Minimal Installation](#toc2) session for the header packages detail.

**Install Commands**<br>
```bash
install.package("bitops",      repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("abind",       repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("neurobase",   repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("matrixStats", repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("R.utils",     repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("rgl",         repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("R.matlab",    repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("neuroim",     repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("magic",       repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("psych",       repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("rsvd",        repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("RcppEigen",   repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("WhiteStripe", repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("fslr",        repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("oro.nifti",   repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
install.package("devtools",    repos="https://mirrors.ustc.edu.cn/CRAN", dependencies=TRUE, Ncpus=1)
```

Note: The `https://mirrors.ustc.edu.cn/CRAN` is our CRAN mirror address, and `Ncpus` argument is the threads number of install process.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

#### <a id="toc4.2.2.3">4.2.2.3 ITKR, ANTsRCore and ANTsR Installation</a>
The ITKR, ANTsRCore and ANTsR release contain pre-compile binary packages, so the installation is a download and install process.

**Download Process**<br>
The download process is listed below till this document.
1. Goto [INKR Release page](https://github.com/stnava/ITKR/releases), and select package `ITKR_0.4.12_R_x86_64-pc-linux-gnu.tar.gz` from "Latest/nightly release" session.
1. Goto [ANTsRCore Release page](https://github.com/ANTsX/ANTsR/releases), and select package `ANTsRCore_0.4.2.1_R_x86_64-pc-linux-gnu.tar.gz` from "Latest release" session.
1. Goto [ANTsR Release page](https://github.com/ANTsX/ANTsR/releases), and select package `ANTsR_0.6.1_R_x86_64-pc-linux-gnu.tar.gz` from "Latest/nightly release" session.

**Install Commands**<br>
```bash
R CMD INSTALL ITKR_0.4.12_R_x86_64-pc-linux-gnu.tar.gz
R CMD INSTALL ANTsRCore_0.4.2.1_R_x86_64-pc-linux-gnu.tar.gz
R CMD INSTALL ANTsR_0.6_R_x86_64-pc-linux-gnu.tar.gz
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

#### <a id="toc4.2.2.4">4.2.2.4 Extrantsr Installation</a>
We use the [`neuro_install()`](https://neuroconductor.org/neuroc-help-install) function of [Neuroconductor](https://neuroconductor.org/) as the Extrantsr installation tool.

**Install Commands**<br>
```bash
source("https://neuroconductor.org/neurocLite.R")
neuroc_install("extrantsr")
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc4.3">4.3 [Nibabel](http://nipy.org/nibabel/)</a>
This package provides read/write access to some common medical and neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips PAR/REC. We can read and write FreeSurfer geometry, annotation and morphometry files. There is some very limited support for DICOM. NiBabel is the successor of PyNIfTI.

This project taking use of Nibabel for neuroimaging to image data transfer.

**Install nibabel Command**<br>
```bash
pip install nibabel
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc4.4">4.4 [OpenCV](https://opencv.org/)</a>
OpenCV (Open Source Computer Vision Library) is released under a BSD license and hence it’s free for both academic and commercial use. It has C++, Python and Java interfaces and supports Windows, Linux, Mac OS, iOS and Android. OpenCV was designed for computational efficiency and with a strong focus on real-time applications. Written in optimized C/C++, the library can take advantage of multi-core processing. Enabled with OpenCL, it can take advantage of the hardware acceleration of the underlying heterogeneous compute platform.

**Install opencv-python Command**<br>
```bash
pip install opencv-python
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc5">5. All in One Script</a>
To simplify the 3rd party tools setup process, we integrate all the process in one script [`setup_env.sh`](../tools/setup_env/setup_env.sh), and it requires pre-download some packages at `$ADDLROOT/tools/setup_env/pkg/`. And the packages are listed below.
1. [NVIDIA-Linux-x86_64-390.25.run](http://us.download.nvidia.com/XFree86/Linux-x86_64/390.25/NVIDIA-Linux-x86_64-390.25.run)
1. [cuda_9.0.176_384.81_linux.run](https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run)
1. [cuda_9.0.176.1_linux.run](https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/1/cuda_9.0.176.1_linux-run)
1. [cuda_9.0.176.2_linux.run](https://developer.nvidia.com/compute/cuda/9.0/Prod/patches/2/cuda_9.0.176.2_linux-run)
1. [cudnn-9.0-linux-x64-v7.tgz](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.5/prod/9.0_20171129/cudnn-9.0-linux-x64-v7)
1. [Anaconda2-5.1.0-Linux-x86_64.sh](https://repo.continuum.io/archive/Anaconda2-5.1.0-Linux-x86_64.sh)
1. [tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl](https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl)
1. [fslinstaller.py](https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py)
1. [fsl-5.0.10-centos7_64.tar.gz](https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-5.0.10-centos7_64.tar.gz)
1. [ITKR_0.4.12_R_x86_64-pc-linux-gnu.tar.gz](https://github.com/stnava/ITKR/releases/download/latest/ITKR_0.4.12_R_x86_64-pc-linux-gnu.tar.gz)
1. [ANTsRCore_0.4.2.1_R_x86_64-pc-linux-gnu.tar.gz](https://github.com/ANTsX/ANTsRCore/releases/download/v0.4.2.1/ANTsRCore_0.4.2.1_R_x86_64-pc-linux-gnu.tar.gz)
1. [ANTsR_0.6.1_R_x86_64-pc-linux-gnu.tar.gz](https://github.com/ANTsX/ANTsR/releases/download/latest/ANTsR_0.6.1_R_x86_64-pc-linux-gnu.tar.gz)

**Instell Commands**<br>
1. Go to the `$ADDLROOT/tools/setup_env` folder.
1. Launch the install script with root, there is a reboot process for the GPU driver update.
```bash
sudo bash setup_env.sh
```

Note: if some packages download slowly and cause install process fail, please update the package mirror according this document.
