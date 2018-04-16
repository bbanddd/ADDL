<a id="toc_top"></a>
[*English Version*](#top_intr_en), [*中文版本*](#top_intr_cn)

----

# <a id="top_intr_en">ADDL</a>

ADDL is an open source project, AD means Alzheimer' disease and DL means deep learning. It applies deep learning techniques on the brain MRI images data for the Alzheimer's disease diagnostic.

## [ADDL Installation](docs/install.md)
 Because the ADDL project wraps a lot of 3rd party tools and works as a script, the installation of ADNI is very easy, just source copy. But the 3rd party tools setting up cost a lot. Please refer to the [install](docs/install.md) for the detail information.

## [ADNI Access](docs/ADNI_data_access.md)
The ADDL study requires plenty of AD MRI data, we get it from the ADNI database. Please check the [ADNI access](docs/ADNI_data_access.md) for the detail information.

## [ADDL Workflow](docs/workflow.md)
The ADDL project bases on structural MRI (T1, 2017) data of Alzheimer's disease(AD) and non-Alzheimer's disease(NL) subjects of ADNI. It takes ResNet DL module to learn the brain gray matter(GM) tissue images obtained through preprocessing, and applies diagnostic algorithm on the ResNet module inference results for the AD diagnostic. The detail ADDL pipeline information please refer to [ADDL Workflow](docs/workflow.md).

## [ADDL Study](docs/study.md)
Try to get higher AD diagnostic precision, we group the ADNI MRI data into several study groups, design different diagnostic methodologies, and apply ADDL pipeline. Specially, we get about 95% AD diagnostic precision. Please get the detail information from [ADDL study document](docs/study.md).

## [ADDL Basic Knowledge](docs/basic.md)
The ADDL is a cross subjects project, such as medical, statistic, deep learning etc. It is hard to get all the knowledge for an engineer. The [ADDL Basic Knowledge](docs/basic.md) tries to give a brief introduction for the notions involved in the ADDL project.

----
[<p align='right'>*返回顶部*</p>](#toc_top)

# <a id="top_intr_cn">ADDL</a>
ADDL是一个开源项目，AD是指阿尔兹海默症，DL是指深度学习。ADDL利用深度学习技术，分析大脑的核磁共振影像数据，实现阿尔兹海默症的诊断。

## [ADDL 安装](docs/安装.md)
因为ADDL项目需要许多第三方工具，是一个基于脚本的项目，所以ADDL的安装非常简单，通过源代码复制即可实现。但是，第三方工具的安装非常复杂，详细信息请参考文档[ADDL 安装](docs/安装.md)。

## [ADNI 数据获取](docs/ADNI数据获取.md)
ADDL的研究工作需要大量AD患者的MRI数据，我们从ADNI数据库中获取这些数据。详细信息请参考文档[ADNI 数据获取](docs/ADNI数据获取.md)。

## [ADDL 工作流程](docs/工作流程.md)
ADDL项目基于ADNI中AD患者和非AD(NL)被试人员的结构MRI数据（T1, 2017年）。它利用由预处理过程获得的大脑灰质（GM）组织的影像数据训练ResNet深度学习模型，应用诊断算法分析ResNet模型的推理结果，实现阿尔兹海默症的诊断。详细的ADDL流程请参考文档[ADDL 工作流程](docs/工作流程.md)。

## [ADDL 研究](docs/研究.md)
为了获得更高的AD诊断精度，我们将ADNI数据分成一些研究组，设计不同的诊断方法，并使用ADDL处理数据。特别的是，我们得到95%的AD诊断精度。请参考[ADDL 研究](docs/研究.md)文档以获得详细信息。

## [ADDL 基础知识](docs/基础.md)
ADDL项目涵盖许多学科，比如医学，统计学，深度学习等等。对工程师而言很难了解全部知识。[ADDL 基础知识](docs/基础.md)试图对项目中涉及的概念给出简单的介绍。

----
