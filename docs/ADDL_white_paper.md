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

**Figure of Preprocessing Flow**<br>
![Figure of Preprocessing Flow](images/sc_wp_preprocess_flow_en.png)

The figure above shows the FSL-VBM work flow detail. The index of process match with the preprocess [sources](../src/1.DAtaPreprocessing).

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.1">2.1 Brain Extraction</a>
This is a fully automated procedure to remove scalp tissue, skull, and dural venous sinus voxels. This procedure initially involves segmentation of the original structural MR images (in native space) into grey and white matter images, followed by a series of fully automated morphological operations for removing unconnected non-brain voxels from the segmented images (erosion followed by conditional dilation). The resulting images are extracted grey and white matter partitions in native space.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.2">2.2 Grey Matter Segmentation</a>
Scans were then segmented into grey matter, white matter, CSF, and other nonbrain partitions. SPM segmentation employs a mixture model cluster analysis to identify voxel intensities matching particular tissue types (grey matter, white matter and CSF) combined with an a priori knowledge of the spatial distribution of these tissues in normal subjects, derived from probability maps. The segmentation step also incorporates an image intensity nonuniformity correction (Ashburner and Friston, 2000) to address image intensity variations caused by different positions of cranial structures within the MRI head coil.

Scans were then segmented into grey matter, white matter, CSF, and other nonbrain partitions. SPM segmentation employs a mixture model cluster analysis to identify voxel intensities matching particular tissue types (grey matter, white matter and CSF) combined with an a priori knowledge of the spatial distribution of these tissues in normal subjects, derived from probability maps. The segmentation step also incorporates an image intensity nonuniformity correction (Ashburner and Friston, 2000) to address image intensity variations caused by different positions of cranial structures within the MRI head coil.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.3">2.3 Template Creation</a>
First, an anatomical template was created from a subgroup of all normal subjects with a mean age and age range matched to the entire study group imaged on the same MRI scanner with the same scanning parameters, in order to reduce any scanner-specific bias and provide a template appropriate to the population sample. This involves spatially normalizing each structural MRI to the ICBM-152 template (Montreal Neurological Institute), which is derived from 152 normal subjects and approximates the Talairach space. The normalized data are then smoothed with an 8-mm full-width at half-maximum (FWHM) isotropic Gaussian kernel, and a mean image (the template) is created.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.1">2.3.1 Affine Registration</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.2">2.3.2 Non-Linear Registration</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc2.3.4">2.3.4 Template Generation</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.4">2.4 Non-Linear Registration</a>

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.5">2.5 Modulation</a>
As a result of nonlinear spatial normalization, the volumes of certain brain regions may grow, whereas others may shrink. In order to preserve the volume of a particular tissue (grey or white matter or CSF) within a voxel, a further processing step is incorporated. This involves multiplying (or modulating) voxel values in the segmented images by the Jacobian determinants derived from the spatial normalization step. In effect, an analysis of modulated data tests for regional differences in the absolute amount (volume) of grey matter, whereas analysis of unmodulated data tests for regional differences in concentration of grey matter (per unit volume in native space) (Ashburner and Friston, 2000).

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc2.6">2.6 Smooth</a>
The normalized, segmented images are smoothed using a 12-mm FWHM isotropic Gaussian kernel. This conditions the data to conform more closely to the Gaussian field model underlying the statistical procedures used for making inferences about regionally specific effects. Smoothing also has the effect of rendering the data more normally distributed (by the central limit theorem). The intensity in each voxel of the smoothed data is a locally weighted average of grey matter density from a region of surrounding voxels, the size of the region being defined by the size of the smoothing kernel (Ashburner and Friston, 2000).

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
