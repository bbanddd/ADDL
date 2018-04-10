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

Try to get higher AD diagnostic precision, we group the ADNI MRI data into several study groups and apply ADDL pipeline.  As a result we get about 95% AD diagnostic precision.

![](images/sc_wp_addl_flow_en.png)

The ADDL pipeline contains four processes, preprocessing, image format transform, training and inference. The preprocessing , the structural MRI (T1) data of all the subjects in the study group were segmented and registered to obtain the gray matter image.
 The grouping process divides the subjects in the study group into a training set and a validation set. The training process is to input training set data into ResNet model training. In the diagnosis process, the gray matter image of a subject in the test group is input into the trained ResNet model, and a diagnostic algorithm is applied to determine whether the subject suffers from Alzheimer's disease.

This chapter introduces the algorithms used in ADDL from five aspects: ADNI subjects, preprocessing, grouping, ResNet model, and diagnostic algorithm.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc2">2. Preprocessing</a>
The preprocessing stage get GM tissue images from ADNI MRI T1 data. We use [FSL-VBM](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLVBM) as the  preprocess tool, and replace several component tools with [ANTsR]().

>"Structural data was analysed with FSL-VBM (Douaud et al., 2007, http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLVBM), an optimised VBM protocol (Good et al., 2001) carried out with FSL tools (Smith et al., 2004). First, structural images were brain-extracted and grey matter-segmented before being registered to the MNI 152 standard space using non-linear registration (Andersson et al., 2007). The resulting images were averaged and flipped along the x-axis to create a left-right symmetric, study-specific grey matter template. Second, all native grey matter images were non-linearly registered to this study-specific template and "modulated" to correct for local expansion (or contraction) due to the non-linear component of the spatial transformation. The modulated grey matter images were then smoothed with an isotropic Gaussian kernel with a sigma of ?? mm. Finally, voxelwise GLM was applied using permutation-based non-parametric testing, correcting for multiple comparisons across space."
>
><p align='right'>-- Referencing FSL-VBM</p>

![Figure of Preprocessing Flow](images/sc_wp_preprocess_flow_en.png)

The figure above shows the FSL-VBM work flow details. The index of each process matches with the preprocess [sources](../src/1.DataPreprocessing) file name.

Please refer to [ADDL basic](ADDL_basic.md#toc3.6.2) document for the MNI-152 standard template information. This project uses MNI-152 template from the FSL package.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.1">2.1 Brain Extraction</a>
The brain extraction get the brain tissue data from ADNI MRI full brain data, it is a necessary process for the following GM segmentation.

We use [`abpBrainExtraction`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/abpBrainExtraction) of ANTsR as the brain extraction tool, and the [`abpN4`](https://www.rdocumentation.org/packages/ANTsR/versions/1.0/topics/abpN4) is not involved for outlier intensities truncate and bais corrects, because ADNI standard MRI T1 sequence contains [N3 correction](http://adni.loni.usc.edu/methods/mri-analysis/mri-pre-processing/). Note that we ignore the N3 and N4 difference here.

The brain extraction process, first, the MNI-152 template brain mask register to all the ADNI MRI data with affine and non-linear spatial transformation(FMM), and then get the brain with the matching brain mask registered.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.2">2.2 Grey Matter Segmentation</a>
After the brain extraction stage, the GM segmentation stage get all the ADNI subjects GM tissues data in native space, which is the start point of following GM registration process.

We use [`FAST`](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST) of FSL package as the GM segmentation tool.

>FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities). The underlying method is based on a hidden Markov random field model and an associated Expectation-Maximization algorithm. The whole process is fully automated and can also produce a bias field-corrected input image and a probabilistic and/or partial volume tissue segmentation. It is robust and reliable, compared to most finite mixture model-based methods, which are sensitive to noise.
>
><p align='right'>-- FAST Research Overview</p>


----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.3">2.3 Template Creation</a>
Template creation get a study group specify GM template from all the subjects GM data, which is used for all the subjects GM registration.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.1">2.3.1 Affine Registration</a>
Please check the [ADNI basic](ADDL_basic.md#toc3.3) for the affine registration detail. The project use [`fsl_reg`](https://manned.org/fsl4.1-fsl_reg/baac7ea7) of fsl as the affine registration tools at this stage.


----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.2">2.3.2 Non-Linear Registration</a>
Please check the [ADNI basic](ADDL_basic.md#toc3.3) for the non-linear registration detail. The project uses [`ants_regwrite`](https://rdrr.io/github/neuroconductor/extrantsr/man/ants_regwrite.html) of extrantsr as the non-linear registration tool at this stage.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.4">2.3.4 Template Generation</a>

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

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc4">4. Package Binary</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc5">5. ResNet</a>
TBD: Introduction the detail of resnet module.

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
