# Sentiment-Foody

Framework: Pytorch

Full folder at: [Notion site](https://drive.google.com/drive/folders/1iW6nos7wXvQXtYfZ3s9di6GpEWtBj8ez?usp=share_link)

**Model list**

- [x] SVM
- [x] PhoBERT
- [x] XLM-R

## Dataset

[FOODY](https://www.kaggle.com/competitions/int3405-sentiment-analysis-problem/data)


### Training

Loss function: Cross Entropy

Optimizers: AdamW

Batch size: 8

Gradient Accumulation steps: 5

Learning rate: 3e-5

Warmup ratio: 0.1

Weight decay: 1e-2

Epoch: 3

### Quickstart

Firstly, you need to install all the required dependencies:

```
pip install -r requirements.txt
```
Secondly, you need to go to this [link](https://drive.google.com/drive/folders/1-8TKnViF6LaJMWivjyaiPplVQppwP96E?usp=share_link) and download data

### How to train

SVM: Run file SVM.ipynb
Fine-tune: Run file Finetune.ipynb

### How to infer

Run file Inference.ipynb
