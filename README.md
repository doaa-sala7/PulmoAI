## Pulmo AI : Automatic Covid Detection 
Pulmo AI : Is a web application that is build on a machine learning research, in which we implmented various deep learning  classification models to detect Pneumonia and Covid from Xray and CT images

### Overview
- Walkthrough of the application
<video width="630" height="300" src="https://github.com/Andrew2077/PulmoAI/blob/main/Pulmo-AI/static/WalkThrough.mp4"></video>

## Table of Contents
- [Pulmo AI : Automatic Covid Detection](#pulmo-ai--automatic-covid-detection)
  - [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [installation - Conda](#installation---conda)
## Features 
- Multiple AI modalities 
- Firendly User Interface - Web Application
- Database integration
- Real time prediction [Strong GPU required]
- Easy to use

## installation - Conda
- clone the repo
  ```bash
  git clone https://github.com/Andrew2077/PulmoAI/tree/main/Pulmo-AI.git
  ```
- Create a Conda Environment - this will take a while
  ```bash
  conda env create -f environment.yml
  ```
- Activate the environment - name : pulmoai
  ```bash
  conda activate pulmoai
  ```
- Navigate to the Pulmo-AI directory
  ```bash
  python app.py
  ```