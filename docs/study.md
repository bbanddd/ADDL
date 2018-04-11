# Introduction
Try to get higher AD diagnostic precision, we group the ADNI MRI data into several study groups, designed different diagnostic methodology, and apply ADDL pipeline. Specially, we get about 95% AD diagnostic precision.

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

**Data List**<br>
The ADDL project stores the `ADNI_1.5T_All_AD_NL` group as an example, that is named  [Rule1_ADNI_1.5T_All_AD_NL](..\examples\Rule1_ADNI_1.5T_All_AD_NL).
* `dataList_ADNI_1.5T_All_AD_NL.dat` is the data list of `ADNI_1.5T_All_AD_NL` study group.
* `dataList_ADNI_1.5T_All_AD_NL_test.dat` is the training data lit, used for DL module training.
* `dataList_ADNI_1.5T_All_AD_NL_train.dat` is the validation data list, used for diagnostic.
* `labels_ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX.dat` is the training data label, used for DL module training.

## `ADNI_1.5T_All_AD_NL_Scale2`
Besides baseline data selection, for each data that has a
‘Scale_2’ version, the corresponding ‘Scale’ version is removed. The phantom scaling of ['Scale_2'](http://adni.loni.usc.edu/scaled-2-uploads/) is more reliable.

**Data List**<br>
The ADDL project stores the `ADNI_1.5T_All_AD_NL` group as an example, that is named  [Rule2_ADNI_1.5T_All_AD_NL_Scale2](..\examples\Rule2_ADNI_1.5T_All_AD_NL_Scale2).
* `dataList_ADNI_1.5T_All_AD_NL_Scale2.dat` is the data list of `ADNI_1.5T_All_AD_NL_Scale2` study group.
* `dataList_ADNI_1.5T_All_AD_NL_Scale2_test.dat` is the training data lit, used for DL module training.
* `dataList_ADNI_1.5T_All_AD_NL_Scale2_train.dat` is the validation data list, used for diagnostic.
* The label please reference to the `Rule1_ADNI_1.5T_All_AD_NL` label, which is the full set of all the study groups.

## `ADNI_1.5T_All_AD_NL_Scale2_LessNL`
Based on ADNI_1.5T_All_AD_NL_Scale2, about half of the NL data are removed.

**Data List**<br>
The ADDL project stores the `ADNI_1.5T_All_AD_NL` group as an example, that is named  [Rule3_ADNI_1.5T_All_AD_NL_Scale2_LessNL](..\examples\Rule3_ADNI_1.5T_All_AD_NL_Scale2_LessNL).
* `dataList_ADNI_1.5T_All_AD_NL_Scale2_LessNL.dat` is the data list of `ADNI_1.5T_All_AD_NL_Scale2_LessNL` study group.
* `dataList_ADNI_1.5T_All_AD_NL_Scale2_LessNL_test.dat` is the training data lit, used for DL module training.
* `dataList_ADNI_1.5T_All_AD_NL_Scale2_LessNL_train.dat` is the validation data list, used for diagnostic.
* The label please reference to the `Rule1_ADNI_1.5T_All_AD_NL` label, which is the full set of all the study groups.

## `ADNI_1.5T_All_AD_NL_FilterScores`
Besides applying common rules. For each subject, if one if its data record's cognition testing score, CDRSB, ADAS11 or MMSE, is not resides in a given range, the whole subject is removed.

||NL Low|NL High|AD Low|AD High|
|:----:|:----:|:----:|:----:|:----:|
|CDR-SB|-0.096|0.156|2.811|6.203|
|ADAS 11|2.8|8.8|13.7|27.9|
|MMSE|27.9|30.3|21|25.2|

**Data List**<br>
The ADDL project stores the `ADNI_1.5T_All_AD_NL` group as an example, that is named  [Rule4_ADNI_1.5T_All_AD_NL_FilterScores](..\examples\Rule4_ADNI_1.5T_All_AD_NL_FilterScores).
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores.dat` is the data list of `ADNI_1.5T_All_AD_NL_FilterScores` study group.
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores_test.dat` is the training data lit, used for DL module training.
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores_train.dat` is the validation data list, used for diagnostic.
* The label please reference to the `Rule1_ADNI_1.5T_All_AD_NL` label, which is the full set of all the study groups.

## `ADNI_1.5T_All_AD_NL_FilterScores_Scale2`
'Scaled_2' version of ADNI_1.5T_All_AD_NL_FilterScores.

**Data List**<br>
The ADDL project stores the `ADNI_1.5T_All_AD_NL_FilterScores_Scale2` group as an example, that is named  [Rule5_ADNI_1.5T_All_AD_NL_FilterScores_Scale2](..\examples\Rule5_ADNI_1.5T_All_AD_NL_FilterScores_Scale2).
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores_Scale2.dat` is the data list of `ADNI_1.5T_All_AD_NL_FilterScores_Scale2` study group.
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores_Scale2_test.dat` is the training data lit, used for DL module training.
* `dataList_ADNI_1.5T_All_AD_NL_FilterScores_Scale2_train.dat` is the validation data list, used for diagnostic.
* The label please reference to the `Rule1_ADNI_1.5T_All_AD_NL` label, which is the full set of all the study groups.

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

----

# Results
**Default subject level test results**<br>

||Data Selection 1|Data Selection 2|Data Selection 3|Data Selection 4|Data Selection 5|
|:----:|:----:|:----:|:----:|:----:|:----:|
|P|122|107|107|69|53|
|N|145|116|77|41|35|
|TP|90|81|93|67|53|
|TN|130|105|67|31|24|
|FP|15|11|10|10|11|
|FN|32|26|14|2|0|
|TPR|73.77%|75.70%|86.92%|97.10%|100.00%|
|TNR|89.66%|90.52%|87.01%|75.61%|68.57%|
|FPR|10.34%|9.48%|12.99%|24.39%|31.43%|
|FNR|26.23%|24.30%|13.08%|2.90%|0.00%|
|ACC|82.40%|83.41%|86.96%|89.09%|87.50%|

The rows means list:
* *P* positive samples
* *N* negative samples
* *TP* true positive
* *TN* true negative
* *FP* false positive
* *FN* false negative
* *TPR* true positive rate
* *TRN* true negative rate (SPC)
* *FPR* false positive rate
* *FNR* false negative rate
* *ACC* accuracy


**subject level test results, strategy variation, N = 32**<br>

||Data Selection 1|Data Selection 2|Data Selection 3|Data Selection 4|Data Selection 5|
|:----:|:----:|:----:|:----:|:----:|:----:|
|TPR|77.87%|74.77%|83.18%|98.55%|96.23%|
|TNR|95.17%|95.69%|94.81%|87.80%|94.29%|
|FPR|4.83%|4.31%|5.19%|12.20%|5.71%|
|FNR|22.13%|25.23%|16.82%|1.45%|3.77%|
|ACC|87.27%|85.65%|88.04%|94.55%|95.45%|

----

# Conclusions
1.	Overall accuracy increases if training set has more AD data than NL. For example, data selection 3 AD/NL = 1.43, data selection 4 AD/NL = 1.58. (One possible reason is that the information for classifying the image as AD occupies only a little part of the image.) This is observed in ADNI 1.5T dataset, further verification is needed to verify other datasets.
1.	Performance increases when making use of some medical knowledge.
1.	The results of dataset 4 and 5 are for reference, it is possible that their results are not reliable due to small amount of data.
