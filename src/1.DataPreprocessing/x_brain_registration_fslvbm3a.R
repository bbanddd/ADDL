library("ANTsR")
library("extrantsr")
library("oro.nifti")

args = commandArgs(TRUE)
input_nii  = args[1]
output_nii = args[2]


template_file = "./template_GM.nii.gz"

aimg_template = antsImageRead(template_file, dimension=3)
aimg_input    = antsImageRead(input_nii    , dimension=3)

aimg_reg = antsRegistration(fixed=aimg_template, moving=aimg_input, typeofTransform="SyN")
aimg_jac = createJacobianDeterminantImage(aimg_template, aimg_reg$fwdtransforms[[1]],1)

img_reg = ants2oro(aimg_reg$warpedmovout)
img_jac = ants2oro(aimg_jac)

output_jac_nii = paste(output_nii, "_JAC_nl", sep="")
writeNIfTI(img_reg, output_nii)
writeNIfTI(img_jac, output_jac_nii)
