<a id="toc_content">**Content**</a>
1. [ADDL Introduction](#toc1)
1. [Preprocessing](#toc2)
   1. [Brain Extraction](#toc2.1)
   1. [Grey Matter Segmentation](#toc2.2)
   1. [Template Creation](#toc2.3)
      1. [Affine Registration](#toc2.3.1)
      1. [Non-Linear Registration](#toc2.3.2)
      1. [Template Generation](#toc2.3.3)
   1. [Non-Linear Registration](#toc2.4)
   1. [Modulation](#toc2.5)
   1. [Smooth](#toc2.6)
1. [Format Transform](#toc3)
1. [Package Binary](#toc4)
1. [ResNet](#toc5)
1. [Diagnostic](#toc6)
1. [Reference](#toc7)

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc1">1. ADDL Introduction</a>
The ADDL project bases on structural MRI (T1, 2017) data of Alzheimer's disease(AD) and non-Alzheimer's disease(NL) subjects of ADNI. It takes ResNet DL module to learn the brain gray matter(GM) tissue images obtained through preprocessing, and applies diagnostic algorithm on the ResNet module inference results for the AD diagnostic.

![Figure of ADDL Pipeline](images/sc_wp_addl_flow_en.png)

The ADDL pipeline above shows the project workflow, it contains four processes, preprocessing, format transfer, training and inference. The preprocessing extract GM from ADNI MRI T1 data, and handle GM registration cross study group. The format transfer process changes the data format from NIFTI to PNG and parts all the PNG data into two sets train and validation. The training process packages the train set PNG and the matching labels(AD/NL) into binary, feeds binary into ResNet module for training, and get the ResNet module parameters till the network convergence. The inference process packages the validation set PNG by subject into binary, feeds the binary into trained ResNet module, and get the AD diagnostic result base on the diagnostic algorithm.   

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc2">2. Preprocessing</a>
The preprocessing stage get GM tissue from ADNI MRI T1 data. We use [FSL-VBM](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLVBM) as the  preprocess tool, and replace several component tools with [ANTsR](https://github.com/ANTsX/ANTsR).

>"Structural data was analysed with FSL-VBM (Douaud et al., 2007, http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLVBM), an optimised VBM protocol (Good et al., 2001) carried out with FSL tools (Smith et al., 2004). First, structural images were brain-extracted and grey matter-segmented before being registered to the MNI 152 standard space using non-linear registration (Andersson et al., 2007). The resulting images were averaged and flipped along the x-axis to create a left-right symmetric, study-specific grey matter template. Second, all native grey matter images were non-linearly registered to this study-specific template and "modulated" to correct for local expansion (or contraction) due to the non-linear component of the spatial transformation. The modulated grey matter images were then smoothed with an isotropic Gaussian kernel with a sigma of ?? mm. Finally, voxelwise GLM was applied using permutation-based non-parametric testing, correcting for multiple comparisons across space."
>
><p align='right'>-- Referencing FSL-VBM</p>

![Figure of Preprocessing Flow](images/sc_wp_preprocess_flow_en.png)

The figure above shows the FSL-VBM work flow details. The index of each process matches with the preprocess [sources](../src/1.DataPreprocessing) file name.

Please refer to [ADDL basic](ADDL_basic.md#toc3.6.2) document for the MNI-152 standard template information. This project uses MNI-152 template from the FSL package.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.1">2.1 Brain Extraction</a>
The brain extraction get the brain tissue from ADNI MRI full brain data, it is a necessary process for the following GM segmentation for the better segmentation result.

We use [`abpBrainExtraction`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/abpBrainExtraction) of ANTsR as the brain extraction tool, and the [`abpN4`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/abpN4) is not involved for outlier intensities truncate and bais corrects, because ADNI standard MRI T1 sequence contains [N3 correction](http://adni.loni.usc.edu/methods/mri-analysis/mri-pre-processing/). Note that we ignore the N3 and N4 difference here.

The brain mask of MNI-152 template register to all the ADNI MRI data with affine and non-linear spatial transformation(FMM), and then get the brain with the matching brain mask registered.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.2">2.2 Grey Matter Segmentation</a>
After the brain extraction stage, the GM segmentation stage get all the ADNI subjects GM tissues data in native space, which is the start point of following GM registration processes.

We use [`FAST`](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST) of FSL package as the GM segmentation tool.

>FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities). The underlying method is based on a hidden Markov random field model and an associated Expectation-Maximization algorithm. The whole process is fully automated and can also produce a bias field-corrected input image and a probabilistic and/or partial volume tissue segmentation. It is robust and reliable, compared to most finite mixture model-based methods, which are sensitive to noise.
>
><p align='right'>-- FAST Research Overview</p>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.3">2.3 Template Creation</a>
Template creation get a study group specify GM template from all the subjects GM data, which is used for all the subjects GM registration. It applies affine registration for all the study group GM data base on MNI152, and get a template named MNI152-ADI affine. And then it applies non-linear registration for all the study group GM data base on MNI152-ADNI affine template, and get the result template for the following GM registration process.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.1">2.3.1 Affine Registration</a>
Please check the [ADNI basic](ADDL_basic.md#toc3.3) for the affine registration detail.

The project use [`fsl_reg`](https://manned.org/fsl4.1-fsl_reg/baac7ea7) of FSL as the affine registration tools at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.2">2.3.2 Non-Linear Registration</a>
Please check the [ADNI basic](ADDL_basic.md#toc3.3) for the non-linear registration detail.

The project uses [`ants_regwrite`](https://rdrr.io/github/neuroconductor/extrantsr/man/ants_regwrite.html) of extrantsr as the non-linear registration tool at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.4">2.3.4 Template Generation</a>
The template generation get a template for the study group, it contains the average and left-right mirror operations. The average makes the template contains all the subjects of study group information, and the left-right mirror is from the brain left-right symmetric.

The project use [`fslmerge`](), [`fslmaths`]() and [`fslswapdim`]() of FSL for the template generation tools.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.4">2.4 Non-Linear Registration</a>
This non-linear registration stage perform spatial normalization for all ADNI study group subjects' GM data base on the study group template generated at [section 2.4]().

Please check the [ADNI basic](ADDL_basic.md#toc3.3) for the non-linear registration detail.

The project uses [`antsRegistration`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/antsRegistration) of ANTsR as the non-linear registration tool at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.5">2.5 Modulation</a>
As a result of nonlinear spatial normalization, the volumes of certain brain regions may grow, whereas others may shrink. In order to preserve the volume of a particular tissue (grey or white matter or CSF) within a voxel, a further processing step is incorporated. This involves multiplying (or modulating) voxel values in the segmented images by the Jacobian determinants derived from the spatial normalization step. In effect, an analysis of modulated data tests for regional differences in the absolute amount (volume) of grey matter, whereas analysis of unmodulated data tests for regional differences in concentration of grey matter (per unit volume in native space) (Ashburner and Friston, 2000).

The project use [`createJacobianDeterminantImage`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/createJacobianDeterminantImage) of AntsR as the modulation tool at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.6">2.6 Smooth</a>
The normalized, segmented images are smoothed using a 3-mm FWHM isotropic Gaussian kernel. This conditions the data to conform more closely to the Gaussian field model underlying the statistical procedures used for making inferences about regionally specific effects. Smoothing also has the effect of rendering the data more normally distributed (by the central limit theorem). The intensity in each voxel of the smoothed data is a locally weighted average of grey matter density from a region of surrounding voxels, the size of the region being defined by the size of the smoothing kernel (Ashburner and Friston, 2000).

The project use [`fslmaths`](https://mandymejia.wordpress.com/fsl-maths-commands/) of FSL as the smooth tool at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc3">3. Format Transform</a>
The formation transform or NIFTI2PNG process services for the DL module.

![Figure of Format Transform]()

**Normalization**<br>
The data normalization operation is involved for the DL module, which helps accelerate the DL module convergent.

**3D-2D Format Transfer**<br>
The DL module expect 2D images data, so this stage changes the ADNI MRI format NIFTI to PNG, which changes a 3D imaging data into several 2D images along the Z axle.

**Selection**<br>
 After the GM segmentation and registration of preprocessing process, there are some blank images in the top and bottom area, we remove all the blank images at the same Z axle location for all the subject images.

**Training and Validation Group**<br>
Note the training and validation groups requires for the DL module. For each study group, 80% of the images of both of AD and NL class are chosen for training, and the rest 20% are for validation. One subject, together with his/her images of all visits, appear in only training or validation group.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc4">4. Package Binary</a>
The package binary process services for the DL module more detail. It resizes the PNG resolution according the DL module, 32x32 in the project. It packages the PNG data with label for the DL module train process, packages the PNG data by subjects for the DL module inference process. It saves the PNG data in the Python object efficient way because the DL module is a Python script too.   

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc5">5. ResNet</a>
TBD: Introduction the detail of resnet module.

```python
# Residual blocks
# 32 layers: n=5, 56 layers: n=9, 110 layers: n=18
n = 5

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
```

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc6">6. Diagnostic Algorithm</a>
The output of ResNet module of the diagnostic process are a vector of labels, which reflect the AD predication values of images along the Z axon. Considering the different GM location or the tissue connection might indication the AD features, for better accuracy we weighted each element of the label vector as the quantity of diagnostic.





----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc7">7. Reference</a>
\[1\] <a id="r1">[Saman Sarraf, DeepAD: Alzheimer's Disease Classification via Deep Convolutional Neural Networks using MRI and fMRI, doi: http://dx.doi.org/10.1101/070441, 2016]()</a><br>
\[2\] <a id="r2">[Alex Krizhevsky, ImageNet Classification with Deep Convolutional Neural Networks]()</a><br>
\[3\] <a id="r3">[Brian B. Avants, A Reproducible Evaluation of ANTs Similarity Metric Performance in Brain Image Registration, doi:10.1016/j.neuroimage.2010.09.025]()</a><br>
\[4\] <a id="r4">[Max A. Viergever , A survey of medical image registration – under review, 2016]()</a><br>
\[5\] <a id="r5">[J. B. Antoine Maintz, A survey of medical image registration, Medical Image Analysis (1998) volume 2, number 1, pp 1–36]()</a><br>
\[6\] <a id="r6">[Kate E. Macdonald , Automated Template-Based Hippocampal Segmentations from MRI: The Effects of 1.5T or 3T Field Strength on Accuracy, DOI 10.1007/s12021-013-9217-y, 2014]()</a><br>
\[7\] <a id="r7">[Fatma El-Zahraa Ahmed El-Gamal, Current trends in medical image registration and fusion, Egyptian Informatics Journal (2016) 17, 99–124, 2015]()</a><br>
\[8\] <a id="r8">[Matthew Lai, Deep Learning for Medical Image Segmentation, arXiv:1505.02000v1, 2015]()</a><br>
\[9\] <a id="r9">[Shumao Pang, Hippocampus Segmentation Based on Local Linear Mapping, DOI: 10.1038/srep45501, 2016]()</a><br>
\[10\] <a id="r10">[Yongfu Hao, Local Label Learning (L3) for Multi-Atlas based Segmentation, doi: 10.1117/12.911014, 2012]()</a><br>
\[11\] <a id="r11">[Yoshua Bengio, Representation Learning: A Review and New Perspectives, rXiv:1206.5538v3, 2014]()</a><br>
\[12\] <a id="r12">[Guorong Wu, Scalable High Performance Image Registration Framework by Unsupervised Deep Feature Representations Learning, doi:10.1109/TBME.2015.2496253, 2016]()</a><br>
\[13\] <a id="r13">[Guorong Wu, Unsupervised Deep Feature Learning for Deformable Registration of MR Brain Images, Med Image Comput Comput Assist Interv. 2013 ; 16(0 2): 649–656., 2014]()</a><br>
\[14\] <a id="r14">[Hiba A. Mohammed, The Image Registration Techniques for Medical Imaging (MRI-CT), doi:10.5923/j.ajbe.20160602.02, 2016]()</a><br>
\[15\] <a id="r15">[Hajnal, J. V., Hawkes, D. J., & Hill, D. L. (2001). Medical Image Registration. CRC Press.]()</a><br>

Zhang, Y. and Brady, M. and Smith, S. Segmentation of brain MR images through a hidden Markov random field model and the expectation-maximization algorithm. IEEE Trans Med Imag, 20(1):45-57, 2001.
