# 2024_Chosun_osp_Deepfake-detection challenge

## Table of Contents

- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick run](#quick-run)
  - [The whole pipeline](#the-whole-pipeline)
- [Train](#Train)
  - [Training a single model](#Training_a_single_model)
- [Test](#Test)
  - [Pretrained weights](#Pretrained_weights)
- [Datasets](#Datasets)
- [References](#References)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About The Project

This project is a deepfake detection challenge project conducted by the Chosun University open source SW project.

이 프로젝트는 조선대학교 오픈소스SW 프로젝트에서 진행되는 딥페이크 탐지 챌린지 프로젝트입니다.


### Built With

- Python 3.10 64-bit
- Django 5.1.2
- EfficientNet b0
- ConvNext Tiny
- MTCNN (전처리)
- BCEWithLogitsLoss (손실 함수)

## Getting Started

Setup description

## Prerequisites

- Install [conda](https://docs.conda.io/en/latest/miniconda.html)
- Create the  environment with *environment.yml*
```
$ conda env create -f environment.yml
```
- Download and unzip the [datasets](https://drive.google.com/drive/folders/18qY34tdNIlYppLn1RmkdqlNsQh8QLKnj?usp=sharing)


## Quick run

If you just want to test the pre-trained models against your own videos or images:

- [Video prediction notebook]( )
- [Image prediction notebook](https://colab.research.google.com/drive/1VRgV_5KhA8EZp0gQ6FNFki2GBGrAFAKO?usp=sharing)
- [Image prediction with attention](https://colab.research.google.com/drive/1WFjqiLt1spXsaSo5CfAxeLZoZGLQIxBo?usp=sharing)

## The whole pipeline

## Pipeline Overview
- Model: EfficientNet b0, ConvNext Tiny
- Preprocessing: MTCNN for face extraction
- Loss Function: BCEWithLogitsLoss
```
$ ./
```



## Train
## Training a single model

If you want to train some models without lunching the script:

- [Training Notebook](https://colab.research.google.com/drive/17sQ3D3lnErrER7Tn8IVk_LhFIagQgSZB?usp=sharing)
  
## Test

## Pretrained weights
We provide pretrained weights for all the architectures presented in the project. 
Please refer to this [Google Drive link](https://drive.google.com/drive/folders/1UyjNHiUvE3yQG9Mq9hqvLXkuFlYp3-lq?usp=sharing)

## Datasets

- [Deepfake Detection Challenge_(DFDC) train test_dataset](https://www.kaggle.com/competitions/deepfake-detection-challenge/data) | [arXiv paper](https://arxiv.org/abs/2006.07397)


## References

- [EfficientNet PyTorch](https://github.com/lukemelas/EfficientNet-PyTorch)
- [ConvNext-Tiny PyTorch](https://pytorch.org/vision/main/models/generated/torchvision.models.convnext_tiny.html)

## How to cite

Plain text:

```

```





## Contact


Yoon Hyejun -  [hj021313@gmail.com](hj021313@gmail.com)

Kim Minseo - [iminseo031224@gamil.com](iminseo031224@gmail.com)

Kim Serin - [qnsghdakf8@gmail.com](qnsghdakf8@gmail.com)

Project Link: [link to the project](https://leaf-geography-00e.notion.site/10e21cb154db809fa334d48c83df050e)

## Acknowledgements

- List of open source codes used within the project
