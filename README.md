# 2024_Chosun_osp_Deepfake-detection challenge

## Table of Contents

- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick run](#quick-run)
  - [The whole pipeline](#the-whole-pipeline)
- [License](#license)
- [Changelog](#changelog)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About The Project

This project is a deepfake detection challenge project conducted by the Chosun University open source SW project.

이 프로젝트는 조선대학교 오픈소스SW 프로젝트에서 진행되는 딥페이크 탐지 챌린지 프로젝트입니다.


### Built With

- Python 3.12.2 64-bit
- 

## Getting Started

Setup description

## Prerequisites

- Install [conda](https://docs.conda.io/en/latest/miniconda.html)
- Create the  environment with *environment.yml*

```
$ conda env create -f environment.yml
$
```

- Download and unzip the [datasets](https://www.kaggle.com/c/deepfake-detection-challenge/data)

## Quick run

If you just want to test the pre-trained models against your own videos or images:

- [Video prediction notebook]( )
- [Image prediction notebook]( )
- [Image prediction with attention]( )

## The whole pipeline

```
$ ./
```

Also, please note that **for the DFDC** we have resorted to *the training split* exclusively!

In `scripts/make_dataset.sh` the value of `DFDC_SRC` should point to the directory containing the DFDC train split.

## Celeb-DF (v2)

Altough **we did not use this dataset in the paper**, we provide a script [index_celebdf.py]( ) to index the videos similarly to DFDC and FF++. Once you have the index, you can proceed with the pipeline starting from [extract_faces.py]( ). You can also use the split `celebdf` during training/testing.

## Train

## Training a single model

If you want to train some models without lunching the script:

- 
- 
    1. 
    2. 

## Test

## Pretrained weights

We also provide pretrained weights for all the architectures presented in the paper. Please refer to this [Google Drive link]( ). Each directory is named `$NETWORK_$DATASET` where `$NETWORK` is the architecture name and `$DATASET` is the training dataset. In each directory, you can find `bestval.pth` which are the best network weights according to the validation set.

Additionally, you can find Jupyter notebooks for results computations in the [notebook]( ) folder.

## Datasets

- [Facebook's DeepFake Detection Challenge (DFDC) train dataset](https://www.kaggle.com/c/deepfake-detection-challenge/data) | [arXiv paper](https://arxiv.org/abs/2006.07397)
- [FaceForensics++](https://github.com/ondyari/FaceForensics/blob/master/dataset/README.md) | [arXiv paper](https://arxiv.org/abs/1901.08971)
- [Celeb-DF (v2)](http://www.cs.albany.edu/~lsw/celeb-deepfakeforensics.html) | [arXiv paper](https://arxiv.org/abs/1909.12962) (**Just for reference, not used in the paper**)

## References

- [EfficientNet PyTorch](https://github.com/lukemelas/EfficientNet-PyTorch)
- [Xception PyTorch](https://github.com/tstandley/Xception-PyTorch)

## How to cite

Plain text:

```

```

## Credits



## License

Information about the license.
For more information about he license see the `LICENSE.md` file.

## Changelog

All notable changes to this project will be documented
in [CHANGELOG.md](https://gitlab.rackhost.hu/rackhost/wp-tudasbazis/-/blob/master/README.md).



## Contact


Yoon Hyejun -  [hj021313@gmail.com](hj021313@gmail.com)

Kim  - 

Kim  -

Project Link: link to the project

## Acknowledgements

- List of open source codes used within the project
