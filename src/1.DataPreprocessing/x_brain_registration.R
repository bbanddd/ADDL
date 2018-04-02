library("ANTsR")
library("extrantsr")
library("oro.nifti")

args = commandArgs(TRUE)
input_nii  = args[1]
output_nii = args[2]

template_file = "./template_GM_init.nii.gz"
ants_regwrite(input_nii, retimg=FALSE, outfile=output_nii, template.file=template_file, typeofTransform ="SyN", verbose=FALSE)

