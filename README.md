# Covid-pnemonia-detection
 ## Objective :
 - Identify the presence of COVID-19 or Pneumonia in a patient using X-ray or CT-Scan images just after scanning the patient's chest.
 - Achieve State-of-the-art accuracy
## Datasts : 
 - X-ray - Dataset 1 : [Paper-dataset](https://data.mendeley.com/datasets/jctsfj2sfn)
 - X-ray - Dataset 2 : [Kaggle-dataset](https://www.kaggle.com/datasets/prashant268/chest-xray-covid19-pneumonia)
 - CT-Scan - Dataset 1 - Missing full training : [Paper-dataset](https://www.kaggle.com/datasets/azaemon/preprocessed-ct-scans-for-covid19)
 - CT-Scan - Dataset 2 : - training not done [Kaggle-dataset](https://www.kaggle.com/datasets/azaemon/preprocessed-ct-scans-for-covid19)

## Milestones
  - Phase 1 : X-ray
    - [x] Training on X-ray images
    - [X] Multiple models
    - [X] Upload models - Inference
    - [ ] Fine tuning - achieved 95.6%
  - Phase 2 : CT-Scan
    - [X] Training on CT-Scan images
    - [ ] Multiple models
    - [ ] Upload models - Inference
    - [ ] Fine tuning
  - Final Phase : 
    - [ ] open-source Model Weights
    - [ ] Build pipeline for both X-ray and CT-Scan
    - [ ] Build a web-app 


## Models
### X-ray 
- [X] CNN
- [X] CNN-LSTM

[![Models in action](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1SPHSru68p8rQPxAGH6aYeywpwrjtjDs-?usp=sharing)


- Extra-model
  - [X] CNN-GRU
  
   <a href="https://www.kaggle.com/code/andrewnaaem/cnn-gru-98-9-accuracy?scriptVersionId=116692637"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open In Kaggle"></a>
### CT-Scan
- [x] CNN-LSTM
- [ ] CNN-wavelet-SE



