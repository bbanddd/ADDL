# <a id="toc_content">Content</a>
1. [Introduction](#toc1)
   1. [Abbreviation](#toc1.1)
1. [Basic](#toc2)
   1. [Brain Anatomy](#toc2.1)
   1. [Structural MRI](#toc2.2)
      1. [Measurement](#toc2.2.1)
      1. [Analysis](#toc2.2.2)
      1. [Limitation](#toc2.2.3)
      1. [Acquisition Tips](#toc2.2.4)
   1. [Theoretical Foundations of Brain Registration](#toc2.3)
      1. [Space](#toc2.3.1)
         1. [Coordinate Systems](#toc2.3.1.1)
         1. [Native Space and Standard Spaces](#toc2.3.1.2)
      1. [Spatial Transformations](#toc2.3.2)
      1. [Transformation Model](#toc2.3.3)
      1. [Cost Functions](#toc2.3.4)
      1. [Interpolation](#toc2.3.5)
      1. [Atlases and Templates](#toc2.3.6)
         1. [The Talairach Atlas](#toc2.3.6.1)
         1. [The MNI Templates](#toc2.3.6.2)
   1. [Theoretical Foundations of Brain Segmentation](#toc2.4)
      1. [Likelihood or Observation Models](#toc2.4.1)
         1. [Parameter and Non-parameter Model](#toc2.4.1.1)
         1. [Finite Mixture Model](#toc2.4.1.2)
         1. [Hidden Markov Random Field Model](#toc2.4.1.3)
      1. [Prior Probability Models](#toc2.4.2)
         1. [Generalized MRF Prior](#toc2.4.2.1)
         1. [Template-base Priors](#toc2.4.2.2)
      1. [Optimization of Maximizing Posterior Probability](#toc2.4.3)
         1. [Atropos](#toc2.4.3.1)
         1. [HMRF-EM](#toc2.4.3.2)
   1. [Deep Learning Suits](#toc2.5)
1. [ADDL](#toc3)
   1. [ADNI Subjects](#toc3.1)
   1. [Preprocessing](#toc3.2)
      1. [Brain Extraction](#toc3.2.1)
      1. [Grey Matter Segmentation](#toc3.2.2)
      1. [Template Creation](#toc3.2.3)
      1. [Spatial Normalization](#toc3.2.4)
      1. [Correction for Volume Changes (Modulation)](#toc3.2.5)
      1. [Smoothing](#toc3.2.6)
   1. [Training and Validation Group](#toc3.3)
   1. [ResNet Module](#toc3.4)
   1. [Diagnostic Algorithm](#toc3.5)
1. [Reference](#toc4)

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc1">1 Introduction</a>

# <a id="toc3">3 ADDL</a>
The ADDL project is based on structural MRI (T1, 2017) data of Alzheimer's disease(AD) and non-Alzheimer's disease(NL) subjects in ADNI. It uses ResNet module to learn the brain gray matter(GM) tissue images obtained through preprocessing, and combines diagnostic algorithms to achieve The diagnosis of AD, with a diagnostic accuracy of more than 87%.

![](images/sc_wp_addl_flow_en.png)

The ADDL project includes four processes: preprocessing, grouping, training and diagnosis. In the pre-process, the structural MRI (T1) data of all the subjects in the study group were segmented and registered to obtain the gray matter image. The grouping process divides the subjects in the study group into a training set and a validation set. The training process is to input training set data into ResNet model training. In the diagnosis process, the gray matter image of a subject in the test group is input into the trained ResNet model, and a diagnostic algorithm is applied to determine whether the subject suffers from Alzheimer's disease.

This chapter introduces the algorithms used in ADDL from five aspects: ADNI subjects, preprocessing, grouping, ResNet model, and diagnostic algorithm.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.1">3.1 ADNI Subjects</a>
TBD, integrate the previous spreadsheet.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.2">3.2 Preprocessing</a>
The preprocessing applies the segmentation algorithm to the original structure MRI image (T1) data of all the subjects to obtain the GM tissue, and transforms the GM data in native space  base on the same template to the spatial space. With respect to segmentation, the brain tissues (GM/WM) were extracted and segmented using the ANTsR tool from the original structural MRI data of all subjects; then the GM obtained from the previous section was extracted using the FAST tool. With regard to registration, a study registration template is first generated based on the GM template of the ICBM-152 GM template of all the subjects; then the generated template is used to spatial transformation of GM in native space into a new spatial space; then a modulation process holds the volume of each voxel after the registration; finally step is the smoothing process.

This section will introduce the six parts of the preprocessing process, brain extraction, GM segmentation, template creation, spatial transformation normalization, voxel volume modulation, and smoothing.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.1">3.2.1 Brain Extraction</a>
This is a fully automated procedure to remove scalp tissue, skull, and dural venous sinus voxels. This procedure initially involves segmentation of the original structural MR images (in native space) into grey and white matter images, followed by a series of fully automated morphological operations for removing unconnected non-brain voxels from the segmented images (erosion followed by conditional dilation). The resulting images are extracted grey and white matter partitions in native space.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.2">3.2.2 Grey Matter Segmentation</a>
Scans were then segmented into grey matter, white matter, CSF, and other nonbrain partitions. SPM segmentation employs a mixture model cluster analysis to identify voxel intensities matching particular tissue types (grey matter, white matter and CSF) combined with an a priori knowledge of the spatial distribution of these tissues in normal subjects, derived from probability maps. The segmentation step also incorporates an image intensity nonuniformity correction (Ashburner and Friston, 2000) to address image intensity variations caused by different positions of cranial structures within the MRI head coil.

Scans were then segmented into grey matter, white matter, CSF, and other nonbrain partitions. SPM segmentation employs a mixture model cluster analysis to identify voxel intensities matching particular tissue types (grey matter, white matter and CSF) combined with an a priori knowledge of the spatial distribution of these tissues in normal subjects, derived from probability maps. The segmentation step also incorporates an image intensity nonuniformity correction (Ashburner and Friston, 2000) to address image intensity variations caused by different positions of cranial structures within the MRI head coil.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.3">3.2.3 Template Creation</a>
First, an anatomical template was created from a subgroup of all normal subjects with a mean age and age range matched to the entire study group imaged on the same MRI scanner with the same scanning parameters, in order to reduce any scanner-specific bias and provide a template appropriate to the population sample. This involves spatially normalizing each structural MRI to the ICBM-152 template (Montreal Neurological Institute), which is derived from 152 normal subjects and approximates the Talairach space. The normalized data are then smoothed with an 8-mm full-width at half-maximum (FWHM) isotropic Gaussian kernel, and a mean image (the template) is created.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.4">3.2.4 Spatial Normalization</a>
All subjects' structural MRI scans (in native space) were transformed to the same stereotactic space by registering each of the images to the same template image, using the residual sum of squared differences as the matching criterion(lose function). The first step in spatial normalization involves estimating the optimum 12-parameter affine transformation to match images (Ashburner et al., 1997). A Bayesian framework is used, whereby the maximum a posteriori (MAP) estimate of the spatial transformation is made using prior knowledge of the normal variability in brain size. The second step accounts for global non-linear shape differences, which are modeled by a linear combination of smooth spatial basis functions (Ashburner and Friston, 1999). A masking procedure is used to weight the normalization to brain rather than nonbrain tissue. The spatially normalized images are resliced with a final voxel size of approximately![LATEX:1.5\times1.5\times1.5\, mm^3](http://latex.codecogs.com/gif.latex?1.5%5Ctimes1.5%5Ctimes1.5%5C%2C%20mm%5E3).

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.5">3.2.5 Correction for Volume Changes (Modulation)</a>
As a result of nonlinear spatial normalization, the volumes of certain brain regions may grow, whereas others may shrink. In order to preserve the volume of a particular tissue (grey or white matter or CSF) within a voxel, a further processing step is incorporated. This involves multiplying (or modulating) voxel values in the segmented images by the Jacobian determinants derived from the spatial normalization step. In effect, an analysis of modulated data tests for regional differences in the absolute amount (volume) of grey matter, whereas analysis of unmodulated data tests for regional differences in concentration of grey matter (per unit volume in native space) (Ashburner and Friston, 2000).

----
[<p align='right'>*Back to Content*</p>](#toc_content)

### <a id="toc3.2.6">3.2.6 Smoothing</a>
The normalized, segmented images are smoothed using a 12-mm FWHM isotropic Gaussian kernel. This conditions the data to conform more closely to the Gaussian field model underlying the statistical procedures used for making inferences about regionally specific effects. Smoothing also has the effect of rendering the data more normally distributed (by the central limit theorem). The intensity in each voxel of the smoothed data is a locally weighted average of grey matter density from a region of surrounding voxels, the size of the region being defined by the size of the smoothing kernel (Ashburner and Friston, 2000).

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.3">3.3 Training and Validation Group</a>
All the subjects are grouped as training and validation two sets, that the training set is used for update ResNet module parameters, but the validation set will never attend the ResNet training process. If training set subject attend diagnostic process, it will be 100% accuracy. Keeping the AD and non-AD subjects and data ratio with the same distribution in the training and validation sets to avoid the bias, considering the subjects visited number are different in ADNI, ADNI involved the group tools base on statistics data of subjects, (and the AD and non-AD ratio is configurable.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.4">3.4 ResNet Module</a>
TBD: Introduction the detail of resnet module.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

## <a id="toc3.5">3.5 Diagnostic Algorithm</a>
The output of ResNet module of the diagnostic process are a vector of labels, which reflect the AD predication values of images along the Z axon. Considering the different GM location or the tissue connection might indication the AD features, for better accuracy we weighted each element of the label vector as the quantity of diagnostic.

----
[<p align='right'>*Back to Content*</p>](#toc_content)

# <a id="toc4">4 Reference</a>
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
