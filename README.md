
# <p ><img src="Pulmo-AI\static\assets\img\lungs.ico" alt="Icon" width="30" height="30"> Pulmo AI : Automatic Covid & Pneumonia Detection </p> 
**Pulmo AI**: Step into the world of cutting-edge technology with our web application. Built upon groundbreaking machine learning research, we've harnessed the power of diverse deep learning classification models. Our application is designed to accurately identify Pneumonia and Covid cases from X-ray and CT images, bringing crucial medical insights to your fingertips.
### Research & Results
Gain profound insights into the intricate technical aspects of our research through the pages of our comprehensive research paper. Explore the intricacies of our integrated AI models, delve into our training methodologies, and uncover details about the datasets we utilized by clicking [here](PULMO.pdf)!  
  

### Pulmo Overview
- Walkthrough of the application
  

https://github.com/Andrew2077/PulmoAI/assets/92538925/9afdae6f-deb6-4e9b-a05c-68e278741180



## Table of Contents
- [ Pulmo AI : Automatic Covid \& Pneumonia Detection ](#-pulmo-ai--automatic-covid--pneumonia-detection-)
    - [Research \& Results](#research--results)
    - [Pulmo Overview](#pulmo-overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [installation - Conda](#installation---conda)
  - [Main Tools](#main-tools)
  - [Future Work](#future-work)
## Features 
- Multiple AI modalities 
- Firendly User Interface - Web Application
- Database integration
- Fast prediction time [Strong GPU required]
  - The project was built to run on `GTX1650 4GB` GPU, and it takes around 7 seconds to switch between models and predict the results
  - with a stronger GPU the wprediction time will be significantly reduced

## installation - Conda
> warning: AI models are not uploaded yet

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
- Follow the Firebase Authentication Guide here
  -  [Firebase connection authentication](Pulmo-AI/readme.md)
- Navigate to the Pulmo-AI directory
  ```bash
  python app.py
  ```

## Main Tools

- `Python` - The primary programming language employed throughout our research endeavors. Python was instrumental in managing backend connections and facilitating database integration.

- `TensorFlow` - Utilized for both research and deployment purposes, TensorFlow played a pivotal role in our projects.

- `Flask` - Our application was constructed using the Flask framework, offering a easy and solid foundation for its development.

- `Firebase` - We established a linkage to Firebase cloud storage, effectively storing our images in a remote environment.

- `PIL` (Python Imaging Library) - PIL was employed to fine-tune images for compatibility with AI models, ensuring seamless integration.

- `Plotly` and `Matplotlib` - These visualization libraries were harnessed to present our research findings, offering clear and visually engaging insights. Moreover, they facilitated model predictions within our application.

- `JavaScript` - This scripting language was strategically employed to manage some backend events, oversee user interface interactions, and provide dynamic animations within the application framework.

- `HTML` , `CSS` and `jinja2` - were utilized to construct the user interface, offering a visually appealing and intuitive experience for users.


## Future Work
- Conduct XAI (Explainable AI) research to explain the models predictions
- Deploy the application on a cloud platform - MLOps
- Improve the UI/UX
- Efficiently quantize the models to reduce the size and improve the prediction time to be more suitable for weak GPUs.
