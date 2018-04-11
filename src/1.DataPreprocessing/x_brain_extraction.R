library("ANTsR")
library("extrantsr")
library("oro.nifti")

args = commandArgs(TRUE)
input_nii  = args[1]
output_nii = args[2]


template_dir = "/usr/local/fsl/data/standard"
template_file = file.path(template_dir, "MNI152_T1_1mm.nii.gz")
template_mask = file.path(template_dir, "MNI152_T1_1mm_brain_mask.nii.gz")
template_aimg = antsImageRead(template_file, dimension = 3)
template_mask_aimg = antsImageRead(template_mask, dimension = 3)

aimg = antsImageRead(input_nii, dimension = 3)
brain_aimg = abpBrainExtraction(img = aimg, tem = template_aimg, temmask = template_mask_aimg)

brain_nii = ants2oro(brain_aimg$brain)
writeNIfTI(brain_nii, filename=output_nii)

