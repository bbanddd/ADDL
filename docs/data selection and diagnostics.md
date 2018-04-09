# Data Selection
The data selection groups ADNI data into several study groups, which helps find the AD features by crossing comparing AD diagnostic results of study groups. Base on different methodologies, we groups the ADNI data into following five groups.
1. `ADNI_1.5T_All_AD_NL`
1. `ADNI_1.5T_All_AD_NL_Scale2`
1. `ADNI_1.5T_All_AD_NL_Scale2_LessNL`
1. `ADNI_1.5T_All_AD_NL_FilterScores`
1. `ADNI_1.5T_All_AD_NL_FilterScores_Scale2`

**Subjects Counts of Groups**<br>

|Index|Group Count|NL Subjects|AD Subjects|Total Subjects|
|:----:|:----:|:----:|:----:|:----:|
|1|ADNI_1.5T_All_AD_NL|158|184|342|
|2|ADNI_1.5T_All_AD_NL_Scale2|158|184|342|
|3|ADNI_1.5T_All_AD_NL_Scale2_LessNL|95|184|279|
|4|ADNI_1.5T_All_AD_NL_FilterScores|45|98|143|
|5|ADNI_1.5T_All_AD_NL_Scale2_LessNL_Scale2|45|98|143|

**NIFTI/Images Counts of Groups**<br>

|Index|Group Count|NL NIFTIs|AD NIFTIs|Total NIFTIs|
|:----:|:----:|:----:|:----:|:----:|
|1|ADNI_1.5T_All_AD_NL|740|643|1372|
|2|ADNI_1.5T_All_AD_NL_Scale2|637|542|1179|
|3|ADNI_1.5T_All_AD_NL_Scale2_LessNL|380|542|922|
|4|ADNI_1.5T_All_AD_NL_FilterScores|212|334|546|
|5|ADNI_1.5T_All_AD_NL_Scale2_LessNL_Scale2|179|287|466|

**Training and Validation Group**<br>
Note the training and validation groups requires for the DL module. For each study group, 80% of the images of both of AD and NL class are chosen for training, and the rest 20% are for validation. One subject, together with his/her images of all visits, appear in only training or validation group.

## `ADNI_1.5T_All_AD_NL`
Select pure AD and NL subjects as a group without MCI subjects and subject who transfer AD from NL. This is the baseline of following data selection.

**Detail Process**<br>
1. Remove subjects with non-uniform diagnose information (DX), excluding subjects whose DX changes among visits, for example NL->MCI->AD.
1. Remove subjects with all empty diagnose information (DX).
1. Remove subjects with diagnose information (DX) being MCI.
1. For each subject, if its diagnose information (DX) is empty, infer its diagnose information (DX) according to the following rules.
   1. If diagnose information (DX) of the first visit (VISCODE = bl) is AD, all diagnose information (DX) of subsequent visits are AD.
   1. If the last non-empty diagnose information (DX) is NL, all diagnose information (DX) before that visit are NL.
1. Remove all data records with empty diagnose information (DX).

## `ADNI_1.5T_All_AD_NL_Scale2`
Besides baseline data selection, for each data that has a
‘Scale_2’ version, the corresponding ‘Scale’ version is removed. The phantom scaling of ['Scale_2'](http://adni.loni.usc.edu/scaled-2-uploads/) is more reliable.
## `ADNI_1.5T_All_AD_NL_Scale2_LessNL`
Based on ADNI_1.5T_All_AD_NL_Scale2, about half of the NL data are removed.
## `ADNI_1.5T_All_AD_NL_FilterScores`
Besides applying common rules. For each subject, if one if its data record's cognition testing score, CDRSB, ADAS11 or MMSE, is not resides in a given range, the whole subject is removed.

||NL Low|NL High|AD Low|AD High|
|:----:|:----:|:----:|:----:|:----:|
|CDR-SB|-0.096|0.156|2.811|6.203|
|ADAS 11|2.8|8.8|13.7|27.9|
|MMSE|27.9|30.3|21|25.2|

## `ADNI_1.5T_All_AD_NL_FilterScores_Scale2`
'Scaled_2' version of ADNI_1.5T_All_AD_NL_FilterScores.

----

# Diagnostics
The last stage of ADDL inference process is diagnostics, which basing on the DL module inference result vector get the diagnostics result. Each element of the results vector indicate the AD classification result by the DL module of a 2D image along the Z axe. Considering the tissue spatial allocation, weight of location etc, we designed several strategies for the final diagnostics.


## Numbers
Base on the number comparing between AD and NL is the most directly method, that is the baseline of all the strategies.

```
if number_of_AD_png > number_of_NL_png:
		subject_class = AD
else:
		subject_class = NL

```

## Continuous
To mitigate the impact of single PNG result, we get continuous stragegy.

```
if there exists continuous N AD png:
	subject_class = AD
else:
	subject_class = NL

```

This strategy gets different N in different data selections, and overall accuracy is better than baseline strategy in only data selection 1.

## Low Z Location
According to medical research, hippocampus tends to show the most rapid loss of tissue earliest in Alzheimer’s disease. Only bottom N PNG files are checked instead of all in baseline strategy.

```
In the bottom N PNG files:
if number_of_AD_png > number_of_NL_png:
		subject_class = AD
else:
		subject_class = NL

```

This strategy has a common N in different data selections. Although not all data selections achieve the best overall accuracy under this N, all get better performance than baseline strategy.

# Results
**Default**<br>


**example**<br>
